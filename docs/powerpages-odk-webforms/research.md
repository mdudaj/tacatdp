# Power Pages ODK Web Forms Research

Status: implementation guidance.

## Decision-Relevant Findings

- Power Pages can host a compiled custom front-end code site and PAC exposes `download-code-site` / `upload-code-site` commands for existing sites. In the installed PAC version, `download-code-site` requires `--webSiteId`.
- A Power Pages SPA that relies on Power Pages authentication, web roles, and table permissions should call the Power Pages Web API at `/_api/...`, not raw Dataverse Web API from browser code.
- Power Pages basic forms have built-in file attachment support with note attachment or Azure Blob Storage, but that control is Dataverse-form based and is not the same UX surface as ODK Web Forms.
- Power Pages file columns are documented for basic forms and `/_api`, but file upload through built-in forms can't happen in Insert mode. TACATDP's hosted browser test created attachment metadata but direct file-column binary upload failed, so binary persistence remains a separate managed Microsoft slice.
- Power Pages PWA installability is not the same as offline write/sync support. Offline drafts and submit retry must be implemented explicitly, using browser storage such as IndexedDB and a sync queue.
- ODK Central is organized around projects, forms, form versions/drafts, submissions, submission versions/review state, attachments, and optional datasets/entities.
- ODK Web Forms is a Vue-based runtime backed by `@getodk/xforms-engine`. It expects XForms semantics, so TACATDP should preserve canonical XForm XML and submitted instance XML/JSON rather than only storing decomposed answer rows.
- ODK XForms engine edit mode may assign a new `instanceID` while preserving the prior id as `deprecatedID`. TACATDP must therefore use the selected Dataverse submission row as the canonical edit target and must not rely only on the emitted XML `instanceID` when editing.
- pyxform is the appropriate XLSForm compiler for the next full-form seed: official project docs state that it converts XLSForm spreadsheets into ODK XForms, PyPI lists `pyxform 4.5.0` released 2026-06-25 with Python `>=3.10`, and the documented CLI is `xls2xform path_to_XLSForm [output_path]`.
- The revised workbook `docs/Revised_TACATDP impact evaluation_20260712.xlsx` has settings `form_id=tacatdp_impact_evaluation`, `version=2607121652`, and `instance_name=concat(${Customer_ID}, ":", ${Customer_Name})`; saved record cards should use that instance name when available.
- ODK Collect's user model has project/form entry points, draft editing, ready/sent states, form navigation, and edit rules. TACATDP should mirror those concepts in a Microsoft-managed web shell while letting ODK Web Forms own the question UI.
- LIMS and STEMGEN provide reusable design-system lessons: project tokens, shared component recipes, labeled back actions, task-focused pages, visible spacing between major siblings, and feature CSS only for narrow exceptions.

## Governing References

- Power Pages Web API: https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview
- Power Pages basic forms and built-in file upload: https://learn.microsoft.com/en-us/power-pages/configure/basic-forms
- Power Pages file columns: https://learn.microsoft.com/en-us/power-pages/configure/file-column
- Dataverse file column data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/file-column-data
- Power Pages table permissions: https://learn.microsoft.com/en-us/power-pages/security/table-permissions
- PAC Pages CLI: https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/pages
- Power Pages PWA: https://learn.microsoft.com/en-us/power-pages/configure/progressive-web-apps
- ODK Collect form management: https://docs.getodk.org/collect-forms/
- ODK Collect form filling/navigation: https://docs.getodk.org/collect-filling-forms/
- ODK Central API: https://docs.getodk.org/central-api/
- ODK Central form API: https://docs.getodk.org/central-api-form-management/
- ODK Central submission API: https://docs.getodk.org/central-api-submission-management/
- ODK dataset/entity APIs: https://docs.getodk.org/central-api-dataset-management/ and https://docs.getodk.org/central-api-entity-management/
- ODK Web Forms source/package context: https://github.com/getodk/web-forms and https://github.com/getodk/central-frontend
- pyxform: https://github.com/XLSForm/pyxform and https://pypi.org/project/pyxform/
- XLSForm settings and instance names: https://docs.getodk.org/xlsform/ and https://xlsform.org/en/

## Implication for TACATDP

The Power Pages MVP should be XForms-first: Dataverse stores published form versions with XForm XML, assignments, submission headers, versioned submitted payloads, and attachments. Decomposed answer rows remain optional projections for reporting, not the runtime source of truth.

The shareable MVP should no longer open as a diagnostic proof page. It should open as **Monitoring Tool**: a CRDB-branded work queue with signed-in user context, project/form cards, draft/history signals, reusable loading states, and a focused ODK runtime page.
