# Power Apps Import Recovery

## Finding

`ErrOpeningDocument_UnknownError` occurred after generated Phase 3 screen/component YAML was promoted into live `app-src/Src/`.

The generated YAML passed the static PA YAML schema after syntax fixes, but that was not enough to make it a reliable import/open artifact. Microsoft documents `*.pa.yaml` source files as read-only/source-control artifacts for review, and external editing is supported through Power Platform Git Integration. The Power Platform CLI `pac canvas pack/unpack` commands are preview/deprecated, and packed apps can either load from YAML or ignore YAML depending on pack options.

## Decision

Keep `app-src/Src/` as the Studio-exported live source baseline:

- `app-src/Src/App.pa.yaml`
- `app-src/Src/_EditorState.pa.yaml`
- `app-src/Src/Screen1.pa.yaml`

Keep generated Phase 3 assets as maker/reference artifacts only:

- `artifacts/powerapps/phase3-scaffolds/components/*.pa.yaml`
- `artifacts/powerapps/phase3-scaffolds/screens/*.pa.yaml`
- `artifacts/powerapps/phase3-scaffolds/phase3-canvas-yaml-pack.json`

Do not manually promote generated scaffold YAML into `app-src/Src/` again unless the change is round-tripped and normalized by Power Apps Studio, Power Platform Git Integration, or a verified `pac canvas pack --layout SourceCode` workflow.

## Safe import path now

Use the current app package/source as the baseline import target. If packing from this repo with Power Platform CLI, prefer a recovery pack that does not force the app to load from generated YAML:

```powershell
pac canvas pack `
  --sources app-src `
  --msapp build/TACATDP.msapp `
  --layout SourceCode `
  --disable-load-from-yaml `
  --overwrite
```

Then open/import the `.msapp` in Power Apps Studio and apply Phase 3 scaffolds through the maker workflow in `docs/phase-3-maker-runbook.md`.

## Phase 3 path after import is stable

1. Import/open the baseline app successfully.
2. Create components and screens in Power Apps Studio using `artifacts/powerapps/phase3-scaffolds/` as the blueprint.
3. Save, export/download, and unpack from Studio or Git Integration.
4. Commit the Studio-normalized source, not handwritten generated source.
5. Only then treat promoted screens/components as importable source.
