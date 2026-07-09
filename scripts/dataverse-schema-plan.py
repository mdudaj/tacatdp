#!/usr/bin/env python3
"""Generate a dry-run Dataverse metadata operation plan for a TACATDP schema file.

No network calls are made and no environment writes are performed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a reviewable Dataverse schema operation plan. No network calls are made.")
    parser.add_argument("--schema-dir", default="schemas/dataverse", help="Directory containing mvp-schema-definition.json when --schema-file is omitted.")
    parser.add_argument("--schema-file", default=None, help="Machine-readable schema definition JSON. Defaults to <schema-dir>/mvp-schema-definition.json.")
    parser.add_argument("--solution", default="$POWER_PLATFORM_SOLUTION_UNIQUE_NAME", help="Solution unique name to include in the planned Web API header.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def load_schema(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    path = Path(args.schema_file) if args.schema_file else Path(args.schema_dir) / "mvp-schema-definition.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    schema_path, schema = load_schema(args)
    operations: list[dict[str, Any]] = []

    for table in schema.get("tables", []):
        table_name = table["name"]
        operations.append({
            "operation": "create_table",
            "target": table_name,
            "primary_name_column": table.get("primary_name_column"),
            "web_api": "POST /api/data/v9.2/EntityDefinitions",
            "solution_header": args.solution,
            "notes": table.get("purpose", ""),
        })
        primary = table.get("primary_name_column")
        for column in table.get("columns", []):
            if column.get("name") == primary:
                continue
            operations.append({
                "operation": "create_column" if not str(column.get("type", "")).startswith("Lookup:") else "create_lookup_relationship",
                "target": f"{table_name}.{column['name']}",
                "type": column.get("type"),
                "required": bool(column.get("required")),
                "web_api": "POST /api/data/v9.2/EntityDefinitions(...)/Attributes" if not str(column.get("type", "")).startswith("Lookup:") else "POST /api/data/v9.2/RelationshipDefinitions",
                "solution_header": args.solution,
                "notes": column.get("notes", ""),
            })

    for rel in schema.get("relationships", []):
        operations.append({
            "operation": "create_relationship",
            "target": f"{rel['referenced_table']} -> {rel['referencing_table']}.{rel['lookup_column']}",
            "referenced_table": rel["referenced_table"],
            "referencing_table": rel["referencing_table"],
            "lookup_column": rel["lookup_column"],
            "required": bool(rel.get("required")),
            "web_api": "POST /api/data/v9.2/RelationshipDefinitions",
            "solution_header": args.solution,
            "notes": rel.get("notes", ""),
        })

    result = {
        "schema_file": str(schema_path),
        "schema_name": schema.get("schema_name"),
        "solution_header": args.solution,
        "operation_count": len(operations),
        "tables": [row["name"] for row in schema.get("tables", [])],
        "operations": operations,
        "writes_performed": False,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("# TACATDP Dataverse Schema Operation Plan")
        print(f"Schema file: {schema_path}")
        print(f"Schema name: {schema.get('schema_name', '')}")
        print(f"Solution header: MSCRM.SolutionUniqueName={args.solution}")
        print("Writes performed: false")
        print(f"Operation count: {len(operations)}")
        for table in schema.get("tables", []):
            print(f"\n## {table['name']}")
            print(f"- Create table: {table.get('purpose', '')}")
            for column in table.get("columns", []):
                required = " required" if column.get("required") else ""
                print(f"- Create column/lookup: {column['name']} ({column['type']}{required})")
        if schema.get("relationships"):
            print("\n## Relationships")
            for relationship in schema["relationships"]:
                print(f"- Create relationship: {relationship['referenced_table']} -> {relationship['referencing_table']}.{relationship['lookup_column']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
