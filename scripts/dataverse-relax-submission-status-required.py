#!/usr/bin/env python3
"""Relax Submissions.Status required level for the TACATDP MVP dev environment.

Why this exists:
- The MVP Dataverse schema originally made Submissions.Status application-required.
- Power Apps Studio repeatedly failed to bind the generic custom Status choice reliably.
- The MVP Canvas package must not reference Status; lifecycle is represented by StartedAt/SubmittedAt until the column is renamed/hardened.

This command is intentionally narrow:
- dev target only;
- explicit --execute required for writes;
- updates only mp_submission.mp_status RequiredLevel to None;
- no deletes, no data updates, no production support.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


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
    parser = argparse.ArgumentParser(description="Relax TACATDP Submissions.Status required level in dev Dataverse.")
    parser.add_argument("--env-file", default=".env", help="Environment file containing Power Platform settings.")
    parser.add_argument("--execute", action="store_true", help="Perform live metadata update. Without this flag only inspect current metadata.")
    parser.add_argument("--no-publish", action="store_true", help="Skip PublishAllXml after metadata update.")
    return parser.parse_args()


def strip_odata_metadata(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: strip_odata_metadata(v) for k, v in value.items() if not k.startswith("@odata.")}
    if isinstance(value, list):
        return [strip_odata_metadata(v) for v in value]
    return value


def main() -> int:
    args = parse_args()
    deploy = load_deploy_module()
    settings = deploy.build_settings(argparse.Namespace(env_file=args.env_file, schema_dir=None, execute=False, no_publish=args.no_publish))
    if settings.deploy_target.lower() != "dev":
        raise SystemExit(f"Refusing non-dev deployment target: {settings.deploy_target}")

    token = deploy.get_token(settings)
    dv = deploy.Dataverse(settings, token)
    table_logical = deploy.table_logical_name(settings.publisher_prefix, "Submissions")
    column_logical = deploy.column_logical_name(settings.publisher_prefix, "Status")
    path = (
        f"EntityDefinitions(LogicalName='{table_logical}')/"
        f"Attributes(LogicalName='{column_logical}')/"
        "Microsoft.Dynamics.CRM.PicklistAttributeMetadata"
    )
    metadata = dv.get_json(path)
    if not metadata:
        raise SystemExit(f"Missing Dataverse metadata for {table_logical}.{column_logical}")

    current = ((metadata.get("RequiredLevel") or {}).get("Value"))
    can_change = ((metadata.get("RequiredLevel") or {}).get("CanBeChanged"))
    print(f"Target: {settings.deploy_target}")
    print(f"Column: {table_logical}.{column_logical}")
    print(f"Current RequiredLevel: {current}")
    print(f"CanBeChanged: {can_change}")
    if current == "None":
        print("No update needed.")
        if args.execute and not args.no_publish:
            publish = dv.request("POST", "PublishAllXml", payload={})
            if publish.status_code >= 400:
                raise RuntimeError(f"PublishAllXml failed: HTTP {publish.status_code} {deploy.safe_error(publish)}")
            print("Published metadata changes.")
        return 0
    if can_change is False:
        raise SystemExit("RequiredLevel cannot be changed for this column according to metadata.")
    if not args.execute:
        print("Dry-run only. Re-run with --execute to set RequiredLevel to None.")
        return 0

    payload = strip_odata_metadata(metadata)
    payload["RequiredLevel"] = {
        "Value": "None",
        "CanBeChanged": True,
        "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings",
    }
    response = dv.request(
        "PUT",
        f"EntityDefinitions(LogicalName='{table_logical}')/Attributes({metadata['MetadataId']})/Microsoft.Dynamics.CRM.PicklistAttributeMetadata",
        payload=payload,
        solution_header=True,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"PUT required-level update failed: HTTP {response.status_code} {deploy.safe_error(response)}")
    print("Updated RequiredLevel to None.")
    if not args.no_publish:
        publish = dv.request("POST", "PublishAllXml", payload={})
        if publish.status_code >= 400:
            raise RuntimeError(f"PublishAllXml failed: HTTP {publish.status_code} {deploy.safe_error(publish)}")
        print("Published metadata changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
