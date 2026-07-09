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
9. Implement assigned forms, form load, local draft, online submit, attachment upload, and history.
10. Upload compiled SPA with `pac pages upload-code-site` after approval.

## Verification Gates

- `pac env who` shows the Power Pages developer environment.
- `pac pages list` shows `TACATDP Monitoring Tool`.
- Schema dry-run plan lists only additive table/column/relationship creation.
- Browser `/_api` read succeeds for one metadata table.
- Local draft survives refresh.
- Online submit creates `Submissions` and `SubmissionVersions` in the Power Pages environment.
- Attachment upload creates `SubmissionAttachments`.


## Current Slice: Authenticated `/_api` Read Smoke

Implementation instructions:

1. Inspect `docs/powerpages-odk-webforms/api-smoke-test.md`, `powerpages/tacatdp-monitoring-tool/.powerpages-site/web-pages/api-smoke/`, and Microsoft Power Pages Web API/table-permission docs.
2. Validate source with `python3 scripts/validate-powerpages-api-smoke.py`.
3. Upload only after confirming `pac env who` and `pac pages list` still point to `PowerPagesDeveloper-070926-125720` and website `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`.
4. Run `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`; it must verify hosted page records, Web API settings, permissions, role links, assignment seed, form version, and form metadata.
5. Do not add ODK Web Forms packages until the automated hosted verifier passes. Manual browser navigation to `/api-smoke` is optional observation, not the delivery gate.
