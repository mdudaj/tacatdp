#!/usr/bin/env python3
"""Dry-run preflight for TACATDP Dataverse MVP schema delivery.

This script validates local configuration and review-only MVP schema artifacts. It
does not authenticate, create tables, import data, publish apps, or write to Dataverse.
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
    "TACATDP_DATAVERSE_SCHEMA_FILE",
]

SERVICE_PRINCIPAL_REQUIRED_FOR_WRITE = [
    "POWER_PLATFORM_TENANT_ID",
    "POWER_PLATFORM_CLIENT_ID",
    "POWER_PLATFORM_CLIENT_SECRET",
]

EXPECTED_MVP_TABLES = {
    "Forms",
    "FormVersions",
    "Sections",
    "Questions",
    "Choices",
    "ValidationRules",
    "FormAssignments",
    "Submissions",
    "SubmissionAnswers",
    "SubmissionFiles",
}

REQUIRED_MVP_COLUMNS = {
    ("FormVersions", "Form"),
    ("Sections", "FormVersion"),
    ("Questions", "Section"),
    ("Choices", "Question"),
    ("ValidationRules", "Question"),
    ("FormAssignments", "FormVersion"),
    ("FormAssignments", "User"),
    ("FormAssignments", "UserEmail"),
    ("Submissions", "FormVersion"),
    ("Submissions", "AssignedUser"),
    ("Submissions", "Status"),
    ("SubmissionAnswers", "Submission"),
    ("SubmissionAnswers", "Question"),
    ("SubmissionAnswers", "ValueText"),
    ("SubmissionAnswers", "ValueNumber"),
    ("SubmissionAnswers", "ValueDecimal"),
    ("SubmissionAnswers", "ValueDate"),
    ("SubmissionAnswers", "ValueBoolean"),
    ("SubmissionAnswers", "ValueJson"),
    ("SubmissionFiles", "Submission"),
    ("SubmissionFiles", "Question"),
    ("SubmissionFiles", "File"),
}

PLACEHOLDER_VALUES = {"", "<required>", "changeme", "todo", "TODO"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate TACATDP Dataverse MVP schema delivery configuration without writing to an environment.")
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
    deploy_target = get_value(env, "TACATDP_DEPLOY_TARGET").lower()

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

    if deploy_target and deploy_target != "dev":
        issues.append(f"Only dev target is allowed for MVP schema setup; got TACATDP_DEPLOY_TARGET={deploy_target}")
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
        schema_file_value = get_value(env, "TACATDP_DATAVERSE_SCHEMA_FILE") or "schemas/dataverse/mvp-schema-definition.json"
        definition_path = repo_root / schema_file_value
        tables_path = schema_dir / "mvp-tables.json"
        columns_path = schema_dir / "mvp-columns.csv"
        renderer_path = schema_dir / "form-renderer-contract.json"
        for artifact in [definition_path]:
            if not artifact.exists():
                issues.append(f"Missing schema definition artifact: {artifact}")

        legacy_mvp_mode = definition_path.name == "mvp-schema-definition.json"
        for artifact in ([tables_path, columns_path, renderer_path] if legacy_mvp_mode else []):
            if not artifact.exists():
                issues.append(f"Missing MVP schema artifact: {artifact}")

        if legacy_mvp_mode and tables_path.exists():
            data = json.loads(tables_path.read_text(encoding="utf-8"))
            tables = {row.get("logical_name") for row in data.get("tables", [])}
            missing = sorted(EXPECTED_MVP_TABLES - tables)
            extra = sorted(tables - EXPECTED_MVP_TABLES)
            if missing:
                issues.append("Missing MVP tables: " + ", ".join(missing))
            if extra:
                issues.append("Unexpected non-MVP tables in mvp-tables.json: " + ", ".join(extra))

        if legacy_mvp_mode and columns_path.exists():
            rows = read_csv(columns_path)
            columns = {(row.get("table") or "", row.get("column") or "") for row in rows}
            missing = sorted(REQUIRED_MVP_COLUMNS - columns)
            if missing:
                issues.append("Missing MVP columns: " + ", ".join(f"{table}.{column}" for table, column in missing))
            column_tables = {table for table, _ in columns}
            extra_tables = sorted(column_tables - EXPECTED_MVP_TABLES)
            if extra_tables:
                issues.append("mvp-columns.csv includes non-MVP tables: " + ", ".join(extra_tables))

        if legacy_mvp_mode and renderer_path.exists():
            json.loads(renderer_path.read_text(encoding="utf-8"))

        if definition_path.exists():
            definition = json.loads(definition_path.read_text(encoding="utf-8"))
            definition_tables = {row.get("name") for row in definition.get("tables", [])}
            if legacy_mvp_mode:
                missing_definition = sorted(EXPECTED_MVP_TABLES - definition_tables)
                if missing_definition:
                    issues.append("Missing MVP tables in mvp-schema-definition.json: " + ", ".join(missing_definition))
            elif not definition_tables:
                issues.append("Schema definition has no tables: " + str(definition_path))

    if shutil.which("pac") is None:
        warnings.append("Power Platform CLI 'pac' was not found on PATH; install/verify it before live deployment.")

    plan.extend([
        "No Dataverse write will be performed by this preflight.",
        "Run scripts/dataverse-schema-plan.py to review table/column/relationship operations.",
        "Use PAC to verify auth and solution state.",
        "Create tables and columns through approved Dataverse Web API metadata operations only after review.",
        "Seed one published form and one assignment after schema exists.",
        "Bind Canvas app only after dev schema and seed data are reviewed.",
    ])

    result = {
        "status": "failed" if issues else "passed",
        "env_file": str(env_file),
        "schema_dir": str(schema_dir),
        "schema_file": str(definition_path),
        "dry_run": dry_run,
        "allow_environment_write": allow_write,
        "issues": issues,
        "warnings": warnings,
        "plan": plan,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("# TACATDP Dataverse MVP Schema Preflight")
        print(f"Status: {result['status']}")
        print(f"Env file: {env_file}")
        print(f"Schema dir: {schema_dir}")
        print(f"Schema file: {definition_path}")
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
