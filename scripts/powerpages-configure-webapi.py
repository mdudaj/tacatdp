#!/usr/bin/env python3
"""Configure Power Pages Web API and table permissions for TACATDP ODK MVP.

Idempotent dev-only configuration for the Power Pages enhanced data model (`mspp_*`):
- creates/updates Webapi/<table>/enabled and Webapi/<table>/fields site settings;
- creates/updates Global table permissions;
- associates permissions to the Authenticated Users web role.

This uses Dataverse Web API as an admin/configuration channel. It does not use the
Power Pages `/_api`, because Microsoft documents portal configuration tables as
unsupported through the portals Web API.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any

WEB_API_TABLES = [
    # metadata reads
    {"logical": "mp_project", "name": "TACATDP Projects", "read": True, "create": False, "write": False, "delete": False, "append": False, "appendto": False},
    {"logical": "mp_form", "name": "TACATDP Forms", "read": True, "create": False, "write": False, "delete": False, "append": False, "appendto": False},
    # FormVersions remain read-only to portal users, but submission create binds
    # mp_submission.mp_FormVersion to an existing form version. Power Pages
    # requires Append To on the referenced table for that association.
    {"logical": "mp_formversion", "name": "TACATDP FormVersions", "read": True, "create": False, "write": False, "delete": False, "append": False, "appendto": True},
    {"logical": "mp_formassignment", "name": "TACATDP FormAssignments", "read": True, "create": False, "write": False, "delete": False, "append": False, "appendto": False},
    {"logical": "mp_formattachment", "name": "TACATDP FormAttachments", "read": True, "create": False, "write": False, "delete": False, "append": False, "appendto": False},
    # submission writes for dev POC; tighten before production with contact/self/custom access
    {"logical": "mp_submission", "name": "TACATDP Submissions", "read": True, "create": True, "write": True, "delete": False, "append": True, "appendto": True},
    {"logical": "mp_submissionversion", "name": "TACATDP SubmissionVersions", "read": True, "create": True, "write": True, "delete": False, "append": True, "appendto": True},
    {"logical": "mp_submissionattachment", "name": "TACATDP SubmissionAttachments", "read": True, "create": True, "write": True, "delete": False, "append": True, "appendto": True},
]

GLOBAL_SCOPE = 756150000
SITE_SETTING_SOURCE_TABLE = 0


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
    parser = argparse.ArgumentParser(description="Configure Power Pages Web API site settings and table permissions for TACATDP MVP.")
    parser.add_argument("--env-file", default=".env", help="Environment file containing Power Platform settings.")
    parser.add_argument("--website-id", default=None, help="Power Pages website id. Defaults to POWERPAGES_WEBSITE_ID or the first matching site name.")
    parser.add_argument("--site-name", default=None, help="Power Pages site name. Defaults to POWERPAGES_SITE_NAME or TACATDP Monitoring Tool.")
    parser.add_argument("--portal-user-email", default=None, help="Optional portal contact email to assign to the Authenticated Users web role.")
    parser.add_argument("--execute", action="store_true", help="Perform live writes. Without this flag only a dry-run summary is shown.")
    return parser.parse_args()


def escape_odata(value: str) -> str:
    return value.replace("'", "''")


def parse_guid_from_entity_id(value: str) -> str:
    return value.rsplit("(", 1)[-1].rstrip(")")


class PagesConfigClient:
    def __init__(self, deploy: Any, settings: Any, token: str) -> None:
        self.deploy = deploy
        self.dv = deploy.Dataverse(settings, token)

    def find_website(self, website_id: str | None, site_name: str) -> str:
        if website_id:
            data = self.dv.get_json(f"mspp_websites({website_id})?$select=mspp_websiteid,mspp_name")
            if not data:
                raise RuntimeError(f"Power Pages website not found: {website_id}")
            return data["mspp_websiteid"]
        data = self.dv.get_json(f"mspp_websites?$select=mspp_websiteid,mspp_name&$filter=mspp_name eq '{escape_odata(site_name)}'&$top=1")
        values = (data or {}).get("value") or []
        if not values:
            raise RuntimeError(f"Power Pages website not found by name: {site_name}")
        return values[0]["mspp_websiteid"]

    def find_authenticated_role(self, website_id: str) -> str:
        data = self.dv.get_json(
            "mspp_webroles?$select=mspp_webroleid,mspp_name,mspp_authenticatedusersrole"
            f"&$filter=_mspp_websiteid_value eq {website_id} and mspp_authenticatedusersrole eq true&$top=1"
        )
        values = (data or {}).get("value") or []
        if not values:
            raise RuntimeError("Authenticated Users web role not found for site")
        return values[0]["mspp_webroleid"]

    def find_contact_by_email(self, email: str) -> str | None:
        data = self.dv.get_json(
            "contacts?$select=contactid,emailaddress1,statecode"
            f"&$filter=emailaddress1 eq '{escape_odata(email)}'&$top=1"
        )
        values = (data or {}).get("value") or []
        if not values:
            return None
        if values[0].get("statecode") != 0:
            raise RuntimeError(f"Portal contact is not active: {email}")
        return values[0]["contactid"]

    def ensure_site_setting(self, website_id: str, name: str, value: str, execute: bool) -> str | None:
        data = self.dv.get_json(
            "mspp_sitesettings?$select=mspp_sitesettingid,mspp_value"
            f"&$filter=_mspp_websiteid_value eq {website_id} and mspp_name eq '{escape_odata(name)}'&$top=1"
        )
        values = (data or {}).get("value") or []
        payload = {
            "mspp_name": name,
            "mspp_value": value,
            "mspp_source": SITE_SETTING_SOURCE_TABLE,
            "mspp_websiteid@odata.bind": f"/mspp_websites({website_id})",
        }
        if values:
            record_id = values[0]["mspp_sitesettingid"]
            if values[0].get("mspp_value") == value:
                print(f"exists: site setting {name}={value}")
            elif execute:
                response = self.dv.request("PATCH", f"mspp_sitesettings({record_id})", payload=payload)
                if response.status_code >= 400:
                    raise RuntimeError(f"PATCH site setting {name} failed: HTTP {response.status_code} {self.deploy.safe_error(response)}")
                print(f"updated: site setting {name}={value}")
            else:
                print(f"would update: site setting {name}={value}")
            return record_id
        if not execute:
            print(f"would create: site setting {name}={value}")
            return None
        response = self.dv.post("mspp_sitesettings", payload)
        print(f"created: site setting {name}={value}")
        return parse_guid_from_entity_id(response.headers.get("OData-EntityId", ""))

    def ensure_permission(self, website_id: str, role_id: str, table: dict[str, Any], execute: bool) -> str | None:
        logical = table["logical"]
        name = table["name"]
        data = self.dv.get_json(
            "mspp_entitypermissions?$select=mspp_entitypermissionid,mspp_entityname,mspp_entitylogicalname,mspp_scope,"
            "mspp_read,mspp_create,mspp_write,mspp_delete,mspp_append,mspp_appendto"
            f"&$filter=_mspp_websiteid_value eq {website_id} and mspp_entitylogicalname eq '{escape_odata(logical)}' and mspp_scope eq {GLOBAL_SCOPE}&$top=1"
        )
        values = (data or {}).get("value") or []
        payload = {
            "mspp_entityname": logical,
            "mspp_entitylogicalname": logical,
            "mspp_scope": GLOBAL_SCOPE,
            "mspp_read": table["read"],
            "mspp_create": table["create"],
            "mspp_write": table["write"],
            "mspp_delete": table["delete"],
            "mspp_append": table["append"],
            "mspp_appendto": table["appendto"],
            "mspp_websiteid@odata.bind": f"/mspp_websites({website_id})",
        }
        if values:
            permission_id = values[0]["mspp_entitypermissionid"]
            current = values[0]
            updates = {
                key: value
                for key, value in payload.items()
                if key != "mspp_websiteid@odata.bind" and current.get(key) != value
            }
            if updates and execute:
                privilege_payload = {
                    "mspp_read": table["read"],
                    "mspp_create": table["create"],
                    "mspp_write": table["write"],
                    "mspp_delete": table["delete"],
                    "mspp_append": table["append"],
                    "mspp_appendto": table["appendto"],
                }
                response = self.dv.request("PATCH", f"mspp_entitypermissions({permission_id})", payload=privilege_payload)
                if response.status_code >= 400:
                    raise RuntimeError(f"PATCH table permission {logical} failed: HTTP {response.status_code} {self.deploy.safe_error(response)}")
                print(f"updated: table permission {logical}")
            elif updates:
                print(f"would update: table permission {logical}")
            else:
                print(f"exists: table permission {logical}")
        else:
            if not execute:
                print(f"would create: table permission {logical}")
                return None
            response = self.dv.post("mspp_entitypermissions", payload)
            permission_id = parse_guid_from_entity_id(response.headers.get("OData-EntityId", ""))
            print(f"created: table permission {logical}")
        self.ensure_permission_role(permission_id, role_id, execute)
        self.ensure_enhanced_permission_role(permission_id, role_id, execute)
        return permission_id

    def ensure_permission_role(self, permission_id: str, role_id: str, execute: bool) -> None:
        existing = self.dv.get_json(
            "mspp_entitypermission_webroleset?$select=mspp_entitypermission_webroleid"
            f"&$filter=mspp_entitypermissionid eq {permission_id} and mspp_webroleid eq {role_id}&$top=1"
        )
        if (existing or {}).get("value"):
            print("exists: permission Authenticated Users role link")
            return
        if not execute:
            print("would create: permission Authenticated Users role link")
            return
        payload = {"@odata.id": f"{self.dv.base}/mspp_webroles({role_id})"}
        response = self.dv.request("POST", f"mspp_entitypermissions({permission_id})/mspp_entitypermission_webrole/$ref", payload=payload)
        if response.status_code >= 400:
            message = self.deploy.safe_error(response)
            if "already" not in message.lower() and "duplicate" not in message.lower():
                raise RuntimeError(f"Associate permission role failed: HTTP {response.status_code} {message}")
        print("created: permission Authenticated Users role link")

    def ensure_enhanced_permission_role(self, permission_id: str, role_id: str, execute: bool) -> None:
        if self.enhanced_permission_role_exists(permission_id, role_id):
            print("exists: enhanced permission Authenticated Users component link")
            return
        if not execute:
            print("would create: enhanced permission Authenticated Users component link")
            return
        payload = {"@odata.id": f"{self.dv.base}/powerpagecomponents({role_id})"}
        response = self.dv.request("POST", f"powerpagecomponents({permission_id})/powerpagecomponent_powerpagecomponent/$ref", payload=payload)
        if response.status_code >= 400:
            message = self.deploy.safe_error(response)
            if "already" not in message.lower() and "duplicate" not in message.lower():
                raise RuntimeError(f"Associate enhanced permission role failed: HTTP {response.status_code} {message}")
        if not self.enhanced_permission_role_exists(permission_id, role_id):
            raise RuntimeError("Associate enhanced permission role did not create a readable component link")
        print("created: enhanced permission Authenticated Users component link")

    def enhanced_permission_role_exists(self, permission_id: str, role_id: str) -> bool:
        existing = self.dv.get_json(
            f"powerpagecomponents({permission_id})/powerpagecomponent_powerpagecomponent"
            "?$select=powerpagecomponentid&$top=50"
        )
        return any(row.get("powerpagecomponentid") == role_id for row in (existing or {}).get("value", []))

    def ensure_contact_role(self, contact_id: str | None, role_id: str, email: str, execute: bool) -> None:
        if not contact_id:
            print(f"missing: portal contact {email}; create/redeem an invitation before browser /_api testing")
            return
        existing = self.dv.get_json(
            f"powerpagecomponents({role_id})/powerpagecomponent_mspp_webrole_contact"
            "?$select=contactid&$top=100"
        )
        if any(row.get("contactid") == contact_id for row in (existing or {}).get("value", [])):
            print(f"exists: portal contact Authenticated Users role link {email}")
            return
        if not execute:
            print(f"would create: portal contact Authenticated Users role link {email}")
            return
        payload = {"@odata.id": f"{self.dv.base}/contacts({contact_id})"}
        response = self.dv.request("POST", f"powerpagecomponents({role_id})/powerpagecomponent_mspp_webrole_contact/$ref", payload=payload)
        if response.status_code >= 400:
            message = self.deploy.safe_error(response)
            if "already" not in message.lower() and "duplicate" not in message.lower():
                raise RuntimeError(f"Associate contact role failed: HTTP {response.status_code} {message}")
        print(f"created: portal contact Authenticated Users role link {email}")


def main() -> int:
    args = parse_args()
    deploy = load_deploy_module()
    settings = deploy.build_settings(argparse.Namespace(env_file=args.env_file, schema_dir=None, schema_file=None, execute=False, no_publish=False))
    env = deploy.load_env(Path(args.env_file).resolve())
    website_id = args.website_id or env.get("POWERPAGES_WEBSITE_ID") or None
    site_name = args.site_name or env.get("POWERPAGES_SITE_NAME") or "TACATDP Monitoring Tool"
    seed_user_email = args.portal_user_email or env.get("TACATDP_SEED_USER_EMAIL") or env.get("POWER_PLATFORM_ASSIGNMENT_USER_EMAIL") or "john.mduda@mshirikacorp.onmicrosoft.com"

    print("# TACATDP Power Pages Web API Configuration")
    print(f"Mode: {'execute' if args.execute else 'dry-run'}")
    print(f"Target: {settings.deploy_target}")
    print(f"Environment: {settings.environment_url}")
    print(f"Site: {site_name}")
    print(f"Tables: {len(WEB_API_TABLES)}")
    if settings.deploy_target.lower() != "dev":
        raise SystemExit(f"Refusing non-dev deployment target: {settings.deploy_target}")

    token = deploy.get_token(settings)
    client = PagesConfigClient(deploy, settings, token)
    resolved_website_id = client.find_website(website_id, site_name)
    role_id = client.find_authenticated_role(resolved_website_id)
    contact_id = client.find_contact_by_email(seed_user_email)
    print(f"Website ID: {resolved_website_id}")
    print(f"Authenticated Users role ID: {role_id}")
    print(f"Seed portal contact ID: {contact_id or 'missing'}")
    if not args.execute:
        print("Dry-run only. Re-run with --execute to configure Power Pages.")

    for table in WEB_API_TABLES:
        logical = table["logical"]
        client.ensure_site_setting(resolved_website_id, f"Webapi/{logical}/enabled", "true", args.execute)
        client.ensure_site_setting(resolved_website_id, f"Webapi/{logical}/fields", "*", args.execute)
        client.ensure_permission(resolved_website_id, role_id, table, args.execute)
    client.ensure_contact_role(contact_id, role_id, seed_user_email, args.execute)

    print("configuration complete" if args.execute else "dry-run complete")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
