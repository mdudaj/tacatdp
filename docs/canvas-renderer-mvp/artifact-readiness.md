# Artifact Readiness: Canvas Metadata Renderer MVP

## Ready

- Dataverse schema deployed and verified.
- Seed form/version/section/questions/choices/rules/assignment deployed and verified.
- Renderer contract exists at `schemas/dataverse/form-renderer-contract.json`.
- Canvas delivery requirements and acceptance criteria are documented in this folder.
- Implementation-ready Canvas scaffold exists under `app-src-metadata-renderer/`.
- Formula catalog exists at `docs/canvas-renderer-mvp/formula-catalog.md`.
- Local slice validator passes with `python3 scripts/validate-canvas-renderer-slice.py`.
- Scaffold YAML parses locally.

## Ready for Power Apps Studio

- Build four screens: assigned forms, history, runner, and attachment capture.
- Add the ten Dataverse MVP tables as data sources.
- Paste/adapt formulas from `docs/canvas-renderer-mvp/formula-catalog.md`.
- Use the Dataverse edit form pattern for `SubmissionFiles` because the attachment control must live inside a form.
- Save from Studio, run App Checker, publish, share, and test with the seeded assignment.

## Needed before implementation sign-off

- Confirm the maker account can create/update Canvas apps in the target environment.
- Confirm the assigned user has app sharing and Dataverse table privileges.
- Confirm actual App Checker and Monitor output after the Studio build.
- Confirm whether GPS is accepted for the first demo or left as a visible optional capture.

## Not ready / deferred

- Full XLSForm compiler.
- Repeat groups.
- Nested repeats.
- Complex XPath-style expressions.
- Offline-first sync.
- Production ALM.
- Dashboards and analytics exports.
