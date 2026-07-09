# Power Pages WebForms SPA Package Review

Status: prepared; package installation not yet approved. Version ranges in `powerpages/webforms-spa/package.json` are provisional and must be checked against the current package registries and upstream documentation before install.

## Policy

Do not run `npm install` or add lockfiles until this review is accepted. Package installation changes the local supply-chain state and is a separate approval gate.

## Proposed Foundation Packages

| Package | Purpose | Source | Notes |
| --- | --- | --- | --- |
| `vue` | SPA framework for Power Pages shell | Vue project | Required before ODK Web Forms integration. |
| `vite` | local dev/build tool | Vite project | Builds the compiled assets for later `pac pages upload-code-site`. |
| `@vitejs/plugin-vue` | Vue single-file component support | Vite project | Needed for `.vue` files. |
| `typescript` | typed source checks | TypeScript project | Keeps Power Pages API contracts explicit. |
| `vue-tsc` | Vue type checking | Vue tooling | Runs type checks over `.vue` files. |

## Proposed ODK Packages for Later Review

| Package | Purpose | Gate |
| --- | --- | --- |
| `@getodk/web-forms` | ODK-style web renderer | Review exact current version, license, published package state, and Central Frontend usage before install. |
| `@getodk/xforms-engine` | XForms computation/runtime semantics | Review exact current version, license, and API shape before install. |

## Current Slice Decision

The SPA foundation intentionally avoids package installation and ODK dependency import. It provides:

- package metadata and scripts,
- source layout,
- mobile-first shell,
- Power Pages `/_api` client,
- local draft adapter,
- validation script.

## References to Check Before Installing

- Vite guide: `https://vite.dev/guide/`
- Vue TypeScript guide: `https://vuejs.org/guide/typescript/overview.html`
- Power Pages Web API overview: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview`
- Power Pages HTTP/CSRF guidance: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-http-requests-handle-errors`
- ODK Web Forms source/package context: `https://github.com/getodk/web-forms`
- ODK Central Frontend source/package context: `https://github.com/getodk/central-frontend`
