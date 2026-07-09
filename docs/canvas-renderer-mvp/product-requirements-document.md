# PRD: Canvas Metadata Renderer MVP

## Goal

Deliver the Canvas runtime for the already deployed Dataverse MVP schema:

> A signed-in user opens the app, sees one assigned published TACATDP form, captures data through a metadata-rendered form, saves a draft, submits it, edits until locked, attaches one file/photo, captures GPS if quick enough, and views submission history.

## Users

- Data collector: captures and submits assigned form data.
- Project manager/admin: verifies that seeded form assignments are visible to the intended user.
- Reviewer/data manager: checks submission status, answers, attachment, and history.
- Developer/maker: builds the generic runtime and validates the vertical slice.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| CANVAS-RQ-01 | Use Power Apps / Entra authentication only; no custom login. | P0 |
| CANVAS-RQ-02 | Show assigned forms by filtering `FormAssignments` for active rows assigned to `User().Email` and/or current Dataverse user lookup. | P0 |
| CANVAS-RQ-03 | Show the seeded published form `TACATDP-MVP-001` / version `2026-07-07-v1`. | P0 |
| CANVAS-RQ-04 | Load ordered sections and questions from Dataverse metadata. | P0 |
| CANVAS-RQ-05 | Render text, integer, decimal, date, select one, select many, file/photo attachment, and GPS question types. | P0 |
| CANVAS-RQ-06 | Load choices from the `Choices` table, not Power Fx `Choices()`. | P0 |
| CANVAS-RQ-07 | Enforce required validation for seeded required rules before submit. | P0 |
| CANVAS-RQ-08 | Save Draft by upserting `Submissions` with status `Draft` and answer rows in `SubmissionAnswers`. | P0 |
| CANVAS-RQ-09 | Submit by validating required answers and setting status to `Submitted`. | P0 |
| CANVAS-RQ-10 | Allow edits when status is `Draft` or `Submitted`; render locked submissions read-only. | P0 |
| CANVAS-RQ-11 | Persist file/photo through `SubmissionFiles`. | P0 |
| CANVAS-RQ-12 | Store GPS point as JSON in `SubmissionAnswers.ValueJson` when implemented. | P1 |
| CANVAS-RQ-13 | Show current user's submission history for the selected form/version. | P0 |
| CANVAS-RQ-14 | Surface clear save/submit errors without losing entered answers. | P0 |

## Non-functional requirements

- Keep assignment/history queries delegable.
- Keep Power Fx formulas reviewable and grouped by screen/control.
- Avoid local collections for large tables; use collections only for the selected form's small metadata and in-progress answers.
- Avoid page-local styling that conflicts with `docs/design-system.md`.
- Keep mobile-first layout usable in Power Apps mobile.
- Do not add secrets or environment identifiers to source.

## Seed data target

- Form: `TACATDP-MVP-001` / `TACATDP MVP Field Visit`.
- Version: `2026-07-07-v1`.
- Assignment: `john.mduda@mshirikacorp.onmicrosoft.com`.
- Questions: `farmer_name`, `farmer_age`, `land_size_acres`, `visit_date`, `primary_crop`, `support_needed`, `farm_photo`, `gps_point`.

## Deferred

- Full XLSForm compiler.
- Repeat groups and nested repeats.
- Complex relevance/constraint/calculation parsing.
- Offline-first sync.
- Barcode.
- Admin publishing UI.
- Dashboards.
