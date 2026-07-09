# Implementation-Ready Slice: July 7 Canvas Renderer

## Slice statement

One published TACATDP field visit form is assigned to one Dataverse user and rendered dynamically from Dataverse metadata in a single Canvas app. The user can open the assigned form, create a draft, answer seeded questions, attach one file/photo, capture GPS when available, submit, reopen submitted records, and view their submission history. Locked submissions are read-only.

## Delivered artifacts

- `app-src-metadata-renderer/README.md`: maker handoff for the renderer slice.
- `app-src-metadata-renderer/Src/App.pa.yaml`: app start and global state scaffold.
- `app-src-metadata-renderer/Src/AssignedFormsScreen.pa.yaml`: assigned published forms screen.
- `app-src-metadata-renderer/Src/HistoryScreen.pa.yaml`: user submission history and new draft flow.
- `app-src-metadata-renderer/Src/RunnerScreen.pa.yaml`: metadata load, visible seeded fields, save draft, review navigation, and GPS capture scaffold.
- `app-src-metadata-renderer/Src/ReviewScreen.pa.yaml`: review summary and submit action for the seeded MVP form.
- `app-src-metadata-renderer/Src/AttachmentScreen.pa.yaml`: attachment capture placeholder for a Dataverse edit form.
- `docs/canvas-renderer-mvp/formula-catalog.md`: copy/paste formula source of truth for Studio implementation.
- `docs/canvas-renderer-mvp/design-system.md`: app shell, identity header, assigned-form display, and generated YAML constraints.
- `scripts/validate-canvas-renderer-slice.py`: local readiness check for required files and MVP behavior markers.

## Current implementation boundary

This is a Studio-ready scaffold, not a claim that PAC can import raw YAML directly. Microsoft marks Canvas YAML source as preview, and the installed PAC CLI reports `pac canvas validate` as unsupported. The authoritative implementation step is to build these screens in Power Apps Studio, save the app, run App Checker, then export/unpack the Studio-normalized source.

## What is ready now

- Dataverse schema and seed data are already deployed in dev.
- Renderer screen flow is defined.
- MVP formulas are defined against the deployed metadata tables.
- Readiness validation can run locally without secrets.
- Existing fixed-screen `app-src/` is untouched.

## Maker build order

1. Open the dev environment and create or open the TACATDP Canvas app.
2. Add the ten Dataverse data sources.
3. Set `App.StartScreen` and `App.OnStart` from `app-src-metadata-renderer/Src/App.pa.yaml`.
4. Create `AssignedFormsScreen`, `HistoryScreen`, `RunnerScreen`, and `AttachmentScreen`.
5. Add galleries and buttons using the formulas in `docs/canvas-renderer-mvp/formula-catalog.md`.
6. In `RunnerScreen`, use the seeded visible controls for the share candidate and keep `QuestionsGallery` as the metadata proof point.
7. In `ReviewScreen`, show the captured values and submit only after review.
8. In `AttachmentScreen`, add an edit form bound to `SubmissionFiles` and place the Attachments control inside the form.
9. Run App Checker and Monitor; resolve delegation warnings or document accepted warnings.
10. Test with `john.mduda@mshirikacorp.onmicrosoft.com` or the configured seeded assignment user.
11. Save, publish, share with the assigned user, and export/unpack the app source.

## Demo script

1. Sign in through standard Power Apps / Entra authentication.
2. Confirm the assigned TACATDP MVP field visit form appears.
3. Start a new draft.
4. Enter text, integer, decimal, date, select one, select many, and attachment answers.
5. Capture GPS if browser/device permission is available.
6. Save draft, leave the runner, reopen the draft from history.
7. Select Review, confirm the summary, then submit the record.
8. Reopen the submitted record from history and edit it.
9. Set the submission to `Locked` in Dataverse and confirm the app renders read-only.

## Deferred deliberately

- Full XLSForm parser/compiler.
- Repeat groups and nested repeats.
- Complex XPath-style relevance and constraints.
- Offline-first sync.
- Barcode.
- Admin publishing UI.
- Dashboards and analytics exports.


## v13 share-candidate boundary

The v13 package intentionally prioritizes a demonstrable vertical slice over full renderer generality. It proves authentication, assignment, draft save, answer persistence, review, submit, history, and GPS scaffolding for one seeded form. The next iteration should replace the visible seeded inputs with a reusable metadata field row once Studio-normalized source is available.


## v14 shell and entry revision

The entry screen now separates title, signed-in identity, screen state, and assigned-form action. The assigned form displays both the form name and version. All MVP screens include a top signed-in-user row so operators always know which Power Apps / Entra identity is active.
