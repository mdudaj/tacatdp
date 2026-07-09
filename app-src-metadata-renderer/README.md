# TACATDP Metadata Renderer Canvas Slice

This folder contains the July 7 MVP Canvas renderer scaffold. It is intentionally separate from `app-src/` so the existing generated fixed-screen app remains untouched.

Use this as the implementation target in Power Apps Studio:

1. Create or open the TACATDP Canvas app in the dev environment.
2. Add the ten Dataverse data sources listed in `docs/canvas-renderer-mvp/formula-catalog.md`.
3. Build the four screens in this scaffold: assigned forms, history, runner, and attachment capture.
4. Paste/adapt the formulas from `Src/*.pa.yaml` and `docs/canvas-renderer-mvp/formula-catalog.md`.
5. Save, run App Checker, test with the seeded assignment, and export/unpack the Studio-normalized source.

The scaffold proves the first vertical slice: one assigned published form, dynamic metadata rendering, draft/save/submit/history, edit-until-locked, attachment, and GPS capture.
