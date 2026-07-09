# TACATDP WebForms SPA

Status: package gate accepted. Dependencies are pinned and locked.

## Purpose

This package is the future Power Pages hosted field runtime. It uses Power Pages authentication and the Power Pages Web API `/_api`; it must not contain Dataverse credentials, client secrets, raw access tokens, or direct OAuth calls.

## Current Slice

- Mobile-first assigned-forms shell.
- Power Pages `/_api` client for assignments, form versions, and forms.
- Local Vite development uses a non-secret fixture because Power Pages `/_api` only exists on the hosted Power Pages origin.
- IndexedDB draft adapter stub.
- ODK Web Forms and XForms engine packages are installed but runtime rendering is still the next slice.

## Local Route

```bash
cd powerpages/webforms-spa
source ~/.nvm/nvm.sh
nvm use v24.18.0
npm run dev
```

Open the Vite URL that is printed, usually `http://localhost:5173/`.

On localhost, assigned forms come from `src/dev/assignedForms.ts`. On the hosted Power Pages site, the same screen calls `/_api/mp_formassignments`, `/_api/mp_formversions`, and `/_api/mp_forms` through the signed-in Power Pages session.

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
