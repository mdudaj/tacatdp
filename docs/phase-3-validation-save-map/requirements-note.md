# Phase 3 Validation and Save Map Requirements Note

## Bounded outcome

Prepare implementation-ready requirements for the TACATDP Phase 3 Canvas app validation and save-map slice before any further Canvas source or Power Fx implementation.

This slice is documentation and protocol artifact work only. It must guide the next implementation slice without connecting to production SharePoint, publishing/importing the app, or changing the current importable Canvas source.

## Evidence reviewed

- `artifacts/powerapps/phase3-preview/summary.json`: 33 chronological screens, 393 field rows, 226 scaffold-required rows, 7 hidden ODK metadata fields, and `Screen_<two-digit-order>_<semantic_name>.pa.yaml` naming.
- `app-src/Src/Screen_*.pa.yaml`: native-control import candidate with label/input/help rows, beginning at `Screen_01_demographics` and `Customer ID`.
- `schemas/xlsform-to-list-mapping.csv`: 292 mapped XLSForm rows across 10 save targets, including 20 multi-select child rows and 72 production-cost line rows.
- `schemas/sharepoint-lists-schema.json`: target Microsoft Lists schema for submissions, child rows, reference lists, section lists, beneficiaries, production income, and production cost lines.
- `docs/design-system.md`: one field per row, visible labels, helper/error text, section hierarchy, accessibility, touch targets, and validation summary expectations.
- `docs/phase-3-requirements.md`: guided multi-section flow, `SubmissionKey`, draft/saved/submitted/save-failed states, visible-only validation, reference data, and Microsoft Lists save strategy.
- `docs/phase-3-delivery-plan.md`: placeholder-first implementation, formula naming, save orchestration, and verification scenarios.
- `docs/phase-3-maker-runbook.md`: Power Apps Studio maker workflow, component wiring, placeholder rules, App Checker, Monitor, and manual QA.
- `docs/powerapps-import-recovery.md`: import-safe native-control strategy and caution against assuming schema-valid generated YAML will open in Studio.

## Model route evidence

- Planning route: GitHub `gpt-5-mini`, role `planner`, source `skillpacks/tacatdp.yml`.
- Delegated planning agent: `tacatdp-planner`, model `gpt-5-mini`, produced the first PRD/story/readiness recommendations for this artifact pack.
- Implementation route for the next slice: `openai_codex` `gpt-5.4-mini` for routine code implementation after these artifacts pass the protocol gate.
- Escalation route: use a higher-capability code or review model only if importability, schema safety, production-risk, or repeated-failure issues recur.

## Requirements summary

| ID | Requirement | Evidence | Priority |
| --- | --- | --- | --- |
| VSM-RQ-01 | Each of the 33 Phase 3 screens must have a declared validation behavior before implementation. | `summary.json`, `app-src/Src/Screen_*.pa.yaml` | P0 |
| VSM-RQ-02 | Required validation must apply only to visible/relevant fields; hidden fields must not block Continue, Save Draft, or Submit. | `docs/phase-3-requirements.md`, `schemas/xlsform-to-list-mapping.csv` | P0 |
| VSM-RQ-03 | Every visible required field must show an inline error near the field and contribute a row to the section validation summary when blocked. | `docs/design-system.md`, `docs/phase-3-maker-runbook.md` | P0 |
| VSM-RQ-04 | Each screen must declare its save target lists and child-row behavior before Power Fx formulas are added. | `schemas/xlsform-to-list-mapping.csv`, `schemas/sharepoint-lists-schema.json` | P0 |
| VSM-RQ-05 | Milestone implementation must use placeholder collections first and leave a clear seam for later Microsoft Lists replacement. | `docs/milestone-1-placeholder-plan.md`, `docs/phase-3-delivery-plan.md` | P0 |
| VSM-RQ-06 | ODK metadata fields from `start` through `username` must remain absent from the visible UI; Power Apps equivalents may be captured automatically later. | `summary.json`, current ordered source | P0 |
| VSM-RQ-07 | Screen filenames and navigation order must remain chronological and reviewable. | `summary.json`, `app-src/Src/_EditorState.pa.yaml` | P0 |
| VSM-RQ-08 | Save failures must be visible and must not be represented as successful draft/save/submit states. | `docs/phase-3-requirements.md`, `docs/design-system.md` | P0 |
| VSM-RQ-09 | Multi-select answers must be normalized into `TACATDP_MultiSelectAnswers`; production-cost details must be normalized into `TACATDP_ProductionCostLines`. | `schemas/xlsform-to-list-mapping.csv` | P0 |
| VSM-RQ-10 | Large reference data, especially cascading locations, must use delegation-safe reference filters rather than loading all values at app start. | `docs/phase-3-requirements.md`, `skills/power-platform-canvas-apps` | P1 |

## Implementation boundary

The next implementation slice may add placeholder validation state, section validation summaries, and save-map formula seams. It must not:

- connect to production SharePoint/Microsoft Lists without explicit approval;
- publish or import into a production Power Apps environment without explicit approval;
- replace the known importable native-control strategy with custom generated components;
- reintroduce visible ODK metadata fields;
- change schema contracts without updating mapping artifacts and protocol evidence.

