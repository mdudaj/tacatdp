#!/usr/bin/env python3
"""Validate the TACATDP Power Pages WebForms SPA foundation slice."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPA = ROOT / "powerpages/webforms-spa"
SITE_SOURCE = ROOT / "powerpages/tacatdp-monitoring-tool/.powerpages-site"
SITE_UPLOAD = ROOT / "powerpages/tacatdp-monitoring-tool-upload/tacatdp-monitoring-tool"
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
    "src/dev/assignedForms.ts",
    "src/vite-env.d.ts",
    "src/types/getodk-web-forms.d.ts",
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
    "/_api/mp_formattachments",
    "/_api/mp_submissions",
    "/_api/mp_submissionversions",
    "/_api/mp_submissionattachments",
    "__RequestVerificationToken",
    "getTokenDeferred",
    "mp_xformsubmissionxml",
    "mp_submissionjson",
    "mp_Submission@odata.bind",
    "mp_SubmissionVersion@odata.bind",
    "mp_file",
    "x-ms-file-name",
    "dataverse-file:",
    "/mp_file/$value",
    "formVersionId",
]
TEXT_SCAN_FILES = [
    "package.json",
    "index.html",
    "vite.config.ts",
    "tsconfig.json",
    "src/main.ts",
    "src/App.vue",
    "src/views/AssignedFormsView.vue",
    "src/powerpages-api/client.ts",
    "src/powerpages-api/types.ts",
    "src/dev/assignedForms.ts",
    "src/vite-env.d.ts",
    "src/types/getodk-web-forms.d.ts",
    "src/offline/drafts.ts",
    "src/styles.css",
]
SEED_SCRIPT = ROOT / "scripts/dataverse-seed-odk-mvp-form.py"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def validate_seed_xform_body_refs() -> None:
    namespace: dict[str, object] = {}
    exec(SEED_SCRIPT.read_text(), namespace)
    xform = str(namespace["RICH_TACATDP_XFORM"])
    root = ET.fromstring(xform)
    body = root.find("{http://www.w3.org/1999/xhtml}body")
    if body is None:
        fail("seeded XForm is missing h:body")

    refs: dict[str, str] = {}
    duplicates: list[str] = []
    for element in body.iter():
        ref = element.attrib.get("ref")
        if not ref:
            continue
        tag = element.tag.rsplit("}", 1)[-1]
        if ref in refs:
            duplicates.append(ref)
        refs[ref] = tag

    if duplicates:
        fail(f"seeded XForm body has duplicate refs rejected by ODK Web Forms: {', '.join(sorted(set(duplicates)))}")


def validate_odk_style_isolation() -> None:
    css = (SPA / "src/styles.css").read_text()
    view = (SPA / "src/views/AssignedFormsView.vue").read_text()
    forbidden_css = [
        r"(?m)^button\s*\{",
        r"(?m)^\*\s*\{",
        r"\.runtime-panel\s+:where",
        r"\.runtime-panel\s+button",
        r"\.runtime-panel\s+input",
        r"\.runtime-panel\s+label",
        r"\.runtime-panel\s+select",
        r"\.runtime-panel\s+textarea",
    ]
    for pattern in forbidden_css:
        if re.search(pattern, css):
            fail(f"host shell CSS must not leak into ODK renderer controls: {pattern}")
    if "odk-runtime-host" not in css or "odk-runtime-host" not in view:
        fail("ODK renderer must be mounted in a dedicated odk-runtime-host boundary")


def validate_powerpages_hosting() -> None:
    for site in (SITE_SOURCE, SITE_UPLOAD):
        if not site.exists():
            fail(f"missing Power Pages package {site.relative_to(ROOT)}")

        template = site / "page-templates/Monitoring-Tool-SPA.pagetemplate.yml"
        home = site / "web-pages/home/Home.webpage.copy.html"
        home_content_candidates = (
            site / "web-pages/home/content-pages/en-US/Home.webpage.copy.html",
            site / "web-pages/home/content-pages/Home.en-US.webpage.copy.html",
        )
        footer = site / "web-templates/footer/Footer.webtemplate.source.html"
        footer_snippet_candidates = (
            site / "content-snippets/footer/en-US/Footer.contentsnippet.value.html",
            site / "content-snippets/footer/Footer.en-US.contentsnippet.value.html",
        )
        if not template.exists():
            fail(f"missing {template.relative_to(ROOT)}")
        if not home.exists():
            fail(f"missing {home.relative_to(ROOT)}")
        if not footer.exists():
            fail(f"missing {footer.relative_to(ROOT)}")
        home_content = next((path for path in home_content_candidates if path.exists()), None)
        if home_content is None:
            fail(f"missing Home language content page under {site.relative_to(ROOT)}")

        template_text = template.read_text()
        home_texts = {
            home.relative_to(ROOT): home.read_text(),
            home_content.relative_to(ROOT): home_content.read_text(),
        }
        footer_text = footer.read_text()
        footer_snippet = next((path for path in footer_snippet_candidates if path.exists()), None)
        if footer_snippet is None:
            fail(f"missing footer content snippet under {site.relative_to(ROOT)}")
        footer_snippet_text = footer_snippet.read_text()
        if "usewebsiteheaderandfooter: true" not in template_text and "adx_usewebsiteheaderandfooter: true" not in template_text:
            fail("Monitoring Tool SPA page template must use the Power Pages header/footer runtime so shell.getTokenDeferred is available")
        for home_path, home_text in home_texts.items():
            for forbidden in ("<!doctype", "<html", "<head", "<body"):
                if forbidden in home_text.lower():
                    fail(f"Monitoring Tool Home copy must be a Power Pages page fragment, not a full HTML document: {home_path}")
            for required in ("__TACATDP_POWERPAGES__", "index-3K1-wZQo.mjs", "index-D2gciYo5.css", "runtime-error-focus-20260712-001"):
                if required not in home_text:
                    fail(f"Monitoring Tool Home copy missing required hosted asset/bootstrap {required}: {home_path}")
        for required in (
            "mt-site-footer",
            "mt-site-footer__inner",
            "role=\"contentinfo\"",
            "(c) CRDB",
            "now | date: 'yyyy'",
            "width: min(1180px, 100%)",
            "justify-content: flex-end",
        ):
            if required not in footer_text:
                fail(f"Power Pages Footer shell template missing required Monitoring Tool footer contract: {required}")
        for forbidden in ("Copyright ©", "All rights reserved", "(c) CRDB"):
            if forbidden in footer_snippet_text:
                fail(f"Power Pages default footer content snippet must not render duplicate footer text: {footer_snippet.relative_to(ROOT)}")


def validate_powerpages_session_contract() -> None:
    view = (SPA / "src/views/AssignedFormsView.vue").read_text()
    client = (SPA / "src/powerpages-api/client.ts").read_text()
    drafts = (SPA / "src/offline/drafts.ts").read_text()
    if '<header class="app-header">' in view:
        fail("SPA must not render a second CRDB/session header; use the Power Pages Header template for visible chrome")
    if "app-footer" in view:
        fail("SPA must not render the copyright footer; use the Power Pages Footer shell template")
    for required in (
        "getSignedInUserEmail",
        "$filter=mp_useremail eq",
        "listSavedSubmissions",
    ):
        if required not in client:
            fail(f"Power Pages assignment API must filter new-form assignments by the signed-in email: missing {required}")
    saved_method = re.search(r"async listSavedSubmissions\(\).*?\n  async getSubmissionFormContext", client, flags=re.S)
    if not saved_method:
        fail("Power Pages API client must keep an explicit listSavedSubmissions method")
    saved_body = saved_method.group(0)
    if "mp_useremail eq" in saved_body:
        fail("Saved submitted records must not be filtered to the signed-in user; authenticated users see all submitted records")
    for required in (
        "mp_lifecyclestatus eq",
        "mp_useremail",
        "getLatestSubmissionVersionByInstanceId",
        "mp_xformsubmissionxml",
        "parseSubmissionMetadata",
        "getSubmissionFormContext",
        "getLatestSubmissionXml",
        "updateSubmission",
        "normalizeInstanceId",
        "resolveInstanceName",
        "Customer_ID",
        "Customer_Name",
        "existingSubmission",
        "displayName",
    ):
        if required not in client:
            fail(f"Global saved-record/edit API path missing required guardrail: {required}")
    for required in (
        "runtime-error-focus-20260712-001",
        "type AppView = 'projects' | 'records' | 'runner'",
        "Add new",
        "Saved",
        "Drafts",
        "Edit",
        "recordSearch",
        "Search records",
        "filteredSavedSubmissions",
        "openSavedSubmission",
        ":edit-instance",
        "@lucide/vue",
        "ArrowLeft",
        "Pencil",
        "Search",
        "RefreshCw",
        "FilePenLine",
        "Editable local draft save and restore is not enabled yet",
        "submitting",
        "postSubmitMessage",
        "postSubmitTone",
        "Submitting record",
        "Saving to Dataverse",
        "/CRDB_Bank_PLC.svg",
        "visiblePageNumbers",
        "activePageStart",
        "activePageEnd",
        "setActivePage",
        "clampActivePage",
        '<nav class="pagination-bar"',
        "Showing {{ activePageStart }}-{{ activePageEnd }} of {{ activeRecordCount }}",
        "Page {{ activeRecordPage }} of {{ activeTotalPages }}",
        "pagination-button--active",
        "activeView.value = selectedProject.value ? 'records' : 'projects'",
        "activeRecordTab.value = 'saved'",
        "existingSubmission: selectedEditSubmission.value",
        "submission.displayName || submission.instanceId",
    ):
        if required not in view:
            fail(f"Monitoring Tool CRUD workspace shell missing required text or state: {required}")
    handle_loaded = re.search(r"function handleFormLoaded\(\)\s*\{(?P<body>.*?)\nasync function handleSubmit", view, flags=re.S)
    if not handle_loaded:
        fail("Monitoring Tool runner must keep an explicit handleFormLoaded function")
    if "draftStore.save" in handle_loaded.group("body"):
        fail("handleFormLoaded must not create local drafts; drafts require restorable ODK instance state")
    if "Local runtime marker saved" in view or "Open a form once to create a local draft marker" in view:
        fail("Monitoring Tool must not present runtime-load markers as local drafts")
    for glyph in ('aria-hidden="true">></span>', 'aria-hidden="true"><</span>', 'aria-hidden="true">R</span>', 'aria-hidden="true">S</span>', 'aria-hidden="true">D</span>', 'aria-hidden="true">+</span>'):
        if glyph in view:
            fail(f"Monitoring Tool actions must use icon components, not text glyphs: {glyph}")
    if "RuntimeLoaded" not in drafts or "isRestorableDraft" not in drafts:
        fail("Draft store must filter non-restorable runtime-load markers")


def main() -> int:
    if not SPA.exists():
        fail(f"missing {SPA.relative_to(ROOT)}")
    if not SEED_SCRIPT.exists():
        fail(f"missing {SEED_SCRIPT.relative_to(ROOT)}")

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
    dependencies = package.get("dependencies", {})
    for dependency in ("@getodk/web-forms", "@getodk/xforms-engine", "@lucide/vue"):
        if dependency not in dependencies:
            fail(f"package.json missing reviewed ODK dependency {dependency}")

    all_text = "\n".join((SPA / relative).read_text() for relative in TEXT_SCAN_FILES)
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, all_text, flags=re.IGNORECASE):
            fail(f"forbidden browser credential/raw Dataverse pattern found: {pattern}")
    for expected in REQUIRED_API_STRINGS:
        if expected not in all_text:
            fail(f"missing required SPA API guardrail string: {expected}")
    if "indexedDB.open" not in all_text:
        fail("draft adapter must use explicit browser-local storage")
    for expected in (
        "OdkWebForm",
        "webFormsPlugin",
        "@getodk/web-forms",
        "@loaded",
        "@submit",
        "Initializing ODK Web Forms runtime",
        "Submitting to Dataverse",
        "POST_SUBMIT__NEW_INSTANCE",
        "xml_submission_file",
        "preventPowerPagesFormSubmit",
        "preventRuntimeButtonDefault",
        "document.addEventListener('submit'",
        "document.addEventListener('click'",
        "runtime-error-focus-20260712-001",
        "Last runtime click",
        "Last ODK submit event",
        "Last Dataverse write",
        "attachmentBinaryUploadCount",
        "attachmentWarnings",
        "relabelOdkSubmitButton",
        "MutationObserver",
        "aria-label', 'Submit'",
        "focusFirstRuntimeError",
        "focusFirstRuntimeErrorAfterRender",
        "ODK validation is not ready",
        "Please fix the highlighted form fields before submitting",
        "aria-invalid=\"true\"",
        ".p-invalid",
        ":focus-visible",
        ".odk-runtime-host .powered-by-wrapper",
        ".odk-runtime-host .footer",
        ".odk-runtime-host .form-wrapper",
        ".submit-overlay",
        ".submit-progress-panel",
        ".loading-dots",
    ):
        if expected not in all_text:
            fail(f"missing required ODK runtime proof string: {expected}")
    validate_seed_xform_body_refs()
    validate_odk_style_isolation()
    validate_powerpages_hosting()
    validate_powerpages_session_contract()

    print("WebForms SPA runtime foundation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
