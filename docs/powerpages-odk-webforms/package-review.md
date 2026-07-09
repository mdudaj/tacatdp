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

## Current Slice Decision

The SPA foundation initially avoided package installation and ODK dependency import. This review accepts the pinned package set and confirms the first install/build/security gate. Runtime integration remains a separate slice.

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

## References to Check Before Installing

- Vite guide: `https://vite.dev/guide/`
- Vue TypeScript guide: `https://vuejs.org/guide/typescript/overview.html`
- Power Pages Web API overview: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview`
- Power Pages HTTP/CSRF guidance: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-http-requests-handle-errors`
- ODK Web Forms source/package context: `https://github.com/getodk/web-forms`
- ODK Central Frontend source/package context: `https://github.com/getodk/central-frontend`
