#!/usr/bin/env python3
"""Dry-run preflight for TACATDP Dataverse dev deployment.

This script validates local configuration and review-only schema artifacts. It does
not authenticate, create tables, import data, publish apps, or write to Dataverse.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
from pathlib import Path

REQUIRED_ALWAYS = [
    "PAC_AUTH_NAME",
    "POWER_PLATFORM_CLOUD",
    "POWER_PLATFORM_AUTH_MODE",
    "POWER_PLATFORM_SOLUTION_UNIQUE_NAME",
    "POWER_PLATFORM_PUBLISHER_PREFIX",
    "TACATDP_DEPLOY_TARGET",
    "TACATDP_SCHEMA_SCOPE",
    "TACATDP_DRY_RUN",
    "TACATDP_ALLOW_ENVIRONMENT_WRITE",
    "TACATDP_DATAVERSE_SCHEMA_DIR",
]

SERVICE_PRINCIPAL_REQUIRED_FOR_WRITE = [
    "POWER_PLATFORM_TENANT_ID",
    "POWER_PLATFORM_CLIENT_ID",
    "POWER_PLATFORM_CLIENT_SECRET",
]

EXPECTED_ARTIFACTS = {
    "platform-tables.json": None,
    "platform-columns.csv": 186,
    "platform-relationships.csv": 48,
    "platform-alternate-keys.csv": 22,
    "form-renderer-contract.json": None,
    "import-order.md": None,
    "tacatdp-field-definitions.csv": 292,
    "tacatdp-vocabulary-terms.csv": 5190,
    "tacatdp-village-reference.csv": 66297,
}

REQUIRED_PROTOTYPE_TABLES = {
    "mp_Project",
    "mp_Instrument",
    "mp_InstrumentVersion",
    "mp_GroupDefinition",
    "mp_FieldDefinition",
    "mp_FieldRule",
    "mp_VocabularyScheme",
    "mp_VocabularyTerm",
    "mp_FieldVocabularyBinding",
    "mp_VillageReference",
    "mp_Submission",
    "mp_GroupInstance",
    "mp_AnswerValue",
    "mp_MultiSelectAnswer",
}

REQUIRED_ANSWERVALUE_LOOKUPS = {
    "mp_vocabularyterm",
    "mp_villagereference",
}

PLACEHOLDER_VALUES = {"", "<required>", "changeme", "todo", "TODO"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate TACATDP Dataverse deployment configuration without writing to an environment.")
    parser.add_argument("--env-file", default=".env", help="Local env file to read. Defaults to .env.")
    parser.add_argument("--repo-root", default=".", help="TACATDP repo root. Defaults to current directory.")
    parser.add_argument("--allow-placeholders", action="store_true", help="Allow blank/example values; useful for validating .env.example shape.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get_value(values: dict[str, str], key: str) -> str:
    return values.get(key) or os.environ.get(key, "")


def is_truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def is_placeholder(value: str) -> bool:
    return value.strip() in PLACEHOLDER_VALUES or value.strip().startswith("<")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    env_file = (repo_root / args.env_file).resolve()
    env = load_env(env_file)
    issues: list[str] = []
    warnings: list[str] = []
    plan: list[str] = []

    if not env_file.exists():
        issues.append(f"Env file not found: {env_file}")

    allow_write = is_truthy(get_value(env, "TACATDP_ALLOW_ENVIRONMENT_WRITE"))
    dry_run = is_truthy(get_value(env, "TACATDP_DRY_RUN"))
    auth_mode = get_value(env, "POWER_PLATFORM_AUTH_MODE") or "servicePrincipal"

    for key in REQUIRED_ALWAYS:
        value = get_value(env, key)
        if args.allow_placeholders:
            if key not in env and key not in os.environ:
                issues.append(f"Missing required configuration key: {key}")
        elif not value or is_placeholder(value):
            issues.append(f"Missing required configuration: {key}")

    env_target_keys = ["POWER_PLATFORM_ENVIRONMENT_ID", "POWER_PLATFORM_ENVIRONMENT_URL"]
    if args.allow_placeholders:
        if not any(key in env or key in os.environ for key in env_target_keys):
            issues.append("Missing required configuration key: POWER_PLATFORM_ENVIRONMENT_ID or POWER_PLATFORM_ENVIRONMENT_URL")
    elif not any(get_value(env, key) and not is_placeholder(get_value(env, key)) for key in env_target_keys):
        issues.append("Missing required configuration: POWER_PLATFORM_ENVIRONMENT_ID or POWER_PLATFORM_ENVIRONMENT_URL")

    if allow_write and dry_run:
        issues.append("TACATDP_ALLOW_ENVIRONMENT_WRITE=true conflicts with TACATDP_DRY_RUN=true")
    if allow_write and auth_mode == "servicePrincipal":
        for key in SERVICE_PRINCIPAL_REQUIRED_FOR_WRITE:
            value = get_value(env, key)
            if not value or is_placeholder(value):
                issues.append(f"Missing service-principal write configuration: {key}")
    if allow_write:
        issues.append("Environment writes are intentionally not implemented by this dry-run preflight. Use a separate reviewed deployment command.")

    schema_dir_value = get_value(env, "TACATDP_DATAVERSE_SCHEMA_DIR") or "schemas/dataverse"
    schema_dir = repo_root / schema_dir_value
    if not schema_dir.exists():
        issues.append(f"Schema directory not found: {schema_dir}")
    else:
        for name, expected_rows in EXPECTED_ARTIFACTS.items():
            artifact = schema_dir / name
            if not artifact.exists():
                issues.append(f"Missing schema artifact: {artifact}")
                continue
            if name.endswith(".csv") and expected_rows is not None:
                rows = read_csv(artifact)
                if len(rows) != expected_rows:
                    issues.append(f"Unexpected row count for {name}: expected {expected_rows}, got {len(rows)}")
            elif name.endswith(".json"):
                json.loads(artifact.read_text(encoding="utf-8"))

        tables_path = schema_dir / "platform-tables.json"
        if tables_path.exists():
            data = json.loads(tables_path.read_text(encoding="utf-8"))
            tables = {row.get("logical_name") for row in data.get("tables", [])}
            missing = sorted(REQUIRED_PROTOTYPE_TABLES - tables)
            if missing:
                issues.append("Missing prototype tables: " + ", ".join(missing))

        columns_path = schema_dir / "platform-columns.csv"
        if columns_path.exists():
            columns = read_csv(columns_path)
            answer_columns = {row["column_logical_name"] for row in columns if row["table_logical_name"] == "mp_AnswerValue"}
            missing = sorted(REQUIRED_ANSWERVALUE_LOOKUPS - answer_columns)
            if missing:
                issues.append("Missing mp_AnswerValue lookup columns: " + ", ".join(missing))

        rels_path = schema_dir / "platform-relationships.csv"
        if rels_path.exists():
            rels = read_csv(rels_path)
            rel_keys = {(row["child_table"], row["parent_table"], row["lookup_column_logical_name"]) for row in rels}
            for rel in [
                ("mp_AnswerValue", "mp_VocabularyTerm", "mp_vocabularyterm"),
                ("mp_AnswerValue", "mp_VillageReference", "mp_villagereference"),
            ]:
                if rel not in rel_keys:
                    issues.append("Missing relationship: " + " -> ".join(rel))

    if shutil.which("pac") is None:
        warnings.append("Power Platform CLI 'pac' was not found on PATH; install/verify it before live deployment.")

    plan.extend([
        "No Dataverse write will be performed by this preflight.",
        "Create or select dev environment after explicit approval.",
        "Create/verify solution and publisher prefix.",
        "Create reduced prototype table set first.",
        "Create relationships and alternate keys after referenced columns exist.",
        "Seed project, instrument, version, groups, fields, vocabulary, and village reference data.",
        "Bind Canvas app only after dev schema and seed data are reviewed.",
    ])

    result = {
        "status": "failed" if issues else "passed",
        "env_file": str(env_file),
        "schema_dir": str(schema_dir),
        "dry_run": dry_run,
        "allow_environment_write": allow_write,
        "issues": issues,
        "warnings": warnings,
        "plan": plan,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("# TACATDP Dataverse Deployment Preflight")
        print(f"Status: {result['status']}")
        print(f"Env file: {env_file}")
        print(f"Schema dir: {schema_dir}")
        print(f"Dry run: {dry_run}")
        print(f"Allow environment write: {allow_write}")
        print("\n## Issues")
        print("- None" if not issues else "\n".join(f"- {issue}" for issue in issues))
        print("\n## Warnings")
        print("- None" if not warnings else "\n".join(f"- {warning}" for warning in warnings))
        print("\n## Dry-Run Plan")
        print("\n".join(f"- {item}" for item in plan))

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
