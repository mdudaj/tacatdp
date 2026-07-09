# TACATDP WebForms SPA

Status: scaffold only. Do not install packages until `docs/powerpages-odk-webforms/package-review.md` is accepted.

## Purpose

This package is the future Power Pages hosted field runtime. It uses Power Pages authentication and the Power Pages Web API `/_api`; it must not contain Dataverse credentials, client secrets, raw access tokens, or direct OAuth calls.

## Current Slice

- Mobile-first assigned-forms shell.
- Power Pages `/_api` client for assignments, form versions, and forms.
- IndexedDB draft adapter stub.
- No ODK package import yet.

## Verification

From the repository root:

```bash
python3 scripts/validate-webforms-spa-foundation.py
python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env
```

After package installation is approved:

```bash
cd powerpages/webforms-spa
npm install
npm run build
```
