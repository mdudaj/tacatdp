# TACATDP Artifacts

This folder stores generated and handoff-ready delivery artifacts that support the Power Apps canvas source under `app-src/Src/`.

Recommended organization:

| Folder | Use |
| --- | --- |
| `powerapps/` | Canvas app scaffolds, maker packs, pack/import support files, and Power Apps Studio handoff artifacts. |
| `powerapps/phase3-scaffolds/` | Phase 3 component and screen blueprints for maker-assisted implementation. Keep these out of live `app-src/Src/` until Power Apps Studio or verified Power Platform tooling normalizes them. |
| `sharepoint/` | Microsoft Lists and SharePoint schema/import artifacts when they are generated or exported. |
| `qa/` | Manual QA evidence, App Checker exports, Monitor notes, and pack/import validation results. |

Keep `app-src/Src/` as the active Studio-exported Canvas source. Keep `artifacts/` for generated packs, review references, and validation outputs that should not be mixed into the live Canvas source tree.
