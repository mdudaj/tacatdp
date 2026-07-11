# TACATDP WebForms SPA

Status: ODK runtime proof and first Dataverse submission mapping implemented locally. Dependencies are pinned and locked.

## Purpose

This package is the future Power Pages hosted field runtime. It uses Power Pages authentication and the Power Pages Web API `/_api`; it must not contain Dataverse credentials, client secrets, raw access tokens, or direct OAuth calls.

## Current Slice

- Mobile-first assigned-forms shell.
- Power Pages `/_api` client for assignments, form versions, forms, submissions, submission versions, and submission attachments.
- Local Vite development uses a non-secret fixture because Power Pages `/_api` only exists on the hosted Power Pages origin.
- IndexedDB draft adapter used for the local runtime-loaded marker.
- ODK Web Forms renders the selected assignment's XForm XML.
- ODK submit validates the runtime payload, extracts `xml_submission_file`, creates or reuses a `Submissions` header, and writes a `SubmissionVersions` record with canonical XML plus compact JSON metadata.
- Hosted browser submit intentionally does not bind `Submissions.FormVersion` for the MVP. Power Pages runtime continued returning `90040106` for that association after the documented append/append-to table permissions were verified. The immutable submission-version JSON keeps `formVersionId`, `assignmentKey`, and `xmlFormId` so the record can still be traced to the published form version.
- The host shell only handles assignment selection and runtime status. The selected form is mounted in `odk-runtime-host` so ODK Web Forms and PrimeVue own the form controls, spacing, fonts, and responsive layout.
- The hosted shell shows submit diagnostics while the first write path is being proven: build marker, last ODK runtime click, last ODK submit event, and last Dataverse write attempt.
- Attachment handling creates `SubmissionAttachments` rows for ODK file payloads and stores attachment metadata in the submission-version JSON summary.
- Attachment binary upload is implemented as a guarded hosted-browser probe: the client attempts the documented Dataverse single-request file-column `PATCH` against `/_api/mp_submissionattachments(<id>)/mp_file` and reports the binary upload count or the exact Power Pages rejection. Production-grade binary storage remains unproven until the hosted browser confirms this route.

## Local Route

```bash
cd powerpages/webforms-spa
source ~/.nvm/nvm.sh
nvm use v24.18.0
npm run dev
```

Open the Vite URL that is printed, usually `http://localhost:5173/`.

On localhost, assigned forms come from `src/dev/assignedForms.ts` and submit returns a local fake result. On the hosted Power Pages site, the same screen calls `/_api/mp_formassignments`, `/_api/mp_formversions`, `/_api/mp_forms`, `/_api/mp_submissions`, `/_api/mp_submissionversions`, and `/_api/mp_submissionattachments` through the signed-in Power Pages session with OData headers and the Power Pages anti-forgery token.

## Verification

From the repository root:

```bash
python3 scripts/validate-webforms-spa-foundation.py
python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env
```

```bash
cd powerpages/webforms-spa
npm install
npm run build
```

## Hosted Upload

Uploading changes the hosted Power Pages site and requires explicit approval.

Verify the active target first:

```bash
pac env who
pac pages list
```

For PAC CLI 2.8.1, `upload-code-site` can initialize a code-site package, but in this environment it created a duplicate Power Pages site because the site name was not unique enough. Do not use `--siteName` alone as the deployment proof.

```bash
pac pages download \
  --environment "https://orga3cf4b37.crm4.dynamics.com/" \
  --webSiteId "fccc0cc6-7f5e-4885-aeb8-2272e68130a3" \
  --path ./powerpages/tacatdp-monitoring-tool-upload \
  --overwrite \
  --modelVersion Enhanced

pac pages upload \
  --environment "https://orga3cf4b37.crm4.dynamics.com/" \
  --path ./powerpages/tacatdp-monitoring-tool-upload/tacatdp-monitoring-tool \
  --modelVersion Enhanced \
  --forceUploadAll
```

After upload, restart or sync the site in Power Pages if needed, then open the site while signed in and confirm assigned forms render through ODK Web Forms.

For submit troubleshooting, first confirm the hosted page shows the expected build marker. If it does not, clear Power Pages server-side cache from `/_services/about` or Power Pages preview, then retest. After clicking ODK Send, use the visible diagnostics to distinguish stale cache, ODK validation blocking submit, ODK event delivery, and Dataverse `/_api` write failures.

Build output intentionally emits JavaScript modules as `.mjs` files. The Power Pages developer environment blocks `.js` as a Dataverse attachment extension, and changing that organization-wide block list is broader than this proof-of-concept deployment requires.
