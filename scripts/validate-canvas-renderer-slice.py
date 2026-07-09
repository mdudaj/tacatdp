#!/usr/bin/env python3
"""Validate the TACATDP July 7 Canvas renderer slice artifacts."""
from __future__ import annotations

import re
import sys
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "app-src-metadata-renderer/README.md",
    "app-src-metadata-renderer/Src/App.pa.yaml",
    "app-src-metadata-renderer/Src/AssignedFormsScreen.pa.yaml",
    "app-src-metadata-renderer/Src/HistoryScreen.pa.yaml",
    "app-src-metadata-renderer/Src/RunnerScreen.pa.yaml",
    "app-src-metadata-renderer/Src/ReviewScreen.pa.yaml",
    "app-src-metadata-renderer/Src/AttachmentScreen.pa.yaml",
    "app-src-metadata-renderer/Src/_EditorState.pa.yaml",
    "docs/canvas-renderer-mvp/formula-catalog.md",
    "docs/canvas-renderer-mvp/implementation-ready-slice.md",
]

REQUIRED_MARKERS = {
    "app-src-metadata-renderer/Src/App.pa.yaml": [
        "StartScreen: '=AssignedFormsScreen'",
        "Set(gblUserEmail, Lower(User().Email))",
        "RemoveIf(colPendingAnswers, true)",
    ],
    "app-src-metadata-renderer/Src/AssignedFormsScreen.pa.yaml": [
        "Filter(FormAssignments",
        "Filter(FormAssignments, UserEmail = gblUserEmail)",
        "AssignedFormsStatus",
        "OpenAssignedFormButton",
        "No assigned forms available.",
        "Signed in as",
        "FormVersion.Form.Name",
        "VersionCode",
        "Navigate(HistoryScreen",
    ],
    "app-src-metadata-renderer/Src/HistoryScreen.pa.yaml": [
        "Filter(Submissions",
        "Patch(Submissions, Defaults(Submissions)",
        "Navigate(RunnerScreen",
        "HistoryStatus",
        "OpenLatestSubmissionButton",
    ],
    "app-src-metadata-renderer/Src/RunnerScreen.pa.yaml": [
        "QuestionsGallery",
        "FarmerNameInput",
        "VisitDateInput",
        "PrimaryCropInput",
        "SupportNeededInput",
        "Patch(SubmissionAnswers",
        "QuestionCode",
        "ReviewButton",
        "RunnerNextButton",
        "Navigate(ReviewScreen",
        "Location.Latitude",
        "DisplayMode: '=If(IsBlank(gblSubmission), DisplayMode.Disabled, DisplayMode.Edit)'",
    ],
    "app-src-metadata-renderer/Src/ReviewScreen.pa.yaml": [
        "ReviewSubmitButton",
        "SubmittedAt: Now()",
        "gblReviewFarmerName",
        "Navigate(HistoryScreen",
    ],
    "app-src-metadata-renderer/Src/AttachmentScreen.pa.yaml": [
        "SubmissionFiles",
        "Attachments control must remain inside a form",
    ],
    "docs/canvas-renderer-mvp/formula-catalog.md": [
        "Do not add a custom login screen",
        "Assigned forms gallery",
        "Question renderer bindings",
        "Save draft",
        "Submit",
        "Display mode",
    ],
}

DEFERRED_TERMS_ALLOWED_ONLY_IN_DOCS = [
    "Full XLSForm parser",
    "repeat groups",
    "offline-first sync",
    "barcode",
]

SECRET_PATTERNS = [
    re.compile(r"client[_-]?secret\s*=", re.IGNORECASE),
    re.compile(r"authorization:\s*bearer", re.IGNORECASE),
    re.compile(r"password\s*=", re.IGNORECASE),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def validate_packed_msapp() -> None:
    msapp = ROOT / "artifacts" / "TACATDP Metadata Renderer - MVP v16.msapp"
    if not msapp.exists():
        fail(f"missing packed MVP app: {msapp.relative_to(ROOT)}")
    with zipfile.ZipFile(msapp) as zf:
        names = set(zf.namelist())
        for required in [
            "Src/App.pa.yaml",
            "Src/AssignedFormsScreen.pa.yaml",
            "Src/HistoryScreen.pa.yaml",
            "Src/RunnerScreen.pa.yaml",
            "Src/ReviewScreen.pa.yaml",
            "Src/AttachmentScreen.pa.yaml",
            "References/DataSources.json",
            "AppCheckerResult.sarif",
        ]:
            if required not in names:
                fail(f"packed MVP app is missing {required}")
        data_sources = json.loads(zf.read("References/DataSources.json"))
        data_source_text = json.dumps(data_sources)
        for table in [
            "FormVersions",
            "Sections",
            "Questions",
            "FormAssignments",
            "Submissions",
            "SubmissionAnswers",
            "SubmissionFiles",
        ]:
            if table not in data_source_text:
                fail(f"packed MVP app is missing Dataverse table reference: {table}")
        live_entities = {
            item.get("RelatedEntityName") or item.get("Name")
            for item in data_sources.get("DataSources", [])
        }
        for unused_table in ["Activities", "Forms", "ValidationRules"]:
            if unused_table in live_entities:
                fail(f"packed MVP app still carries unused data source reference: {unused_table}")
        props = json.loads(zf.read("Properties.json"))
        if props.get("DocumentLayoutScaleToFit") is not False:
            fail("packed MVP app must disable Scale to fit for phone-responsive layout")
        if props.get("DocumentLayoutMaintainAspectRatio") is not False:
            fail("packed MVP app must disable Lock aspect ratio for phone-responsive layout")
        if props.get("DocumentLayoutLockOrientation") is not False:
            fail("packed MVP app must disable Lock orientation for phone-responsive layout")
        sarif = json.loads(zf.read("AppCheckerResult.sarif"))
        results = sarif.get("runs", [{}])[0].get("results", [])
        if results:
            fail(f"packed MVP app has embedded App Checker results: {len(results)}")


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    for rel_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                fail(f"{rel_path} is missing marker: {marker}")

    all_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in REQUIRED_FILES)
    for pattern in SECRET_PATTERNS:
        if pattern.search(all_text):
            fail(f"possible secret pattern found: {pattern.pattern}")

    src_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in REQUIRED_FILES if path.endswith(".pa.yaml"))
    if "Login" in src_text or "password" in src_text.lower():
        fail("Canvas source scaffold appears to include custom login/password handling")
    if "Assigned form found for" in src_text or "No assigned forms for" in src_text:
        fail("Entry screen must show signed-in user in the header and keep assignment status text user-neutral")
    if src_text.count("Signed in as") < 5:
        fail("Every MVP screen must show the signed-in user at the top")
    if "FormVersion.Form.Name" not in src_text or "VersionCode" not in src_text:
        fail("Assigned form entry must show both form display name and version code")
    if "Lower(UserEmail)" in src_text:
        fail("Do not call Lower() on Dataverse UserEmail columns inside delegable filters")
    if "gblAttachmentQuestion" in src_text:
        fail("Attachment screen should not depend on undefined gblAttachmentQuestion")
    if "Status (FormAssignments)" in src_text or "Status (Submissions)" in src_text or "Text(gblSubmission.'Status')" in src_text:
        fail("MVP Canvas source must not depend on ambiguous Dataverse custom Status choice columns; relax/rename the Dataverse column instead")
    if "FormVersion = gblFormVersion" in src_text or "Submission = gblSubmission" in src_text:
        fail("Use local collection id comparisons instead of direct Dataverse lookup record comparisons")
    if "Location.Accuracy" in src_text:
        fail("Power Fx Location signal does not expose Accuracy; use Latitude, Longitude, and Altitude only")
    if "ValueBoolean:" in src_text:
        fail("Do not patch ValueBoolean until Studio confirms the imported Dataverse field type")
    if "[@Choices]" in src_text or "ClearCollect(colChoices" in src_text:
        fail("Do not reference the Choices table until the Studio app has that data source bound")
    if "Clear(" in src_text:
        fail("Use ClearCollect/RemoveIf collection initialization instead of Clear() in importable formulas")
    if "ValueDate:" in src_text:
        fail("Do not patch ValueDate until staged answer records have a confirmed Date-typed field")
    if "Filter(colQuestions, false)" in src_text or "Filter(Questions, false)" in src_text or "Filter(Sections, false)" in src_text or "Filter(Submissions, false)" in src_text or "Filter(SubmissionAnswers, false)" in src_text:
        fail("Do not use literal false Filter predicates for empty collection initialization")
    if "ForAll(" in src_text:
        fail("Do not mutate data sources inside ForAll in the MVP import package")
    stale_collection_patterns = [
        "ClearCollect(colAllSections",
        "ClearCollect(colAllQuestions",
        "ClearCollect(colAllAnswers",
        "ClearCollect(colUserSubmissions",
        "ClearCollect(colSections",
        "ClearCollect(colQuestions",
        "ClearCollect(colAnswers",
        "ClearCollect(colRules",
    ]
    for pattern in stale_collection_patterns:
        if pattern in src_text:
            fail(f"Do not stage whole Dataverse tables or one-shot collections in the MVP package: {pattern}")

    for path in REQUIRED_FILES:
        if not path.endswith(".pa.yaml"):
            continue
        active_control = None
        for line_no, line in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("- Name:"):
                active_control = None
            elif stripped == "Control: Label@2.5.1":
                active_control = "Label"
            elif stripped in {"Control: Button", "Control: Button@2.2.0"}:
                active_control = "Button"
            elif stripped.startswith("Control:"):
                active_control = None
            prop = stripped.split(":", 1)[0] if ":" in stripped else None
            if active_control == "Label" and prop in {"AccessibleLabel", "TabIndex", "Role"}:
                fail(f"{path}:{line_no} uses {prop} on Label@2.5.1, which the current Source Code import schema rejects")
            if active_control == "Button" and prop == "TabIndex":
                fail(f"{path}:{line_no} uses TabIndex on Button, which the current Source Code import schema rejects")
            if active_control == "Button" and prop in {"Fill", "Color", "HoverFill", "PressedFill", "HoverColor", "PressedColor", "BorderThickness", "Align"}:
                fail(f"{path}:{line_no} uses {prop} on Button, which the current Source Code import path rejects or downgrades")

    for required in ["AccessibleLabel", "TabIndex"]:
        if required not in src_text:
            fail(f"MVP app source is missing supported accessibility property: {required}")

    if "app-src/Src" in all_text:
        fail("Slice artifacts should not instruct overwriting the existing fixed-screen app source")

    validate_packed_msapp()

    print("OK: Canvas renderer slice artifacts and packed MVP app are present and aligned with the July 7 MVP.")


if __name__ == "__main__":
    main()
