# Acceptance Criteria

- Power Pages site source is downloaded under `powerpages/tacatdp-monitoring-tool/`.
- ODK Central-inspired schema artifacts exist and have a dry-run Dataverse plan.
- One assigned XForm-backed form can be read by an authenticated Power Pages user.
- The UI does not create or display a draft unless the stored browser-local state is restorable. Runtime-load markers are not drafts.
- Online submit creates a submission header and current submission version.
- One attachment is represented as a `SubmissionAttachments` row linked to the submission version.
- Browser binary upload through the Power Pages route is attempted with the documented Dataverse single-request file-column pattern and must report whether Power Pages accepted or rejected the binary content.
- No raw Dataverse credentials or client secrets are present in the SPA.


## API Smoke Slice Acceptance

- `python3 scripts/validate-powerpages-api-smoke.py` passes locally.
- Power Pages source contains a hidden `/api-smoke` page.
- The page calls Power Pages `/_api`, not raw Dataverse Web API.
- Browser code contains no client secret, bearer token, or Dataverse OAuth endpoint.
- `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env` passes against the hosted environment.
- Browser navigation to `/api-smoke` passes after Power Pages Security workspace table-permission saves; the page must show the expected portal contact, `Authenticated Users`, and `Power Pages /_api read smoke test passed.`

## SPA Foundation Slice Acceptance

- `docs/powerpages-odk-webforms/user-stories.md` exists and maps stories to requirements.
- `docs/powerpages-odk-webforms/slice-checklist.md` identifies completed, current, next, and deferred work.
- `docs/powerpages-odk-webforms/package-review.md` exists and blocks dependency installation until accepted.
- `powerpages/webforms-spa/` contains a private Vite/Vue package skeleton.
- SPA source uses Power Pages `/_api` paths and includes anti-forgery token handling for future writes.
- SPA source contains no raw Dataverse OAuth endpoint, client secret, bearer token, or custom login.
- `python3 scripts/validate-webforms-spa-foundation.py` passes.
- Hosted state remains verified by `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`.

## ODK Runtime Proof Acceptance

- The assigned form view imports `OdkWebForm` from `@getodk/web-forms`.
- The selected assignment's XForm XML is passed to the ODK runtime from the Power Pages `/_api` client result.
- The runtime `loaded` event updates only the runtime status. It must not save a browser-local draft marker or refresh a misleading local draft count.
- The runtime `submit` event validates ODK payload readiness and writes the canonical instance XML through Power Pages `/_api`.
- `npm run build` succeeds for `powerpages/webforms-spa/`.

## Monitoring Tool UX Acceptance

- Shell actions use the maintained `@lucide/vue` icon package rather than text glyphs.
- Back actions use `ArrowLeft`; Open actions use `FolderOpen`; pagination uses chevron icons.
- The project workspace does not show old non-restorable runtime-load markers as local drafts.
- The empty draft state tells users that editable local draft save/restore is not enabled yet.
- The Saved tab lists all submitted records readable by the authenticated user's Power Pages table permissions; it must not filter submitted records by `mp_useremail`.
- The Saved/Drafts toolbar includes a search input at the end and filters as the user types.
- Saved submitted records show owner email, version, updated timestamp, and an Edit action.
- Edit opens ODK Web Forms using `editInstance` and the latest `SubmissionVersions.XFormSubmissionXml`; submit writes a new submission version for the same ODK instance id.

## Dataverse Submission Mapping Acceptance

- The submit handler uses the ODK Web Forms submit payload, not page-local input scraping.
- Non-ready ODK payloads are blocked before Dataverse writes.
- The browser extracts `xml_submission_file` and preserves it in `SubmissionVersions.XFormSubmissionXml`.
- Submit creates or reuses one `Submissions` header keyed by ODK `instanceID`.
- Submit creates a new `SubmissionVersions` record with `Current = true`, version number, compact JSON metadata, browser user agent, and device id.
- Mutating requests use Power Pages `/_api`, EntitySetName paths, JSON/OData headers, submission-version `@odata.bind` lookup references, and the Power Pages anti-forgery token.
- Browser submit does not bind `Submissions.FormVersion` in the MVP because Power Pages runtime continued to return `90040106` after the documented append/append-to table permissions were verified. The submitted `SubmissionVersions` JSON must include `formVersionId`, `assignmentKey`, and `xmlFormId` until a server-side association or child-permission model is proven.
- Attachment metadata persists to `mp_submissionattachments` and binds to the created `mp_submissionversion`.
- Attachment binary upload uses a guarded `PATCH /_api/mp_submissionattachments(<id>)/mp_file` probe with `x-ms-file-name`; if Power Pages rejects the non-JSON file-column request, the submit remains complete and the warning is shown in the browser.

## Attachment Slice Acceptance

- The SPA creates a `SubmissionAttachments` row for each non-`xml_submission_file` `File` value in the ODK submit payload.
- Each attachment row stores `FileName`, `MediaType`, `UploadedAt`, and a `SubmissionVersion` lookup.
- The `SubmissionVersions` JSON summary stores attachment names plus file name, media type, and size metadata.
- The hosted UI shows attachment row count, binary upload count, and any binary warning after submit.
- The source validator guards the `mp_submissionattachments`, `mp_SubmissionVersion@odata.bind`, `mp_file`, and `x-ms-file-name` code paths.
- Binary upload is considered proven only after the hosted Power Pages browser reports a nonzero binary upload count and Dataverse file content is verified. On 2026-07-11, the hosted browser proved metadata persistence but direct file-column binary upload failed with `400` / `0x80048d19`; production-grade binary persistence is therefore a later managed server-side slice.
