# PRD: Dynamic Data Collection Platform Vision and TACATDP MVP

## Context

TACATDP started as one Power Apps survey conversion. The product direction is now a reusable dynamic data collection platform powered by Dataverse, with a Canvas App runtime that renders form metadata instead of generating one app per form.

The July 7, 2026 MVP is intentionally narrow and is defined in `docs/mvp-july-7.md`.

## Problem

A full ODK Central / ODK Collect equivalent requires form authoring, versioning, assignments, runtime rendering, repeats, expression evaluation, offline sync, publishing, monitoring, export, and dashboards. Building all of that before the first end-to-end slice would delay learning.

## MVP goal

Deliver one vertical slice:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

## Long-term goals

| Goal | Direction |
| --- | --- |
| ODK Central-like control plane | Dataverse/admin surfaces for forms, versions, assignments, submissions, export, monitoring, and publishing. |
| ODK Collect-like runtime | One Canvas App runtime for assigned forms, metadata rendering, drafts, submit, edit-until-locked, attachments, and history. |
| Metadata-driven forms | Form definitions are data, not generated app screens. |
| Generic runtime storage | Submissions and answers use generic Dataverse tables first; projections can come later. |
| XLSForm compatibility | Build XLSForm import/compiler after the runtime path is proven. |
| Future ODK parity | Add repeats, richer expressions, offline sync, barcode, and complex media after MVP. |

## MVP Dataverse model

Use small, reviewable table names for the MVP:

- `Forms`;
- `FormVersions`;
- `Sections`;
- `Questions`;
- `Choices`;
- `ValidationRules`;
- `FormAssignments`;
- `Submissions`;
- `SubmissionAnswers`;
- `SubmissionFiles`.

Longer-term `Project`, `Instrument`, `GroupDefinition`, `FieldDefinition`, `VocabularyTerm`, `GroupInstance`, and projection concepts remain valid platform vocabulary, but they should not block the July 7 MVP.

## MVP users / actors

- Data collector: completes assigned forms in Canvas.
- Admin/project manager: seeds one form and assignment.
- Reviewer/data manager: checks submissions and history.
- Developer/maker: builds the MVP Dataverse solution and renderer.

## MVP requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| MP-MVP-01 | Use Entra/Power Apps authentication only. | P0 |
| MP-MVP-02 | Show assigned active published forms. | P0 |
| MP-MVP-03 | Render form sections/questions dynamically from metadata. | P0 |
| MP-MVP-04 | Support text, integer, decimal, date, select one, select many, and one attachment field. | P0 |
| MP-MVP-05 | Support GPS point only if it fits the July 7 delivery window. | P1 |
| MP-MVP-06 | Save drafts and submit using `Draft`, `Submitted`, `Locked` statuses. | P0 |
| MP-MVP-07 | Edit while `Draft` or `Submitted`; block edit when `Locked`. | P0 |
| MP-MVP-08 | Show current user's submission history for the selected form. | P0 |
| MP-MVP-09 | Seed one form manually/from JSON/YAML; defer full XLSForm compiler. | P0 |

## Deferred requirements

- repeat groups and nested repeats;
- full XLSForm parser/compiler;
- complex XPath expression engine;
- offline-first sync;
- barcode;
- admin publishing UI;
- version migration;
- dashboards;
- locking workflow beyond simple status.

## Safety and constraints

- No secrets or tenant-specific credentials in source.
- No production writes.
- Dev Dataverse writes require explicit approval.
- Keep source artifacts reviewable before environment mutation.
