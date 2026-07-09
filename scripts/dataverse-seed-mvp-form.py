#!/usr/bin/env python3
"""Seed one TACATDP MVP form/version/assignment for the Canvas renderer.

The command is idempotent and narrow:
- dev target only;
- explicit --execute required for writes;
- creates one form, one published form version, one section, MVP renderer questions,
  choices, validation rules, and one active assignment;
- no deletes and no bulk reference imports.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

DEFAULT_ASSIGNMENT_EMAIL = "john.mduda@mshirikacorp.onmicrosoft.com"
FORM_CODE = "TACATDP-MVP-001"
FORM_NAME = "TACATDP MVP Field Visit"
FORM_VERSION_CODE = "2026-07-07-v1"
SECTION_CODE = "core"
SECTION_NAME = "Core Visit"

CHOICE = {
    "active": 100000001,
    "published": 100000001,
    "assignment_active": 100000000,
    "q_text": 100000000,
    "q_integer": 100000001,
    "q_decimal": 100000002,
    "q_date": 100000003,
    "q_select_one": 100000004,
    "q_select_many": 100000005,
    "q_file_photo": 100000006,
    "q_gps": 100000007,
    "rule_required": 100000000,
}

QUESTIONS = [
    {"code": "farmer_name", "type": "q_text", "label": "Farmer name", "required": True, "order": 10},
    {"code": "farmer_age", "type": "q_integer", "label": "Farmer age", "required": False, "order": 20},
    {"code": "land_size_acres", "type": "q_decimal", "label": "Land size acres", "required": False, "order": 30},
    {"code": "visit_date", "type": "q_date", "label": "Visit date", "required": True, "order": 40},
    {"code": "primary_crop", "type": "q_select_one", "label": "Primary crop", "required": True, "order": 50,
     "choices": [("maize", "Maize"), ("rice", "Rice"), ("sunflower", "Sunflower"), ("other", "Other")]},
    {"code": "support_needed", "type": "q_select_many", "label": "Support needed", "required": False, "order": 60,
     "choices": [("finance", "Finance"), ("inputs", "Inputs"), ("training", "Training"), ("market", "Market linkage")]},
    {"code": "farm_photo", "type": "q_file_photo", "label": "Farm photo", "required": False, "order": 70},
    {"code": "gps_point", "type": "q_gps", "label": "GPS point", "required": False, "order": 80},
]


def load_deploy_module():
    module_path = Path(__file__).resolve().parent / "dataverse-schema-deploy.py"
    spec = importlib.util.spec_from_file_location("dataverse_schema_deploy", module_path)
    if not spec or not spec.loader:
        raise SystemExit(f"Unable to load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["dataverse_schema_deploy"] = module
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed one TACATDP MVP published form and assignment.")
    parser.add_argument("--env-file", default=".env", help="Environment file containing Power Platform settings.")
    parser.add_argument("--assignment-email", default=None, help="User email to receive the active form assignment.")
    parser.add_argument("--execute", action="store_true", help="Perform live writes. Without this flag only a dry-run summary is shown.")
    return parser.parse_args()


def escape_odata(value: str) -> str:
    return value.replace("'", "''")


def parse_guid_from_entity_id(value: str) -> str:
    return value.rsplit("(", 1)[-1].rstrip(")")


class SeedClient:
    def __init__(self, deploy: Any, settings: Any, token: str) -> None:
        self.deploy = deploy
        self.settings = settings
        self.dv = deploy.Dataverse(settings, token)
        self.prefix = settings.publisher_prefix
        self.entity_sets: dict[str, str] = {}
        self.primary_ids: dict[str, str] = {}
        self.nav_properties: dict[str, str] = {}

    def logical(self, table: str) -> str:
        return self.deploy.table_logical_name(self.prefix, table)

    def column(self, column: str) -> str:
        return self.deploy.column_logical_name(self.prefix, column)

    def entity_set(self, table: str) -> str:
        if table not in self.entity_sets:
            logical = self.logical(table)
            data = self.dv.get_json(f"EntityDefinitions(LogicalName='{logical}')?$select=EntitySetName,PrimaryIdAttribute")
            if not data:
                raise RuntimeError(f"Missing table metadata for {logical}")
            self.entity_sets[table] = data["EntitySetName"]
            self.primary_ids[table] = data["PrimaryIdAttribute"]
        return self.entity_sets[table]

    def primary_id(self, table: str) -> str:
        self.entity_set(table)
        return self.primary_ids[table]

    def nav_property(self, relationship_schema: str) -> str:
        if relationship_schema not in self.nav_properties:
            encoded = quote(relationship_schema, safe="")
            base = self.dv.get_json(f"RelationshipDefinitions(SchemaName='{encoded}')?$select=MetadataId")
            if not base:
                raise RuntimeError(f"Missing relationship metadata for {relationship_schema}")
            metadata_id = base["MetadataId"]
            data = self.dv.get_json(f"RelationshipDefinitions({metadata_id})/Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata?$select=ReferencingEntityNavigationPropertyName")
            if not data:
                raise RuntimeError(f"Missing one-to-many relationship metadata for {relationship_schema}")
            self.nav_properties[relationship_schema] = data["ReferencingEntityNavigationPropertyName"]
        return self.nav_properties[relationship_schema]

    def relationship_name(self, referenced: str, referencing: str, lookup: str) -> str:
        rel = {"referenced_table": referenced, "referencing_table": referencing, "lookup_column": lookup}
        return self.deploy.relationship_schema_name(self.settings, rel)

    def bind(self, referenced_table: str, referencing_table: str, lookup: str, record_id: str) -> tuple[str, str]:
        rel_schema = self.relationship_name(referenced_table, referencing_table, lookup)
        nav = self.nav_property(rel_schema)
        entity_set = "systemusers" if referenced_table == "SystemUser" else self.entity_set(referenced_table)
        return f"{nav}@odata.bind", f"/{entity_set}({record_id})"

    def find_one(self, table: str, filter_expr: str) -> dict[str, Any] | None:
        entity_set = self.entity_set(table)
        primary_id = self.primary_id(table)
        data = self.dv.get_json(f"{entity_set}?$select={primary_id}&$filter={filter_expr}&$top=1")
        values = (data or {}).get("value") or []
        return values[0] if values else None

    def create(self, table: str, payload: dict[str, Any]) -> str:
        entity_set = self.entity_set(table)
        response = self.dv.post(entity_set, payload)
        return parse_guid_from_entity_id(response.headers.get("OData-EntityId", ""))

    def ensure(self, table: str, filter_expr: str, payload: dict[str, Any], label: str, execute: bool) -> str | None:
        existing = self.find_one(table, filter_expr)
        primary_id = self.primary_id(table)
        if existing:
            print(f"exists: {label}")
            return existing[primary_id]
        if not execute:
            print(f"would create: {label}")
            return None
        record_id = self.create(table, payload)
        print(f"created: {label}")
        return record_id

    def find_system_user(self, email: str) -> str | None:
        escaped = escape_odata(email.lower())
        data = self.dv.get_json(f"systemusers?$select=systemuserid,internalemailaddress,domainname&$filter=internalemailaddress eq '{escaped}' or domainname eq '{escaped}'&$top=1")
        values = (data or {}).get("value") or []
        return values[0]["systemuserid"] if values else None


def env_assignment_email(deploy: Any, env_file: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    env = deploy.load_env(Path(env_file).resolve())
    return env.get("TACATDP_SEED_USER_EMAIL") or env.get("POWER_PLATFORM_ASSIGNMENT_USER_EMAIL") or DEFAULT_ASSIGNMENT_EMAIL


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    args = parse_args()
    deploy = load_deploy_module()
    settings = deploy.build_settings(argparse.Namespace(env_file=args.env_file, schema_dir=None, execute=False, no_publish=False))
    assignment_email = env_assignment_email(deploy, args.env_file, args.assignment_email)

    print("# TACATDP MVP Seed")
    print(f"Mode: {'execute' if args.execute else 'dry-run'}")
    print(f"Target: {settings.deploy_target}")
    print(f"Environment: {settings.environment_url}")
    print(f"Assignment email: {assignment_email}")
    print(f"Form code: {FORM_CODE}")

    if settings.deploy_target.lower() != "dev":
        raise SystemExit(f"Refusing non-dev deployment target: {settings.deploy_target}")
    if not args.execute:
        print("Dry-run only. Re-run with --execute to seed Dataverse rows.")

    token = deploy.get_token(settings)
    client = SeedClient(deploy, settings, token)
    now = datetime.now(timezone.utc).isoformat()

    form_id = client.ensure(
        "Forms",
        f"{client.column('FormCode')} eq '{escape_odata(FORM_CODE)}'",
        {
            client.column("FormCode"): FORM_CODE,
            client.column("Name"): FORM_NAME,
            client.column("Status"): CHOICE["active"],
        },
        f"form {FORM_CODE}",
        args.execute,
    )

    if not form_id and not args.execute:
        form_id = "DRY-RUN-FORM-ID"

    version_payload = {
        client.column("VersionCode"): FORM_VERSION_CODE,
        client.column("LifecycleStatus"): CHOICE["published"],
        client.column("PublishedAt"): now,
    }
    if args.execute:
        key, value = client.bind("Forms", "FormVersions", "Form", form_id)
        version_payload[key] = value
    version_id = client.ensure(
        "FormVersions",
        f"{client.column('VersionCode')} eq '{escape_odata(FORM_VERSION_CODE)}'",
        version_payload,
        f"form version {FORM_VERSION_CODE}",
        args.execute,
    )
    if not version_id and not args.execute:
        version_id = "DRY-RUN-VERSION-ID"

    section_payload = {
        client.column("SectionCode"): SECTION_CODE,
        client.column("Name"): SECTION_NAME,
        client.column("DisplayOrder"): 10,
    }
    if args.execute:
        key, value = client.bind("FormVersions", "Sections", "FormVersion", version_id)
        section_payload[key] = value
    section_id = client.ensure(
        "Sections",
        f"{client.column('SectionCode')} eq '{escape_odata(SECTION_CODE)}'",
        section_payload,
        f"section {SECTION_CODE}",
        args.execute,
    )
    if not section_id and not args.execute:
        section_id = "DRY-RUN-SECTION-ID"

    question_ids: dict[str, str] = {}
    for question in QUESTIONS:
        payload = {
            client.column("QuestionCode"): question["code"],
            client.column("Type"): CHOICE[question["type"]],
            client.column("Label"): question["label"],
            client.column("Required"): bool(question["required"]),
            client.column("DisplayOrder"): question["order"],
        }
        if args.execute:
            key, value = client.bind("Sections", "Questions", "Section", section_id)
            payload[key] = value
        question_id = client.ensure(
            "Questions",
            f"{client.column('QuestionCode')} eq '{escape_odata(question['code'])}'",
            payload,
            f"question {question['code']}",
            args.execute,
        )
        if question_id:
            question_ids[question["code"]] = question_id
        elif not args.execute:
            question_ids[question["code"]] = f"DRY-RUN-{question['code']}"

        if question.get("required"):
            rule_name = f"{question['code']}:required"
            rule_payload = {
                client.column("Name"): rule_name,
                client.column("RuleType"): CHOICE["rule_required"],
                client.column("Expression"): "true",
                client.column("Message"): "This field is required.",
            }
            if args.execute:
                key, value = client.bind("Questions", "ValidationRules", "Question", question_ids[question["code"]])
                rule_payload[key] = value
            client.ensure(
                "ValidationRules",
                f"{client.column('Name')} eq '{escape_odata(rule_name)}'",
                rule_payload,
                f"validation rule {rule_name}",
                args.execute,
            )

        for idx, (code, label) in enumerate(question.get("choices", []), start=1):
            choice_payload = {
                client.column("ChoiceCode"): code,
                client.column("Label"): label,
                client.column("DisplayOrder"): idx,
            }
            if args.execute:
                key, value = client.bind("Questions", "Choices", "Question", question_ids[question["code"]])
                choice_payload[key] = value
            client.ensure(
                "Choices",
                f"{client.column('ChoiceCode')} eq '{escape_odata(code)}'",
                choice_payload,
                f"choice {question['code']}.{code}",
                args.execute,
            )

    assignment_payload = {
        client.column("UserEmail"): assignment_email,
        client.column("Status"): CHOICE["assignment_active"],
    }
    if args.execute:
        key, value = client.bind("FormVersions", "FormAssignments", "FormVersion", version_id)
        assignment_payload[key] = value
        user_id = client.find_system_user(assignment_email)
        if user_id:
            key, value = client.bind("SystemUser", "FormAssignments", "User", user_id)
            assignment_payload[key] = value
            print(f"resolved systemuser for assignment: {assignment_email}")
        else:
            print(f"systemuser not found; using email-only assignment: {assignment_email}")
    client.ensure(
        "FormAssignments",
        f"{client.column('UserEmail')} eq '{escape_odata(assignment_email)}'",
        assignment_payload,
        f"assignment {assignment_email}",
        args.execute,
    )

    print("seed complete")
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
