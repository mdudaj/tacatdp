# Product Requirements Document: Dataverse-First Dynamic Data Collection MVP

## Context and evidence

TACATDP now has working Power Platform service-principal access to the Dataverse development environment. The next deliverable should use that access to prove a small metadata-driven data collection platform instead of continuing with a generated one-screen-per-form approach.

Evidence:

- `docs/mvp-july-7.md`;
- `docs/app-vision.md`;
- `docs/multi-project-monitoring/form-renderer-ux.md`;
- `schemas/dataverse/form-renderer-contract.json`;
- PAC validation: service-principal `pac solution list` and `pac org who` succeeded against the Dataverse org.

## Problem

The project needs an MVP quickly, but the full ODK-style platform is too broad for the July 7 target. A TACATDP-specific app with many fixed screens would deliver visible UI but would not prove the platform architecture. A full XLSForm compiler, repeat engine, offline sync, and admin publishing UI would overrun the MVP.

## Goal

Deliver the first vertical slice of a Dynamic Data Collection Platform powered by Dataverse:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

## Users / actors

- Data collector: signs into Power Apps, sees assigned forms, captures data, saves drafts, submits, edits until locked, attaches evidence, and views history.
- Project manager/admin: seeds one published form version and assigns it to a user.
- Developer/maker: builds the Dataverse MVP tables and the Canvas metadata renderer.
- Reviewer/data manager: verifies submissions, status, attachment, and history behavior.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| MVP-RQ-01 | Use Power Apps / Entra authentication; do not build custom login. | P0 |
| MVP-RQ-02 | Show assigned forms from `FormAssignments`, filtered by the current Dataverse user/email and active published form version. | P0 |
| MVP-RQ-03 | Render one published form from Dataverse metadata using `Forms`, `FormVersions`, `Sections`, `Questions`, `Choices`, and `ValidationRules`. | P0 |
| MVP-RQ-04 | Support text, integer, decimal, date, select one, and select many question types. | P0 |
| MVP-RQ-05 | Support one photo/file attachment linked to a submission/question. | P0 |
| MVP-RQ-06 | Support GPS point only if it does not endanger the July 7 vertical slice. | P1 |
| MVP-RQ-07 | Save drafts in `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`. | P0 |
| MVP-RQ-08 | Submit a draft by changing submission status to `Submitted`. | P0 |
| MVP-RQ-09 | Allow editing while status is `Draft` or `Submitted`; block editing when status is `Locked`. | P0 |
| MVP-RQ-10 | Show the signed-in user's submission history for the selected form. | P0 |
| MVP-RQ-11 | Seed one form into Dataverse metadata manually or from a small JSON/YAML artifact; do not build the full XLSForm compiler yet. | P0 |
| MVP-RQ-12 | Implement only the July 7 rule subset: required true/false, relevance depending on one prior answer, and simple numeric/text constraints. | P0 |

## Dataverse table requirements

Use these MVP tables:

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

Do not add a custom `Users` table unless profile metadata is needed. Use Dataverse system users and assignment rows referencing user/email.

## Generic answer model

`SubmissionAnswers` stores generic typed values:

- `Submission`;
- `Question`;
- `ValueText`;
- `ValueNumber`;
- `ValueDecimal`;
- `ValueDate`;
- `ValueBoolean`;
- `ValueJson`.

For MVP, select-many can use `ValueJson` to avoid designing repeat answer child rows before the renderer is proven.

## Deferred scope

Defer until after the first working vertical slice:

- full XLSForm parser/compiler;
- repeat groups and nested repeats;
- complex XPath expressions;
- offline-first sync;
- barcode;
- admin publishing UI;
- version migration;
- dashboards;
- locking workflow beyond a simple status field.

## UX requirements

- Assigned forms list first, not a landing page.
- Form runner shows one field per row with visible labels, helper/error text, and clear required markers.
- Save Draft, Submit, and status are visible.
- Locked submissions are readable but not editable.
- History is scannable by form, status, and updated/submitted timestamp.

## Safety and constraints

- No secrets, tenant IDs, environment IDs, or credentials in source.
- No production writes.
- Dev Dataverse writes require explicit approval.
- Package created tables/app in a solution.
- Keep the MVP schema small enough to review manually.

## Acceptance criteria

See `docs/tacatdp-prototype-slice-1/acceptance-criteria.md`.
