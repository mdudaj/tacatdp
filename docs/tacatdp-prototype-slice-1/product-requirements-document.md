# PRD: July 7 Metadata-Driven MVP Slice

## Problem

TACATDP needs a working MVP quickly, but the project should not spend the first slice on a full XLSForm compiler, repeat engine, or 33 fixed Canvas screens. The first implementation should prove the generic platform path with the smallest useful data collection loop.

## Goal

Deliver one vertical slice:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

## Users

- Data collector: sees assigned forms, captures data, saves draft, submits, edits until locked, attaches a file/photo, and sees history.
- Admin/project manager: seeds one published form and assignment.
- Developer/maker: builds the MVP tables and Canvas renderer.
- Reviewer/data manager: validates the submitted data and status behavior.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| MVP-RQ-01 | Use Power Apps / Entra authentication; do not build custom login. | P0 |
| MVP-RQ-02 | Show assigned forms from `FormAssignments`, filtered by current user/email and published active form version. | P0 |
| MVP-RQ-03 | Render one seeded form dynamically from `Forms`, `FormVersions`, `Sections`, `Questions`, `Choices`, and `ValidationRules`. | P0 |
| MVP-RQ-04 | Support text, integer, decimal, date, select one, and select many fields. | P0 |
| MVP-RQ-05 | Support one photo/file attachment linked to a question/submission. | P0 |
| MVP-RQ-06 | Support GPS point only if fast enough after the core slice works. | P1 |
| MVP-RQ-07 | Save drafts to `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`. | P0 |
| MVP-RQ-08 | Submit by changing status to `Submitted`. | P0 |
| MVP-RQ-09 | Allow editing when status is `Draft` or `Submitted`; block editing when `Locked`. | P0 |
| MVP-RQ-10 | Show the current user's submission history for the selected form. | P0 |
| MVP-RQ-11 | Seed one form manually or from a small JSON/YAML artifact; defer full XLSForm compiler. | P0 |
| MVP-RQ-12 | Implement only required true/false, relevance depending on one prior answer, and simple numeric/text constraints. | P0 |

## MVP Dataverse tables

- `Forms`
- `FormVersions`
- `Sections`
- `Questions`
- `Choices`
- `ValidationRules`
- `FormAssignments`
- `Submissions`
- `SubmissionAnswers`
- `SubmissionFiles`

Do not create a custom `Users` table for the MVP unless profile metadata becomes necessary.

## Generic answer storage

`SubmissionAnswers` uses:

- `Submission`;
- `Question`;
- `ValueText`;
- `ValueNumber`;
- `ValueDecimal`;
- `ValueDate`;
- `ValueBoolean`;
- `ValueJson`.

For MVP, select-many can be stored in `ValueJson`. Normalize later if analytics require it.

## Explicitly deferred

- full XLSForm parser/compiler;
- repeat groups;
- nested repeats;
- complex XPath expressions;
- offline-first sync;
- barcode;
- admin publishing UI;
- version migration;
- dashboards;
- locking workflow beyond the simple status field.

## Non-functional requirements

- No secrets, tenant IDs, environment IDs, or credentials in source.
- Dev Dataverse writes require explicit approval.
- Keep the metadata seed small and reviewable.
- Keep Canvas formulas readable enough for hand review.
- Preserve accessible labels, helper/error text, focus order, and touch-safe controls.
