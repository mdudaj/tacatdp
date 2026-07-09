# Power Pages API Smoke Test Slice

## Evidence to Inspect First

- `docs/powerpages-odk-webforms/adr-0002-power-pages-odk-webforms.md`
- `docs/powerpages-odk-webforms/dataverse-setup-runbook.md`
- `schemas/dataverse/odk-central-inspired-mvp-schema.json`
- `powerpages/tacatdp-monitoring-tool/.powerpages-site/web-pages/api-smoke/`
- Microsoft Power Pages Web API docs: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview`
- Microsoft Power Pages HTTP/CSRF docs: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-http-requests-handle-errors`
- Microsoft Power Pages table-permission docs: `https://learn.microsoft.com/en-us/power-pages/security/table-permissions`

## Purpose

This slice proves the browser runtime can read TACATDP Dataverse metadata through Power Pages authentication, table permissions, web roles, and `/_api` before ODK Web Forms packages are added.

## Source Route

- Power Pages route: `/api-smoke`
- Source folder: `powerpages/tacatdp-monitoring-tool/.powerpages-site/web-pages/api-smoke/`
- Page visibility: hidden from sitemap

## Runtime Checks

The page reads:

1. `/_api/mp_formassignments?$select=mp_assignmentkey,mp_useremail,mp_lifecyclestatus,_mp_formversion_value&$top=10`
2. `/_api/mp_formversions(<id>)?$select=mp_version,mp_webformsenabled,mp_lifecyclestatus,mp_xformxml,_mp_form_value`
3. `/_api/mp_forms(<id>)?$select=mp_name,mp_xmlformid,mp_lifecyclestatus`

These EntitySetName values were verified from Dataverse metadata on 2026-07-09.

## Local Validation

```bash
python3 scripts/validate-powerpages-api-smoke.py
```

## Upload Command

This PAC CLI version distinguishes metadata upload from compiled code-site upload. For this smoke page, use metadata upload, not `upload-code-site`.

Only upload after reviewing the diff and confirming the target site ID:

```bash
pac pages download \
  --environment "https://orga3cf4b37.crm4.dynamics.com/" \
  --webSiteId "fccc0cc6-7f5e-4885-aeb8-2272e68130a3" \
  --path ./powerpages-upload \
  --overwrite \
  --modelVersion Enhanced

# Copy or generate the smoke page into:
# ./powerpages-upload/tacatdp-monitoring-tool/web-pages/api-smoke/

pac pages upload \
  --environment "https://orga3cf4b37.crm4.dynamics.com/" \
  --path ./powerpages-upload/tacatdp-monitoring-tool \
  --modelVersion Enhanced
```

After upload, refresh the committed code-site source:

```bash
pac pages download-code-site \
  --environment "https://orga3cf4b37.crm4.dynamics.com/" \
  --webSiteId "fccc0cc6-7f5e-4885-aeb8-2272e68130a3" \
  --path ./powerpages \
  --overwrite
```

## Automated Hosted Verification

Do not make manual browser navigation the delivery gate. Verify the hosted state programmatically:

```bash
python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env
```

The verifier checks:

- the local smoke-page source and JavaScript syntax,
- the expected Power Pages website,
- the 8 `mp_*` Dataverse EntitySetName values,
- the 16 named `Webapi/mp_*` site settings,
- absence of nameless site settings,
- 8 table permissions and Authenticated Users web-role links,
- 2 `/api-smoke` page rows,
- at least one assignment, form version with XForm XML, and form record.

Opening `/api-smoke` remains an optional observation step, not the release gate.

## Next Slice

After the automated hosted smoke verifier passes, add the first ODK shell that loads `FormVersions.XFormXml` from the form version result and renders the form through the selected ODK Web Forms package versions.

## PAC 2.8.1 Upload Note

`upload-code-site` is reserved for compiled custom front-end code and requires `--rootPath` plus `--compiledPath` in this PAC build.
