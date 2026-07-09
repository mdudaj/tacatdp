#!/usr/bin/env python3
"""Validate the TACATDP Power Pages /_api smoke-test source slice."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_DIR = ROOT / "powerpages/tacatdp-monitoring-tool/.powerpages-site/web-pages/api-smoke"
REQUIRED_SUFFIXES = [
    ".webpage.yml",
    ".webpage.copy.html",
    ".webpage.custom_css.css",
    ".webpage.custom_javascript.js",
    ".webpage.summary.html",
]
REQUIRED_ENTITY_SETS = [
    "mp_formassignments",
    "mp_formversions",
    "mp_forms",
]
FORBIDDEN_PATTERNS = [
    r"client_secret",
    r"Authorization\s*:",
    r"Bearer\s+",
    r"login\.microsoftonline\.com",
    r"api/data/v9\.2",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def file_with_suffix(suffix: str) -> Path:
    matches = sorted(PAGE_DIR.glob(f"*{suffix}"))
    if not matches:
        fail(f"missing api-smoke file ending in {suffix}")
    if len(matches) > 1:
        fail(f"multiple api-smoke files ending in {suffix}: {', '.join(p.name for p in matches)}")
    return matches[0]


def check_javascript_syntax(js: str) -> None:
    node = shutil.which("node")
    if not node:
        print("WARN: node not found; skipped JavaScript syntax check")
        return
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
        handle.write(js)
        temp_path = Path(handle.name)
    try:
        result = subprocess.run([node, "--check", str(temp_path)], text=True, capture_output=True, check=False)
        if result.returncode != 0:
            fail("JavaScript syntax check failed: " + (result.stderr or result.stdout).strip())
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    if not PAGE_DIR.exists():
        fail(f"missing {PAGE_DIR.relative_to(ROOT)}")
    for suffix in REQUIRED_SUFFIXES:
        file_with_suffix(suffix)

    yml = file_with_suffix(".webpage.yml").read_text()
    js = file_with_suffix(".webpage.custom_javascript.js").read_text()
    html = file_with_suffix(".webpage.copy.html").read_text()

    if "partialurl: api-smoke" not in yml:
        fail("smoke page route must be /api-smoke")
    if "hiddenfromsitemap: true" not in yml:
        fail("smoke page must remain hidden from sitemap")
    if "/_api/" not in js:
        fail("smoke page JavaScript must call the Power Pages Web API /_api route")
    for entity_set in REQUIRED_ENTITY_SETS:
        if entity_set not in js:
            fail(f"missing EntitySetName reference {entity_set}")
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, js, flags=re.IGNORECASE) or re.search(pattern, html, flags=re.IGNORECASE):
            fail(f"forbidden browser credential/raw Dataverse pattern found: {pattern}")
    if "aria-live" not in html or 'role="status"' not in html:
        fail("smoke page must expose status updates accessibly")
    if 'class="tacatdp-smoke__record"' not in js:
        fail("smoke page JavaScript must safely quote rendered record markup")
    check_javascript_syntax(js)

    print("Power Pages API smoke source validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
