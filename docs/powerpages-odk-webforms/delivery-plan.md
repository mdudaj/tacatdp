# Power Pages ODK Web Forms Delivery Plan

## Target Environment

- Environment: `PowerPagesDeveloper-070926-125720`
- Org URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Site: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

## Package Layout

```text
powerpages/
  tacatdp-monitoring-tool/
    .powerpages-site/
  webforms-spa/
    package.json
    vite.config.ts
    src/
      odk/
      powerpages-api/
      offline/
      views/
```

## Implementation Order

1. Keep downloaded Power Pages source under `powerpages/tacatdp-monitoring-tool/`.
2. Deploy the ODK Central-inspired Dataverse schema to the Power Pages environment after explicit approval.
3. Seed one project, form, form version with XForm XML, assignment, and one test user mapping.
4. Configure Power Pages Web API site settings for the TACATDP tables.
5. Configure table permissions and web roles for authenticated users.
6. Build a tiny authenticated `/_api` read smoke page before adding ODK Web Forms.
7. Scaffold `powerpages/webforms-spa/` with Vue/Vite.
8. Add ODK Web Forms/XForms engine dependencies after package/version/license review.
9. Implement assigned forms, ODK Web Forms runtime load, local draft proof, online submit, attachment upload, and history.
10. Upload compiled SPA through the enhanced Power Pages metadata package after approval, using the explicit website ID package path.
11. Promote the prototype shell into the **Monitoring Tool** UX: CRDB-branded app shell, work queue, top action bars, reusable loading panel, project/form cards, history entry point, and hidden debug diagnostics.
12. Replace the hand-authored rich seed with a pyxform-compiled version of `docs/Revised_TACATDP impact evaluation_20260712.xlsx`, preserving XLSForm settings metadata and assigning the published form version code from `settings.version`.

## Verification Gates

- `pac env who` shows the Power Pages developer environment.
- `pac pages list` shows `TACATDP Monitoring Tool`.
- Schema dry-run plan lists only additive table/column/relationship creation.
- Browser `/_api` read succeeds for one metadata table.
- Local draft survives refresh.
- Online submit creates `Submissions` and `SubmissionVersions` in the Power Pages environment.
- Edit submit creates a new `SubmissionVersions` row on the selected `Submissions` record and does not create a new saved record.
- Saved record cards show computed XLSForm `instance_name` when available.
- Attachment upload creates `SubmissionAttachments`.
- Browser binary file persistence is either verified through the documented Power Pages file-column route or explicitly reported as pending with attachment metadata preserved.
- Mobile and desktop screenshots show the Monitoring Tool shell, CRDB branding, readable form cards, and isolated ODK runtime spacing.


## Completed Slice: Authenticated `/_api` Read Smoke

Implementation instructions:

1. Inspect `docs/powerpages-odk-webforms/api-smoke-test.md`, `powerpages/tacatdp-monitoring-tool/.powerpages-site/web-pages/api-smoke/`, and Microsoft Power Pages Web API/table-permission docs.
2. Validate source with `python3 scripts/validate-powerpages-api-smoke.py`.
3. Upload only after confirming `pac env who` and `pac pages list` still point to `PowerPagesDeveloper-070926-125720` and website `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`.
4. Run `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`; it must verify hosted page records, Web API settings, permissions, role links, assignment seed, form version, and form metadata.
5. Run the browser `/api-smoke` test after Power Pages Security workspace table-permission saves; it must show the expected portal contact, `Authenticated Users`, and `Power Pages /_api read smoke test passed.`
6. Do not add ODK Web Forms packages until both the automated hosted verifier and browser runtime smoke pass.

## Completed Slice: SPA Foundation

Implementation instructions:

1. Inspect `requirements.md`, `user-stories.md`, `slice-checklist.md`, `package-review.md`, and `powerpages/webforms-spa/`.
2. Validate source with `python3 scripts/validate-webforms-spa-foundation.py`.
3. Keep `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env` as the hosted-state gate.
4. Do not run `npm install` or import ODK packages until package/version/license review is accepted.
5. The next implementation slice is package review plus first ODK runtime proof.

## Completed Slice: ODK Runtime Proof

Implementation instructions:

1. Inspect `powerpages/webforms-spa/src/views/AssignedFormsView.vue`, `src/powerpages-api/client.ts`, `src/offline/drafts.ts`, and the installed `@getodk/web-forms` package export before changing runtime behavior.
2. Render only the selected assignment's `xformXml` with `OdkWebForm`; do not add raw Dataverse Web API calls or custom authentication.
3. Treat `loaded` as the proof event and save only a local IndexedDB marker. Do not claim Dataverse draft persistence until the submit/write slice exists.
4. Treat `submit` and `submit-chunked` as proof callbacks for this slice only until the Dataverse submission mapping slice is implemented.
5. Validate with `python3 scripts/validate-webforms-spa-foundation.py`, `npm run build` from `powerpages/webforms-spa/`, and the hosted-state smoke verifier.

## Current Slice: Dataverse Submission Mapping

Implementation instructions:

1. Inspect `skills/power-pages-odk-webforms/SKILL.md`, Microsoft Power Pages Web API docs, `schemas/dataverse/odk-central-inspired-mvp-schema.json`, `scripts/dataverse-schema-deploy.py`, and the installed ODK Web Forms/XForms engine submit payload source before changing submit behavior.
2. Confirm the deployed lookup navigation property names for `FormVersions -> Submissions` and `Submissions -> SubmissionVersions`; TACATDP currently resolves them as `mp_FormVersion` and `mp_Submission`.
3. Use Power Pages `/_api` with EntitySetName paths, JSON/OData headers, `shell.getTokenDeferred` CSRF handling, and `@odata.bind` relationship values.
4. Read the ODK submit payload from `payload.data[0].get("xml_submission_file")`; do not scrape rendered fields or create answer rows as the runtime source of truth.
5. Reject non-ready ODK payloads before writes. For ready payloads, extract `meta/instanceID`, create or reuse `mp_submissions`, and create a current `mp_submissionversions` record with the canonical XML and compact JSON metadata.
6. Keep binary attachments deferred until the attachment slice; this slice stores attachment names only in the JSON metadata summary.
7. Validate with `python3 scripts/validate-webforms-spa-foundation.py`, `npm run build`, and `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`; after approved upload, run a browser submit and verify records in Dataverse.

## Current Slice: Edit Semantics and XLSForm Import Planning

Implementation instructions:

1. Inspect `xlsform-import-and-edit-plan.md`, `requirements.md`, `acceptance-criteria.md`, `AssignedFormsView.vue`, `PowerPagesApiClient`, and ODK local dependency source for `editInstance` / `FormInstanceEditMode`.
2. Treat the selected saved Dataverse submission as the canonical edit target. Do not infer edit identity from the XML `instanceID` emitted by ODK Web Forms.
3. Store a display name in submission-version metadata. For the revised TACATDP workbook, the MVP expression is `Customer_ID:Customer_Name`.
4. Review `package-review.md` before installing `pyxform==4.5.0`.
5. Compile `docs/Revised_TACATDP impact evaluation_20260712.xlsx` with `xls2xform` and seed the generated XML only after dry-run review.
6. Validate with source validator, SPA build, pyxform conversion, hosted smoke, and browser edit/add-new tests.

## Completed Slice: Monitoring Tool UX Foundation

Implementation instructions:

1. Inspect `monitoring-tool-ux-design-system.md`, `file-handling-research.md`, `requirements.md`, `slice-checklist.md`, `powerpages/webforms-spa/src/views/AssignedFormsView.vue`, `powerpages/webforms-spa/src/styles.css`, and CRDB assets under `assets/images/`.
2. Inspect comparable reusable UX patterns from LIMS `docs/UX_DESIGN_SYSTEM.md` and STEMGEN UI tokens/components before adding new CSS.
3. Introduce shared Vue shell components or clearly separated sections for `AppShell`, `TopActionBar`, `LoadingPanel`, `ProjectCard`, `FormCard`, `StatusBanner`, `DebugPanel`, and `OdkRuntimeBoundary`.
4. Rename user-facing shell text to **Monitoring Tool**.
5. Route unauthenticated users to the configured Power Pages / Microsoft Entra sign-in path; do not build a custom login.
6. Show a work queue first: project/form cards, draft count, recent submission/history entry point, signed-in user in the shell, and Refresh.
7. Move prototype diagnostics into a collapsed debug panel and keep submit/file warnings as concise user status.
8. Keep host CSS scoped outside ODK controls except documented runtime boundary spacing and the accepted Submit label/footer behavior.
9. Validate locally with the SPA validator and build; after approved upload, verify mobile and desktop browser behavior on the Power Pages site.

Verification result on 2026-07-11:

- `python3 scripts/validate-webforms-spa-foundation.py` passed.
- `npm run build` passed; warnings were limited to the documented upstream ODK direct `eval` and large bundle warnings.
- `pac pages upload --environment "https://orga3cf4b37.crm4.dynamics.com/" --path ./powerpages/tacatdp-monitoring-tool-upload/tacatdp-monitoring-tool --modelVersion Enhanced --forceUploadAll` succeeded for website `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`.
- Post-upload `pac pages download` verified Home references `index-CLUTd6fC.mjs` and `index-CLlTa1IS.css`.
- `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env` passed after upload.

Remaining manual check:

- Open the private site while signed in and confirm phone-width layout, work queue, form start, ODK runtime, submit, and collapsed diagnostics behavior.
