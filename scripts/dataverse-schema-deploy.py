#!/usr/bin/env python3
"""Create the TACATDP MVP Dataverse schema through Dataverse Web API metadata calls.

This command is intentionally narrow:
- dev target only;
- explicit --execute required for writes;
- creates missing publisher/solution/table/column/relationship metadata;
- no deletes, no updates, no data import, no production deployment.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

API_VERSION = "v9.2"
TOKEN_URL_TEMPLATE = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"

CHOICE_VALUES = {
    ("Forms", "Status"): ["Draft", "Active", "Retired"],
    ("FormVersions", "LifecycleStatus"): ["Draft", "Published", "Retired"],
    ("Questions", "Type"): ["text", "integer", "decimal", "date", "select_one", "select_many", "file_photo_attachment", "gps"],
    ("ValidationRules", "RuleType"): ["required", "relevant", "constraint"],
    ("FormAssignments", "Status"): ["Active", "Inactive"],
    ("Submissions", "Status"): ["Draft", "Submitted", "Locked"],
}

PRIMARY_NAME_COLUMNS = {
    "Forms": "Name",
    "FormVersions": "VersionCode",
    "Sections": "Name",
    "Questions": "QuestionCode",
    "Choices": "ChoiceCode",
    "ValidationRules": "Name",
    "FormAssignments": "UserEmail",
    "Submissions": "UserEmail",
    "SubmissionAnswers": "ValueText",
    "SubmissionFiles": "FileName",
}

SINGULAR_SCHEMA_NAMES = {
    "Forms": "Form",
    "FormVersions": "FormVersion",
    "Sections": "Section",
    "Questions": "Question",
    "Choices": "Choice",
    "ValidationRules": "ValidationRule",
    "FormAssignments": "FormAssignment",
    "Submissions": "Submission",
    "SubmissionAnswers": "SubmissionAnswer",
    "SubmissionFiles": "SubmissionFile",
}

SYSTEM_TABLE_LOGICAL = {
    "SystemUser": "systemuser",
}


@dataclass(frozen=True)
class Settings:
    tenant_id: str
    client_id: str
    client_secret: str
    environment_url: str
    solution_unique_name: str
    solution_display_name: str
    publisher_name: str
    publisher_prefix: str
    deploy_target: str
    schema_dir: Path
    schema_file: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create TACATDP MVP Dataverse schema metadata. Requires --execute for writes.")
    parser.add_argument("--env-file", default=".env", help="Environment file containing Power Platform settings.")
    parser.add_argument("--schema-dir", default=None, help="Schema directory. Defaults to TACATDP_DATAVERSE_SCHEMA_DIR from env or schemas/dataverse.")
    parser.add_argument("--schema-file", default=None, help="Schema definition JSON. Defaults to TACATDP_DATAVERSE_SCHEMA_FILE from env or <schema-dir>/mvp-schema-definition.json.")
    parser.add_argument("--execute", action="store_true", help="Perform live writes. Without this flag only a dry-run summary is shown.")
    parser.add_argument("--no-publish", action="store_true", help="Skip PublishAllXml after metadata creation.")
    return parser.parse_args()


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def require(env: dict[str, str], key: str) -> str:
    value = env.get(key, "").strip()
    if not value:
        raise SystemExit(f"Missing required env value: {key}")
    return value


def build_settings(args: argparse.Namespace) -> Settings:
    env_file = Path(args.env_file).resolve()
    if not env_file.exists():
        raise SystemExit(f"Env file not found: {env_file}")
    env = load_env(env_file)
    schema_dir = Path(args.schema_dir or env.get("TACATDP_DATAVERSE_SCHEMA_DIR") or "schemas/dataverse").resolve()
    schema_file = Path(args.schema_file or env.get("TACATDP_DATAVERSE_SCHEMA_FILE") or schema_dir / "mvp-schema-definition.json").resolve()
    return Settings(
        tenant_id=require(env, "POWER_PLATFORM_TENANT_ID"),
        client_id=require(env, "POWER_PLATFORM_CLIENT_ID"),
        client_secret=require(env, "POWER_PLATFORM_CLIENT_SECRET"),
        environment_url=require(env, "POWER_PLATFORM_ENVIRONMENT_URL").rstrip("/"),
        solution_unique_name=require(env, "POWER_PLATFORM_SOLUTION_UNIQUE_NAME"),
        solution_display_name=env.get("POWER_PLATFORM_SOLUTION_DISPLAY_NAME") or require(env, "POWER_PLATFORM_SOLUTION_UNIQUE_NAME"),
        publisher_name=env.get("POWER_PLATFORM_PUBLISHER_NAME") or "TACATDP",
        publisher_prefix=require(env, "POWER_PLATFORM_PUBLISHER_PREFIX"),
        deploy_target=require(env, "TACATDP_DEPLOY_TARGET"),
        schema_dir=schema_dir,
        schema_file=schema_file,
    )


def load_schema(settings: Settings) -> dict[str, Any]:
    path = settings.schema_file
    if not path.exists():
        raise SystemExit(f"Schema definition not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def label(text: str) -> dict[str, Any]:
    return {
        "@odata.type": "Microsoft.Dynamics.CRM.Label",
        "LocalizedLabels": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                "Label": text,
                "LanguageCode": 1033,
            }
        ],
    }


def required_level(required: bool) -> dict[str, Any]:
    return {
        "Value": "ApplicationRequired" if required else "None",
        "CanBeChanged": True,
        "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings",
    }


def schema_name(prefix: str, raw_name: str) -> str:
    return f"{prefix}_{raw_name[0].upper()}{raw_name[1:]}"


def singular_name(table: dict[str, Any] | str) -> str:
    if isinstance(table, dict):
        return table.get("singular_name") or SINGULAR_SCHEMA_NAMES.get(table["name"]) or table["name"].removesuffix("s")
    return SINGULAR_SCHEMA_NAMES.get(table) or table.removesuffix("s")


def table_schema_name(prefix: str, table_name: str, table: dict[str, Any] | None = None) -> str:
    return schema_name(prefix, singular_name(table or table_name))


def table_logical_name(prefix: str, table_name: str, table: dict[str, Any] | None = None) -> str:
    return table_schema_name(prefix, table_name, table).lower()


def column_schema_name(prefix: str, column_name: str) -> str:
    return schema_name(prefix, column_name)


def column_logical_name(prefix: str, column_name: str) -> str:
    return column_schema_name(prefix, column_name).lower()


def get_token(settings: Settings) -> str:
    token_url = TOKEN_URL_TEMPLATE.format(tenant=settings.tenant_id)
    response = requests.post(
        token_url,
        data={
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "scope": f"{settings.environment_url}/.default",
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    if response.status_code >= 400:
        raise SystemExit(f"Token request failed: HTTP {response.status_code} {safe_error(response)}")
    return response.json()["access_token"]


class Dataverse:
    def __init__(self, settings: Settings, token: str) -> None:
        self.settings = settings
        self.base = f"{settings.environment_url}/api/data/{API_VERSION}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        })

    def request(self, method: str, path: str, *, payload: dict[str, Any] | None = None, solution_header: bool = False) -> requests.Response:
        headers = {}
        if solution_header:
            headers["MSCRM.SolutionUniqueName"] = self.settings.solution_unique_name
        response = self.session.request(method, f"{self.base}/{path.lstrip('/')}", json=payload, headers=headers, timeout=60)
        if response.status_code in {429, 500, 502, 503, 504}:
            time.sleep(3)
            response = self.session.request(method, f"{self.base}/{path.lstrip('/')}", json=payload, headers=headers, timeout=60)
        return response

    def get_json(self, path: str) -> dict[str, Any] | None:
        response = self.request("GET", path)
        if response.status_code == 404:
            return None
        if response.status_code >= 400:
            raise RuntimeError(f"GET {path} failed: HTTP {response.status_code} {safe_error(response)}")
        return response.json()

    def post(self, path: str, payload: dict[str, Any], *, solution_header: bool = False) -> requests.Response:
        response = self.request("POST", path, payload=payload, solution_header=solution_header)
        if response.status_code >= 400:
            raise RuntimeError(f"POST {path} failed: HTTP {response.status_code} {safe_error(response)}")
        return response


def safe_error(response: requests.Response) -> str:
    try:
        data = response.json()
        error = data.get("error") or data
        if isinstance(error, dict):
            return str(error.get("message") or error.get("code") or error)[:1000]
        return str(error)[:1000]
    except Exception:
        return response.text[:1000]


def query_first(dv: Dataverse, entity_set: str, filter_expr: str, select: str) -> dict[str, Any] | None:
    data = dv.get_json(f"{entity_set}?$select={select}&$filter={filter_expr}&$top=1")
    values = (data or {}).get("value") or []
    return values[0] if values else None


def ensure_publisher(dv: Dataverse) -> str:
    settings = dv.settings
    existing = query_first(dv, "publishers", f"customizationprefix eq '{settings.publisher_prefix}'", "publisherid,customizationprefix")
    if existing:
        print(f"publisher exists: {settings.publisher_prefix}")
        return existing["publisherid"]
    payload = {
        "uniquename": settings.publisher_name.lower(),
        "friendlyname": settings.publisher_name,
        "customizationprefix": settings.publisher_prefix,
        "customizationoptionvalueprefix": 10000,
    }
    response = dv.post("publishers", payload)
    publisher_id = response.headers.get("OData-EntityId", "").rsplit("(", 1)[-1].rstrip(")")
    if not publisher_id:
        created = query_first(dv, "publishers", f"customizationprefix eq '{settings.publisher_prefix}'", "publisherid,customizationprefix")
        if not created:
            raise RuntimeError("Publisher was created but publisher id could not be resolved")
        publisher_id = created["publisherid"]
    print(f"publisher created: {settings.publisher_prefix}")
    return publisher_id


def ensure_solution(dv: Dataverse, publisher_id: str) -> None:
    settings = dv.settings
    existing = query_first(dv, "solutions", f"uniquename eq '{settings.solution_unique_name}'", "solutionid,uniquename")
    if existing:
        print(f"solution exists: {settings.solution_unique_name}")
        return
    payload = {
        "uniquename": settings.solution_unique_name,
        "friendlyname": settings.solution_display_name,
        "version": "0.1.0.0",
        "publisherid@odata.bind": f"/publishers({publisher_id})",
    }
    dv.post("solutions", payload)
    print(f"solution created: {settings.solution_unique_name}")


def entity_exists(dv: Dataverse, logical_name: str) -> bool:
    data = dv.get_json(f"EntityDefinitions(LogicalName='{logical_name}')?$select=LogicalName")
    return data is not None


def attribute_exists(dv: Dataverse, table_logical: str, attr_logical: str) -> bool:
    data = dv.get_json(f"EntityDefinitions(LogicalName='{table_logical}')/Attributes(LogicalName='{attr_logical}')?$select=LogicalName")
    return data is not None


def relationship_exists(dv: Dataverse, rel_schema: str) -> bool:
    response = dv.request("GET", f"RelationshipDefinitions(SchemaName='{rel_schema}')?$select=SchemaName")
    if response.status_code == 404:
        return False
    if response.status_code >= 400:
        raise RuntimeError(f"GET relationship {rel_schema} failed: HTTP {response.status_code} {safe_error(response)}")
    return True


def attr_payload(settings: Settings, table_name: str, column: dict[str, Any]) -> dict[str, Any]:
    col_name = column["name"]
    col_type = column["type"]
    base: dict[str, Any] = {
        "SchemaName": column_schema_name(settings.publisher_prefix, col_name),
        "DisplayName": label(col_name),
        "Description": label(column.get("notes") or col_name),
        "RequiredLevel": required_level(bool(column.get("required"))),
    }
    if col_type == "Text":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "MaxLength": 850,
            "FormatName": {"Value": "Text"},
        })
    elif col_type == "MultilineText":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.MemoAttributeMetadata",
            "MaxLength": 1048576,
            "FormatName": {"Value": "TextArea"},
        })
    elif col_type == "WholeNumber":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
            "MinValue": -2147483648,
            "MaxValue": 2147483647,
            "Format": "None",
        })
    elif col_type == "Decimal":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.DecimalAttributeMetadata",
            "MinValue": -100000000000,
            "MaxValue": 100000000000,
            "Precision": 4,
        })
    elif col_type == "Date":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
            "Format": "DateOnly",
            "DateTimeBehavior": {"Value": "DateOnly"},
        })
    elif col_type == "DateTime":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
            "Format": "DateAndTime",
            "DateTimeBehavior": {"Value": "UserLocal"},
        })
    elif col_type == "Boolean":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
            "DefaultValue": False,
            "OptionSet": {
                "TrueOption": {"Value": 1, "Label": label("Yes")},
                "FalseOption": {"Value": 0, "Label": label("No")},
            },
        })
    elif col_type == "Choice":
        values = column.get("choices") or CHOICE_VALUES.get((table_name, col_name), ["Active", "Inactive"])
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.PicklistAttributeMetadata",
            "OptionSet": {
                "@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata",
                "IsGlobal": False,
                "OptionSetType": "Picklist",
                "Options": [
                    {"Value": 100000000 + idx, "Label": label(value)}
                    for idx, value in enumerate(values)
                ],
            },
        })
    elif col_type == "File":
        base.update({
            "@odata.type": "Microsoft.Dynamics.CRM.FileAttributeMetadata",
            "MaxSizeInKB": 131072,
        })
    else:
        raise ValueError(f"Unsupported non-lookup column type: {table_name}.{col_name} {col_type}")
    return base


def create_table_payload(settings: Settings, table: dict[str, Any]) -> dict[str, Any]:
    table_name = table["name"]
    primary = table.get("primary_name_column") or PRIMARY_NAME_COLUMNS[table_name]
    primary_col = next((col for col in table["columns"] if col["name"] == primary), None)
    if not primary_col:
        raise ValueError(f"Primary name column missing for {table_name}: {primary}")
    primary_payload = attr_payload(settings, table_name, primary_col)
    primary_payload["IsPrimaryName"] = True
    return {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
        "SchemaName": table_schema_name(settings.publisher_prefix, table_name, table),
        "DisplayName": label(table_name),
        "DisplayCollectionName": label(table_name),
        "Description": label(table.get("purpose") or table_name),
        "OwnershipType": "UserOwned",
        "IsActivity": False,
        "HasActivities": False,
        "HasNotes": False,
        "Attributes": [primary_payload],
    }


def ensure_tables(dv: Dataverse, schema: dict[str, Any]) -> None:
    for table in schema["tables"]:
        logical = table_logical_name(dv.settings.publisher_prefix, table["name"], table)
        if entity_exists(dv, logical):
            print(f"table exists: {logical}")
            continue
        dv.post("EntityDefinitions", create_table_payload(dv.settings, table), solution_header=True)
        print(f"table created: {logical}")


def ensure_columns(dv: Dataverse, schema: dict[str, Any]) -> None:
    for table in schema["tables"]:
        table_name = table["name"]
        table_logical = table_logical_name(dv.settings.publisher_prefix, table_name)
        primary = table.get("primary_name_column") or PRIMARY_NAME_COLUMNS[table_name]
        for column in table["columns"]:
            if column["name"] == primary or str(column["type"]).startswith("Lookup:"):
                continue
            attr_logical = column_logical_name(dv.settings.publisher_prefix, column["name"])
            if attribute_exists(dv, table_logical, attr_logical):
                print(f"column exists: {table_logical}.{attr_logical}")
                continue
            dv.post(f"EntityDefinitions(LogicalName='{table_logical}')/Attributes", attr_payload(dv.settings, table_name, column), solution_header=True)
            print(f"column created: {table_logical}.{attr_logical}")


def relationship_schema_name(settings: Settings, rel: dict[str, Any]) -> str:
    ref = rel["referenced_table"]
    referencing = rel["referencing_table"]
    lookup = rel["lookup_column"]
    ref_part = SYSTEM_TABLE_LOGICAL.get(ref, SINGULAR_SCHEMA_NAMES.get(ref, ref.removesuffix("s")))
    referencing_part = SINGULAR_SCHEMA_NAMES.get(referencing, referencing.removesuffix("s"))
    return f"{settings.publisher_prefix}_{ref_part}_{referencing_part}_{lookup}"


def referenced_logical(settings: Settings, table_name: str) -> str:
    if table_name in SYSTEM_TABLE_LOGICAL:
        return SYSTEM_TABLE_LOGICAL[table_name]
    return table_logical_name(settings.publisher_prefix, table_name)


def ensure_relationships(dv: Dataverse, schema: dict[str, Any]) -> None:
    for rel in schema["relationships"]:
        rel_schema = relationship_schema_name(dv.settings, rel)
        if relationship_exists(dv, rel_schema):
            print(f"relationship exists: {rel_schema}")
            continue
        referencing_logical = table_logical_name(dv.settings.publisher_prefix, rel["referencing_table"])
        lookup_schema = column_schema_name(dv.settings.publisher_prefix, rel["lookup_column"])
        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata",
            "SchemaName": rel_schema,
            "ReferencedEntity": referenced_logical(dv.settings, rel["referenced_table"]),
            "ReferencingEntity": referencing_logical,
            "Lookup": {
                "SchemaName": lookup_schema,
                "DisplayName": label(rel["lookup_column"]),
                "Description": label(rel.get("notes") or rel["lookup_column"]),
                "RequiredLevel": required_level(bool(rel.get("required"))),
            },
            "CascadeConfiguration": {
                "Assign": "NoCascade",
                "Delete": "RemoveLink",
                "Merge": "NoCascade",
                "Reparent": "NoCascade",
                "Share": "NoCascade",
                "Unshare": "NoCascade",
            },
        }
        dv.post("RelationshipDefinitions", payload, solution_header=True)
        print(f"relationship created: {rel_schema}")


def publish(dv: Dataverse) -> None:
    dv.post("PublishAllXml", {})
    print("customizations published")


def print_summary(settings: Settings, schema: dict[str, Any], execute: bool) -> None:
    tables = schema.get("tables", [])
    column_count = sum(len(table.get("columns", [])) for table in tables)
    rel_count = len(schema.get("relationships", []))
    print("# TACATDP Dataverse MVP Schema Deploy")
    print(f"Mode: {'execute' if execute else 'dry-run'}")
    print(f"Target: {settings.deploy_target}")
    print(f"Environment: {settings.environment_url}")
    print(f"Solution: {settings.solution_unique_name}")
    print(f"Publisher prefix: {settings.publisher_prefix}")
    print(f"Schema file: {settings.schema_file}")
    print(f"Tables: {len(tables)}")
    print(f"Columns: {column_count}")
    print(f"Relationships: {rel_count}")


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    args = parse_args()
    settings = build_settings(args)
    schema = load_schema(settings)
    print_summary(settings, schema, args.execute)

    if settings.deploy_target.lower() != "dev":
        raise SystemExit(f"Refusing non-dev deployment target: {settings.deploy_target}")
    if not args.execute:
        print("Dry-run only. Re-run with --execute to write metadata.")
        return 0

    token = get_token(settings)
    dv = Dataverse(settings, token)
    publisher_id = ensure_publisher(dv)
    ensure_solution(dv, publisher_id)
    ensure_tables(dv, schema)
    ensure_columns(dv, schema)
    ensure_relationships(dv, schema)
    if not args.no_publish:
        publish(dv)
    print("schema deployment complete")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except requests.RequestException as exc:
        print(f"Network/API error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
