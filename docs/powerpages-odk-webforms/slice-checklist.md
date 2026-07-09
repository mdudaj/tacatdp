# Power Pages ODK Web Forms Slice Checklist

## Completed

- [x] ODK Central-inspired Dataverse schema deployed to the Power Pages environment.
- [x] Rich XForm-backed MVP form seeded.
- [x] Power Pages Web API settings configured for 8 `mp_*` tables.
- [x] Authenticated Users table permissions linked.
- [x] Invalid nameless site settings cleaned.
- [x] `/api-smoke` page uploaded.
- [x] Automated hosted-state smoke verifier added and passing.

## Current Slice: SPA Foundation

- [x] User stories captured.
- [x] SPA package skeleton created under `powerpages/webforms-spa/`.
- [x] Mobile-first shell created without ODK dependency installation.
- [x] Power Pages `/_api` client module added.
- [x] Local draft adapter stub added.
- [x] Source validator added for no-secret and `/_api` guardrails.
- [ ] Package/version/license review accepted before package installation.

## Next Slice: Package Review and ODK Runtime Proof

- [ ] Review `vue`, `vite`, `@vitejs/plugin-vue`, `typescript`, `vue-tsc`, ODK Web Forms, and XForms engine package versions/licenses.
- [ ] Install dependencies only after approval.
- [ ] Build the SPA locally.
- [ ] Load one XForm XML payload through the API client.
- [ ] Render through ODK Web Forms/XForms engine.
- [ ] Keep automated hosted-state smoke verifier as a required gate.

## Deferred

- [ ] Offline sync queue.
- [ ] Online submit mutation path.
- [ ] Attachment upload.
- [ ] Submission history.
- [ ] Production-scoped table permissions.
- [ ] Admin publishing UI.
