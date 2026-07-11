# Power Pages WebForms SPA Package Review

Status: accepted for dev install on 2026-07-09. Versions are pinned in `powerpages/webforms-spa/package.json`.

## Policy

Package installation changes the local supply-chain state and must use the approved package set below.

## Accepted Foundation Packages

| Package | Version | License | Purpose | Evidence |
| --- | --- | --- | --- | --- |
| `vue` | `3.5.39` | MIT | SPA framework for Power Pages shell | `npm view vue version license homepage repository.url` |
| `vite` | `8.1.4` | MIT | local dev/build tool | `npm view vite version license homepage repository.url`; Node engine `^20.19.0 || >=22.12.0` |
| `@vitejs/plugin-vue` | `6.0.7` | MIT | Vue single-file component support | `npm view @vitejs/plugin-vue version license peerDependencies engines` |
| `typescript` | `5.9.3` | Apache-2.0 | typed source checks | `npm view typescript dist-tags version versions --json`; TypeScript `7.0.2` is the npm latest tag but is not compatible with `vue-tsc@3.3.7` because `typescript/lib/tsc` is not exported |
| `vue-tsc` | `3.3.7` | MIT | Vue type checking | `npm view vue-tsc version license dependencies peerDependencies engines` |

## Accepted ODK Packages

| Package | Version | License | Purpose | Evidence |
| --- | --- | --- | --- | --- |
| `@getodk/web-forms` | `1.0.0` | Apache-2.0 | ODK-style web renderer | `npm view @getodk/web-forms version license dependencies peerDependencies dist.unpackedSize time.modified`; repository `getodk/central-frontend`; peer `vue ^3.5.29` |
| `@getodk/xforms-engine` | `1.0.0` | Apache-2.0 | XForms computation/runtime semantics | `npm view @getodk/xforms-engine version license dependencies peerDependencies dist.unpackedSize time.modified`; repository `getodk/central-frontend`; peer `solid-js ^1.9.7` |

## Compatibility Notes

- Local Node validated for this slice: `v24.18.0`; local npm: `11.16.0`.
- Current Vite and Vue engine requirement is satisfied by local Node.
- ODK packages declare Node `^24.16.0` and npm `11`; Node `v24.18.0` satisfies this requirement.
- `@getodk/web-forms` depends on Vue peer `^3.5.29`; pinned Vue `3.5.39` satisfies it.
- `@getodk/xforms-engine` includes `solid-js` as a dependency and also declares peer `solid-js ^1.9.7`; install output must be checked for unmet peer warnings.
- ODK packages were modified on npm on 2026-07-03 and point to `getodk/central-frontend`, so this is an emerging package path and must be validated with a build before runtime integration.
- `npm install` completed with `found 0 vulnerabilities` and no ODK Node engine warning under Node `v24.18.0`.
- `npm audit --audit-level=moderate` completed with `found 0 vulnerabilities`.
- `npm run build` completed successfully after pinning TypeScript to `5.9.3`.
- ODK runtime integration build on 2026-07-10 completed successfully, but Vite/Rolldown reported direct `eval` usage inside `node_modules/@getodk/web-forms/dist/index-Cg9qvMI9.js` and large output chunks. Treat this as an accepted upstream-package risk for the proof of concept, not as TACATDP application code. Revisit chunking and content-security-policy impact before production hardening.
- Power Pages code-site upload initially failed because the target Dataverse organization blocks `.js` attachments. The safer proof-of-concept response is to emit browser module chunks as `.mjs`, not to weaken the organization-wide blocked attachment list.
- `pac pages upload-code-site --siteName "TACATDP Monitoring Tool"` created a second `powerpagesite` with the same name instead of updating the public `https://tacatdp.powerappsportals.com/` site. Corrective deployment used `pac pages download --webSiteId fccc0cc6-7f5e-4885-aeb8-2272e68130a3 --modelVersion Enhanced`, patched that uploadable package, then uploaded with `pac pages upload --modelVersion Enhanced`.
- ODK Web Forms must be registered with `webFormsPlugin` at Vue bootstrap. Directly rendering `OdkWebForm` without `createApp(...).use(webFormsPlugin)` can leave the runtime blank before the `loaded` event.
- ODK Web Forms rejects duplicate body controls bound to the same reference. The rich MVP seed must not use repeated section wrappers such as `<group ref="/data">`; unbound `<group>` sections are acceptable, while individual questions bind to unique `/data/...` nodes. The source and hosted validators now check for duplicate body refs before browser testing.
- The host SPA must not style ODK renderer descendants with generic selectors. ODK Web Forms imports Roboto, PrimeFlex, ODK global styles, component styles, and installs a PrimeVue theme through `webFormsPlugin`; TACATDP shell CSS must be scoped to shell classes and mount the renderer in an `odk-runtime-host` boundary.
- The ODK Web Forms package declares Apache-2.0. TACATDP can hide the visible `Powered by ODK` runtime footer for the client-facing MVP with a scoped `.odk-runtime-host .powered-by-wrapper` override, while retaining package/license documentation in project artifacts. Do not edit files under `node_modules`.
- ODK Web Forms hardcodes the English submit button through `odk_web_forms.submit.label = "Send"` and exposes no reviewed label prop in `@getodk/web-forms@1.0.0`. For the TACATDP MVP, relabel only the scoped footer action button from `Send` to `Submit` after render and with a mutation observer, preserving the original ODK submit event path.
- Renderer spacing should be host-scoped. Use `.odk-runtime-host`, `.odk-runtime-host .form-wrapper`, and `.odk-runtime-host .footer` for outer spacing around the form and after the submit action; do not add broad selectors for `button`, `input`, `label`, `select`, or `textarea`.
- Submit troubleshooting must start from observed evidence. The local ODK Web Forms bundle inspected on 2026-07-11 emits `submit`/`submitChunked` events and the bundled PrimeVue button defaults to `type="button"`, so a Send click that appears to jump/reload is not automatically a native browser form submit. Verify the hosted build marker, runtime click diagnostic, ODK submit-event diagnostic, Dataverse write diagnostic, and row counts before changing submission code.
- Power Pages can serve cached site metadata/web files after upload. Microsoft documents server-side cache behavior and cache clearing through design studio preview or `/_services/about`; use those before concluding that an uploaded bundle is the one currently running in the signed-in browser.

## Current Slice Decision

The SPA foundation initially avoided package installation and ODK dependency import. This review accepts the pinned package set and confirms the first install/build/security gate. Runtime proof now imports `OdkWebForm` and renders the assigned XForm XML; Dataverse submit mapping remains a separate slice.

- package metadata and scripts,
- source layout,
- mobile-first shell,
- Power Pages `/_api` client,
- local draft adapter,
- validation script.

## Required Verification After Install

```bash
cd powerpages/webforms-spa
npm install
npm run build
```

Also rerun from the repository root:

```bash
python3 scripts/validate-webforms-spa-foundation.py
python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env
```

For hosted submit diagnostics, open the signed-in site and confirm build `submit-diagnostics-20260711-001` appears before retesting ODK Send.

## References to Check Before Installing

- Vite guide: `https://vite.dev/guide/`
- Vue TypeScript guide: `https://vuejs.org/guide/typescript/overview.html`
- Power Pages Web API overview: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview`
- Power Pages HTTP/CSRF guidance: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-http-requests-handle-errors`
- ODK Web Forms source/package context: `https://github.com/getodk/web-forms`
- ODK Central Frontend source/package context: `https://github.com/getodk/central-frontend`
