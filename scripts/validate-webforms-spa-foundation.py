#!/usr/bin/env python3
"""Validate the TACATDP Power Pages WebForms SPA foundation slice."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPA = ROOT / "powerpages/webforms-spa"
REQUIRED_FILES = [
    "package.json",
    "index.html",
    "vite.config.ts",
    "tsconfig.json",
    "src/main.ts",
    "src/App.vue",
    "src/views/AssignedFormsView.vue",
    "src/powerpages-api/client.ts",
    "src/powerpages-api/types.ts",
    "src/offline/drafts.ts",
    "src/styles.css",
]
FORBIDDEN_PATTERNS = [
    r"client_secret",
    r"Authorization\s*:",
    r"Bearer\s+",
    r"login\.microsoftonline\.com",
    r"/api/data/v9\.2",
]
REQUIRED_API_STRINGS = [
    "/_api/mp_formassignments",
    "/_api/mp_formversions",
    "/_api/mp_forms",
    "__RequestVerificationToken",
    "getTokenDeferred",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    if not SPA.exists():
        fail(f"missing {SPA.relative_to(ROOT)}")

    for relative in REQUIRED_FILES:
        path = SPA / relative
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    package = json.loads((SPA / "package.json").read_text())
    if package.get("private") is not True:
        fail("webforms-spa package must be private")
    for script in ("dev", "build", "typecheck"):
        if script not in package.get("scripts", {}):
            fail(f"package.json missing script {script}")

    all_text = "\n".join(path.read_text() for path in SPA.rglob("*") if path.is_file())
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, all_text, flags=re.IGNORECASE):
            fail(f"forbidden browser credential/raw Dataverse pattern found: {pattern}")
    for expected in REQUIRED_API_STRINGS:
        if expected not in all_text:
            fail(f"missing required SPA API guardrail string: {expected}")
    if "@getodk/" in all_text:
        fail("ODK packages must not be imported before package review is accepted")
    if "indexedDB.open" not in all_text:
        fail("draft adapter must use explicit browser-local storage")
    if "Render form after ODK package review" not in all_text:
        fail("UI must make ODK runtime deferment explicit")

    print("WebForms SPA foundation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
