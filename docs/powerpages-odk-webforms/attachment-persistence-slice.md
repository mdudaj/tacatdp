# Attachment Persistence Slice

Date: 2026-07-11

## Requirements Note

The MVP must keep all browser writes inside the managed Microsoft boundary. The hosted SPA uses the signed-in Power Pages session, Power Pages table permissions, and the Power Pages anti-forgery token. It must not use raw Dataverse OAuth, client secrets, bearer tokens, external storage, or a custom login.

Microsoft documents the Power Pages portals Web API as the `/_api` route for Dataverse table CRUD, governed by table permissions and web roles. Microsoft also documents Dataverse file-column upload through raw Dataverse Web API routes, including a single-request `PATCH <record>/<filecolumn>` path for files under 128 MB and multi-request upload actions for larger files. Power Pages documents that portals Web API calls to Dataverse actions and functions are unsupported, so the browser binary upload must be treated as a hosted-origin proof, not assumed complete before testing.

## UX Description

The ODK Web Forms runtime remains the primary form surface. On Send, the host shell writes the submission and displays one concise status line with:

- ODK instance id and submission version number.
- Number of attachment metadata records created.
- Number of attachment binaries accepted by the Power Pages file-column route.
- Exact warning text if Power Pages rejects the binary upload.

The host shell does not restyle ODK controls or add a custom attachment widget for this slice.

## Acceptance Criteria

- Non-`xml_submission_file` `File` values in the ODK submit payload create `mp_submissionattachments` records.
- Attachment records bind to the created `mp_submissionversion` through `mp_SubmissionVersion@odata.bind`.
- Attachment rows store file name, media type, and uploaded timestamp.
- The submission-version JSON summary stores attachment names, file names, media types, and byte sizes.
- The browser attempts `PATCH /_api/mp_submissionattachments(<id>)/mp_file` with `x-ms-file-name`.
- The base submission remains complete if binary upload is rejected; the UI reports the rejection for follow-up.
- Binary persistence is accepted only after hosted browser testing shows a nonzero binary upload count and Dataverse file content is verified.

## Accessibility Checklist

- Status updates remain in the existing `aria-live="polite"` runtime proof region.
- No new custom interactive controls are added.
- ODK Web Forms continues to own field labels, validation, focus, and attachment input accessibility.

## Artifact Readiness

- Schema target: `schemas/dataverse/odk-central-inspired-mvp-schema.json`.
- API client: `powerpages/webforms-spa/src/powerpages-api/client.ts`.
- Runtime view: `powerpages/webforms-spa/src/views/AssignedFormsView.vue`.
- Guardrail validator: `scripts/validate-webforms-spa-foundation.py`.
- Delivery checklist: `docs/powerpages-odk-webforms/slice-checklist.md`.
- Acceptance criteria: `docs/powerpages-odk-webforms/acceptance-criteria.md`.

## Verification Summary

- Live metadata read verified:
  - `mp_submissionattachment` entity set is `mp_submissionattachments`.
  - File column logical name is `mp_file`.
  - Submission version lookup logical name is `mp_submissionversion`.
  - Lookup navigation property is `mp_SubmissionVersion`.
- Required local checks:
  - `python3 scripts/validate-webforms-spa-foundation.py`
  - `npm run build` from `powerpages/webforms-spa`
  - `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`
- Required browser check after upload:
  - Submit the seeded form with one file/photo.
  - Confirm the status line shows the latest deployed renderer build marker.
  - Confirm attachment record count is at least 1.
  - Confirm whether binary upload count is 1 or a documented Power Pages rejection warning.

## Browser Verification Result

Observed on 2026-07-11 with build `renderer-spacing-submit-label-20260711-001`:

- ODK submit payload was ready.
- Dataverse write completed.
- `mp_submissions` row was created for `uuid:1be351ef-af63-4225-9d78-f9e2e2c68f23`.
- `mp_submissionversions` row was created with version `1`.
- `mp_submissionattachments` row was created for `1783772222197.png`.
- Submission JSON preserved attachment details: file name `1783772222197.png`, media type `image/png`, size `21197`.
- Direct browser binary upload to `PATCH /_api/mp_submissionattachments(<id>)/mp_file` failed with `400`, Power Pages/Dataverse code `0x80048d19`.
- Dataverse verification showed `mp_file_name` remained null on the attachment row.

Conclusion: Power Pages browser `/_api` is proven for submission and attachment metadata CRUD, but not for direct Dataverse file-column binary upload. Treat binary persistence as the next managed Microsoft server-side slice, not as a browser-only Power Pages Web API task.

## References

- Microsoft Learn: Portals Web API overview, including `/_api`, table permissions, EntitySetName, and unsupported actions/functions.
- Microsoft Learn: Portals Web API HTTP requests and errors, including CSRF token and `90040106` append-to errors.
- Microsoft Learn: Dataverse file column data, including single-request file-column upload and block-upload messages.
