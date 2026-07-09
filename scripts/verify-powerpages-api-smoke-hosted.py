#!/usr/bin/env python3
"""Verify hosted Power Pages/Dataverse state for the TACATDP API smoke slice.

This does not require opening a browser. It verifies the live configuration and
records that the Power Pages /api-smoke page depends on.
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

EXPECTED_TABLES = [
    "mp_project",
    "mp_form",
    "mp_formversion",
    "mp_formassignment",
    "mp_formattachment",
    "mp_submission",
    "mp_submissionversion",
    "mp_submissionattachment",
]
EXPECTED_ENTITY_SETS = {
    "mp_project": "mp_projects",
    "mp_form": "mp_forms",
    "mp_formversion": "mp_formversions",
    "mp_formassignment": "mp_formassignments",
    "mp_formattachment": "mp_formattachments",
    "mp_submission": "mp_submissions",
    "mp_submissionversion": "mp_submissionversions",
    "mp_submissionattachment": "mp_submissionattachments",
}
METADATA_TABLES = {
    "mp_project",
    "mp_form",
    "mp_formversion",
    "mp_formassignment",
    "mp_formattachment",
}
SUBMISSION_TABLES = {
    "mp_submission",
    "mp_submissionversion",
    "mp_submissionattachment",
}
GLOBAL_SCOPE = 756150000


def load_deploy_module() -> Any:
    module_path = Path(__file__).resolve().parent / "dataverse-schema-deploy.py"
    spec = importlib.util.spec_from_file_location("dataverse_schema_deploy", module_path)
    if not spec or not spec.loader:
        raise SystemExit(f"Unable to load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["dataverse_schema_deploy"] = module
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify hosted Power Pages API smoke prerequisites.")
    parser.add_argument("--env-file", default=".env", help="Environment file containing Power Platform settings.")
    parser.add_argument("--website-id", default=None, help="Expected Power Pages website ID.")
    parser.add_argument("--site-name", default=None, help="Expected Power Pages site name.")
    parser.add_argument("--skip-source", action="store_true", help="Skip local source validator.")
    return parser.parse_args()


def escape_odata(value: str) -> str:
    return value.replace("'", "''")


class CheckFailure(Exception):
    pass


class Verifier:
    def __init__(self, deploy: Any, dv: Any, website_id: str | None, site_name: str, test_user_email: str) -> None:
        self.deploy = deploy
        self.dv = dv
        self.website_id = website_id
        self.site_name = site_name
        self.test_user_email = test_user_email
        self.failures: list[str] = []

    def check(self, label: str, condition: bool, detail: str = "") -> None:
        if condition:
            print(f"ok: {label}{' - ' + detail if detail else ''}")
            return
        message = f"FAIL: {label}{' - ' + detail if detail else ''}"
        print(message)
        self.failures.append(message)

    def first(self, entity_set: str, filter_expr: str, select: str) -> dict[str, Any] | None:
        data = self.dv.get_json(f"{entity_set}?$select={select}&$filter={filter_expr}&$top=1")
        values = (data or {}).get("value") or []
        return values[0] if values else None

    def rows(self, path: str) -> list[dict[str, Any]]:
        data = self.dv.get_json(path)
        return (data or {}).get("value") or []

    def resolve_website(self) -> str:
        if self.website_id:
            data = self.dv.get_json(f"mspp_websites({self.website_id})?$select=mspp_websiteid,mspp_name")
            self.check("website id exists", bool(data), self.website_id)
            return self.website_id
        data = self.first(
            "mspp_websites",
            f"mspp_name eq '{escape_odata(self.site_name)}'",
            "mspp_websiteid,mspp_name",
        )
        self.check("website name exists", bool(data), self.site_name)
        if not data:
            raise CheckFailure("website could not be resolved")
        return data["mspp_websiteid"]

    def verify_entity_sets(self) -> None:
        for logical, expected_set in EXPECTED_ENTITY_SETS.items():
            data = self.dv.get_json(f"EntityDefinitions(LogicalName='{logical}')?$select=LogicalName,EntitySetName")
            actual = (data or {}).get("EntitySetName")
            self.check(f"entity set {logical}", actual == expected_set, f"expected {expected_set}, got {actual}")

    def verify_webapi_settings(self, website_id: str) -> None:
        expected_names = {f"Webapi/{table}/{suffix}" for table in EXPECTED_TABLES for suffix in ("enabled", "fields")}
        rows = self.rows(
            "mspp_sitesettings?$select=mspp_name,mspp_value,_mspp_websiteid_value"
            f"&$filter=_mspp_websiteid_value eq {website_id} and startswith(mspp_name,'Webapi/mp_')&$top=100"
        )
        found = {row.get("mspp_name"): row.get("mspp_value") for row in rows}
        self.check("web api setting count", len(found) == len(expected_names), f"{len(found)} of {len(expected_names)}")
        for name in sorted(expected_names):
            value = found.get(name)
            expected = "true" if name.endswith("/enabled") else "*"
            self.check(f"web api setting {name}", value == expected, f"expected {expected}, got {value}")
        blank = self.rows(
            "mspp_sitesettings?$select=mspp_sitesettingid"
            f"&$filter=_mspp_websiteid_value eq {website_id} and mspp_name eq null&$top=100"
        )
        self.check("no nameless site settings", not blank, str(len(blank)))

    def verify_permissions(self, website_id: str) -> None:
        role = self.first(
            "mspp_webroles",
            f"_mspp_websiteid_value eq {website_id} and mspp_authenticatedusersrole eq true",
            "mspp_webroleid,mspp_name",
        )
        self.check("authenticated users role exists", bool(role), "Authenticated Users")
        role_id = role["mspp_webroleid"] if role else ""
        rows = self.rows(
            "mspp_entitypermissions?$select=mspp_entitypermissionid,mspp_entitylogicalname,mspp_scope,"
            "mspp_read,mspp_create,mspp_write,mspp_delete,mspp_append,mspp_appendto"
            f"&$filter=_mspp_websiteid_value eq {website_id} and startswith(mspp_entitylogicalname,'mp_')&$top=100"
        )
        by_table = {row["mspp_entitylogicalname"]: row for row in rows}
        self.check("table permission count", len(by_table) == len(EXPECTED_TABLES), f"{len(by_table)} of {len(EXPECTED_TABLES)}")
        for table in EXPECTED_TABLES:
            row = by_table.get(table)
            self.check(f"table permission {table} exists", row is not None)
            if not row:
                continue
            self.check(f"table permission {table} global scope", row.get("mspp_scope") == GLOBAL_SCOPE)
            self.check(f"table permission {table} read", row.get("mspp_read") is True)
            if table in METADATA_TABLES:
                self.check(f"table permission {table} metadata read-only", not any(row.get(name) for name in ("mspp_create", "mspp_write", "mspp_delete", "mspp_append", "mspp_appendto")))
            if table in SUBMISSION_TABLES:
                self.check(f"table permission {table} submission write flags", all(row.get(name) is True for name in ("mspp_create", "mspp_write", "mspp_append", "mspp_appendto")) and row.get("mspp_delete") is False)
            link_rows = self.rows(
                "mspp_entitypermission_webroleset?$select=mspp_entitypermission_webroleid"
                f"&$filter=mspp_entitypermissionid eq {row['mspp_entitypermissionid']} and mspp_webroleid eq {role_id}&$top=1"
            )
            self.check(f"table permission {table} linked to authenticated users", bool(link_rows))
            enhanced_link_rows = self.rows(
                "powerpagecomponent_powerpagecomponent?$select=powerpagecomponentidone,powerpagecomponentidtwo"
                f"&$filter=powerpagecomponentidone eq {row['mspp_entitypermissionid']} and powerpagecomponentidtwo eq {role_id}&$top=1"
            )
            self.check(f"enhanced table permission {table} linked to authenticated users", bool(enhanced_link_rows))

    def verify_smoke_page(self) -> None:
        rows = self.rows(
            "mspp_webpages?$select=mspp_webpageid,mspp_name,mspp_partialurl,mspp_isroot,_mspp_rootwebpageid_value"
            "&$filter=mspp_partialurl eq 'api-smoke'&$top=10"
        )
        roots = [row for row in rows if row.get("mspp_isroot") is True]
        content = [row for row in rows if row.get("mspp_isroot") is False]
        self.check("api-smoke page rows", len(rows) == 2, str(len(rows)))
        self.check("api-smoke root page", len(roots) == 1, str(len(roots)))
        self.check("api-smoke content page", len(content) == 1, str(len(content)))

    def verify_portal_user(self) -> None:
        email = escape_odata(self.test_user_email)
        rows = self.rows(
            "contacts?$select=contactid,fullname,emailaddress1,statecode,statuscode"
            f"&$filter=emailaddress1 eq '{email}'&$top=5"
        )
        self.check("portal contact exists for test user", bool(rows), self.test_user_email)
        if rows:
            self.check("portal contact is active", any(row.get("statecode") == 0 for row in rows), self.test_user_email)

    def verify_seed_data(self) -> None:
        assignments = self.rows(
            "mp_formassignments?$select=mp_formassignmentid,mp_assignmentkey,mp_useremail,_mp_formversion_value&$top=10"
        )
        self.check("assignment seed exists", bool(assignments), str(len(assignments)))
        assignment = assignments[0] if assignments else None
        form_version_id = (assignment or {}).get("_mp_formversion_value")
        self.check("assignment has form version lookup", bool(form_version_id))
        if not form_version_id:
            return
        version = self.dv.get_json(
            f"mp_formversions({form_version_id})?$select=mp_version,mp_webformsenabled,mp_lifecyclestatus,mp_xformxml,_mp_form_value"
        )
        self.check("form version exists", bool(version), form_version_id)
        self.check("form version web forms enabled", (version or {}).get("mp_webformsenabled") is True)
        xform = (version or {}).get("mp_xformxml") or ""
        self.check("form version has XForm XML", len(xform) > 1000, f"{len(xform)} bytes")
        form_id = (version or {}).get("_mp_form_value")
        self.check("form version has form lookup", bool(form_id))
        if form_id:
            form = self.dv.get_json(f"mp_forms({form_id})?$select=mp_name,mp_xmlformid,mp_lifecyclestatus")
            self.check("form exists", bool(form), form_id)
            self.check("form XmlFormId populated", bool((form or {}).get("mp_xmlformid")), (form or {}).get("mp_xmlformid") or "")

    def finish(self) -> None:
        if self.failures:
            raise CheckFailure(f"{len(self.failures)} hosted smoke checks failed")


def run_source_validator(skip_source: bool) -> None:
    if skip_source:
        print("skip: local source validator")
        return
    result = subprocess.run(
        [sys.executable, "scripts/validate-powerpages-api-smoke.py"],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr.strip())
        raise CheckFailure("local source validator failed")


def main() -> int:
    args = parse_args()
    deploy = load_deploy_module()
    settings = deploy.build_settings(
        argparse.Namespace(env_file=args.env_file, schema_dir=None, schema_file=None, execute=False, no_publish=False)
    )
    env = deploy.load_env(Path(args.env_file).resolve())
    website_id = args.website_id or env.get("POWERPAGES_WEBSITE_ID") or None
    site_name = args.site_name or env.get("POWERPAGES_SITE_NAME") or "TACATDP Monitoring Tool"
    test_user_email = env.get("TACATDP_SEED_USER_EMAIL") or env.get("POWER_PLATFORM_ASSIGNMENT_USER_EMAIL") or "john.mduda@mshirikacorp.onmicrosoft.com"

    print("# TACATDP Hosted Power Pages API Smoke Verification")
    print(f"Target: {settings.deploy_target}")
    print(f"Environment: {settings.environment_url}")
    print(f"Site: {site_name}")
    run_source_validator(args.skip_source)

    dv = deploy.Dataverse(settings, deploy.get_token(settings))
    verifier = Verifier(deploy, dv, website_id, site_name, test_user_email)
    resolved_website_id = verifier.resolve_website()
    print(f"Website ID: {resolved_website_id}")
    verifier.verify_entity_sets()
    verifier.verify_webapi_settings(resolved_website_id)
    verifier.verify_permissions(resolved_website_id)
    verifier.verify_smoke_page()
    verifier.verify_portal_user()
    verifier.verify_seed_data()
    verifier.finish()
    print("hosted Power Pages API smoke verification passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
