# Power Pages ODK Web Forms Slice Checklist

## Completed

- [x] ODK Central-inspired Dataverse schema deployed to the Power Pages environment.
- [x] Rich XForm-backed MVP form seeded.
- [x] Power Pages Web API settings configured for 8 `mp_*` tables.
- [x] Authenticated Users table permissions linked.
- [x] Invalid nameless site settings cleaned.
- [x] `/api-smoke` page uploaded.
- [x] Automated hosted-state smoke verifier added and passing.
- [x] Browser `/api-smoke` runtime test passed after Power Pages Security workspace table-permission role saves.
- [x] `EntityPermissionReadIsMissing` troubleshooting documented.
- [x] File-handling research documented for built-in Power Pages controls, file columns, and the hosted browser failure.
- [x] Monitoring Tool UX/design-system direction documented.

## Completed Slice: SPA Foundation

- [x] User stories captured.
- [x] SPA package skeleton created under `powerpages/webforms-spa/`.
- [x] Mobile-first shell created without ODK dependency installation.
- [x] Power Pages `/_api` client module added.
- [x] Local draft adapter stub added.
- [x] Source validator added for no-secret and `/_api` guardrails.
- [x] Package/version/license review accepted before package installation.

## Current Slice: ODK Runtime Proof

- [x] Review `vue`, `vite`, `@vitejs/plugin-vue`, `typescript`, `vue-tsc`, ODK Web Forms, and XForms engine package versions/licenses.
- [x] Install dependencies from the pinned package set.
- [x] Build the SPA locally.
- [x] Load one XForm XML payload through the API client.
- [x] Render through ODK Web Forms/XForms engine.
- [x] Save a browser-local runtime marker in IndexedDB after form load.
- [x] Keep automated hosted-state smoke verifier as a required gate.

## Current Slice: Dataverse Submission Mapping

- [x] Map ODK Web Forms submit payload to `mp_submissions`.
- [x] Map canonical instance XML and compact submit metadata to `mp_submissionversions`.
- [x] Use Power Pages `/_api`, CSRF token handling, and deployed lookup navigation properties.
- [x] Update the source validator to guard the submit mapping path.
- [x] Add browser-visible submit diagnostics for build marker, ODK runtime click, ODK submit event, and Dataverse write attempt.
- [x] Confirm hosted browser shows build `submit-no-formversion-bind-20260711-001`.
- [x] Diagnose first submit authorization failure: ODK emitted ready payload, Power Pages blocked `mp_FormVersion@odata.bind` with `90040106` because `mp_formversion` lacked `Append To`.
- [x] Confirm a valid ODK Send emits the ODK submit event and creates `mp_submissions` plus `mp_submissionversions` rows.
- [x] Verify the submitted `SubmissionVersions` JSON preserves `assignmentKey`, `formVersionId`, and `xmlFormId` while browser submit skips the failing `Submissions.FormVersion` lookup bind.
- [x] Add attachment metadata handling after the base submit path works.
- [x] Verify hosted browser shows build `renderer-spacing-submit-label-20260711-001`.
- [x] Verify a submit with one photo/file creates an `mp_submissionattachment` row.
- [x] Verify whether Power Pages accepts or rejects the guarded file-column binary upload probe.
- [ ] Add browser-level submit verification against the Power Pages developer environment.

## Current Slice: Attachment Persistence Probe

- [x] Preserve the working `mp_submissions` and `mp_submissionversions` write path.
- [x] Extract non-`xml_submission_file` `File` values from the ODK submit payload.
- [x] Create `mp_submissionattachments` rows linked to the created submission version.
- [x] Attempt single-request `PATCH /_api/mp_submissionattachments(<id>)/mp_file` with `x-ms-file-name`.
- [x] Report attachment row count, binary upload count, and warning details in the hosted UI.
- [x] Browser-confirm binary upload behavior on the hosted Power Pages origin: metadata persists, direct file-column binary upload fails with `400` / `0x80048d19`, and `mp_file_name` remains null.

### Submit Diagnosis Workflow

If clicking ODK Send appears to reload the page or returns to the top with answers still filled, do not patch the submit path from assumption. Use this sequence:

1. Confirm the hosted page shows build `submit-diagnostics-20260711-001`.
2. If the build marker is absent, clear Power Pages server-side cache through `/_services/about` or Power Pages preview, then retest.
3. Click Send once and inspect the visible diagnostics.
4. If `Last runtime click` changes but `Last ODK submit event` does not, treat it as an ODK validation/runtime issue and inspect visible validation errors before Dataverse code.
5. If `Last ODK submit event` changes but `Last Dataverse write` fails, use the displayed error and Power Pages `/_api`/table-permission docs. For `90040106` on `mp_formversion` to `mp_submission`, grant `Append To` on the `mp_formversion` table permission while keeping create/write/delete disabled.
6. If Dataverse write completes, verify new rows in `mp_submissions` and `mp_submissionversions`.

## Deferred

- [ ] Offline sync queue.
- [ ] Production-grade attachment binary persistence through a verified Power Pages file-column route or a managed Microsoft server-side mediator.
- [ ] Submission history.
- [ ] Production-scoped table permissions.
- [ ] Admin publishing UI.

## Next Slice: Monitoring Tool UX Foundation

- [x] Rename user-facing shell text to **Monitoring Tool**.
- [x] Add CRDB-branded design tokens from `assets/images/CRDB_Bank_PLC.svg` and verify contrast-oriented darker shell primary.
- [x] Add reusable shell sections: app shell, top action bar, loading panel, project card, form card, status banner, debug panel, ODK runtime boundary.
- [x] Route unauthenticated users to Power Pages / Microsoft Entra sign-in when the Power Pages token provider is unavailable.
- [x] Present a work queue first: project/form cards, draft count, session indicator, and signed-in user in the top shell.
- [x] Move prototype diagnostics behind a collapsed debug panel.
- [x] Keep attachment binary warnings visible but not as a full submission failure when metadata persisted.
- [x] Verify host CSS does not broadly restyle ODK controls with the source validator.
- [x] Upload build `monitoring-tool-ux-foundation-20260711-001` to the explicit Power Pages website ID.
- [x] Post-upload PAC download verifies Home references `index-CLUTd6fC.mjs` and `index-CLlTa1IS.css`.
- [ ] Verify phone-width layout in a signed-in browser session.
- [ ] Verify the signed-in browser can start the form, submit, and see the collapsed diagnostics only when expanded.

## Current Slice: CRUD Workspace Revision

- [x] Replace assigned-form-first shell with project cards as the first screen.
- [x] Add project-detail workspace with icon+text Back and Add new actions.
- [x] Add Saved and Drafts tabs for project data cards.
- [x] Page data cards at 10 records per page.
- [x] Use Open for existing saved/draft cards and avoid Start in the shell.
- [x] Preserve online/offline status in the project workspace and runner top bar.
- [x] Keep ODK Web Forms isolated inside `OdkRuntimeBoundary`.
- [ ] Verify the signed-in browser shows only one CRDB header, project cards first, and the project detail data-card tabs.
