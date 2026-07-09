# Power Pages ODK Web Forms Research

Status: implementation guidance.

## Decision-Relevant Findings

- Power Pages can host a compiled custom front-end code site and PAC exposes `download-code-site` / `upload-code-site` commands for existing sites. In the installed PAC version, `download-code-site` requires `--webSiteId`.
- A Power Pages SPA that relies on Power Pages authentication, web roles, and table permissions should call the Power Pages Web API at `/_api/...`, not raw Dataverse Web API from browser code.
- Power Pages PWA installability is not the same as offline write/sync support. Offline drafts and submit retry must be implemented explicitly, using browser storage such as IndexedDB and a sync queue.
- ODK Central is organized around projects, forms, form versions/drafts, submissions, submission versions/review state, attachments, and optional datasets/entities.
- ODK Web Forms is a Vue-based runtime backed by `@getodk/xforms-engine`. It expects XForms semantics, so TACATDP should preserve canonical XForm XML and submitted instance XML/JSON rather than only storing decomposed answer rows.

## Governing References

- Power Pages Web API: https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview
- Power Pages table permissions: https://learn.microsoft.com/en-us/power-pages/security/table-permissions
- PAC Pages CLI: https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/pages
- Power Pages PWA: https://learn.microsoft.com/en-us/power-pages/configure/progressive-web-apps
- ODK Central API: https://docs.getodk.org/central-api/
- ODK Central form API: https://docs.getodk.org/central-api-form-management/
- ODK Central submission API: https://docs.getodk.org/central-api-submission-management/
- ODK dataset/entity APIs: https://docs.getodk.org/central-api-dataset-management/ and https://docs.getodk.org/central-api-entity-management/
- ODK Web Forms source/package context: https://github.com/getodk/web-forms and https://github.com/getodk/central-frontend

## Implication for TACATDP

The Power Pages MVP should be XForms-first: Dataverse stores published form versions with XForm XML, assignments, submission headers, versioned submitted payloads, and attachments. Decomposed answer rows remain optional projections for reporting, not the runtime source of truth.
