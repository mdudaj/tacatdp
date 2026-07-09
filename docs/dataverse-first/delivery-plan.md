# Dataverse-First Delivery Plan

## Current delivery target

Deliver the July 7, 2026 MVP from `docs/mvp-july-7.md`:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

## Phase 0: Confirm dev environment

Completed enough to proceed with development planning:

1. Dataverse environment is available.
2. Service principal can authenticate.
3. `pac solution list` succeeds.
4. `pac org who` succeeds.

Environment-specific IDs and secrets must stay outside source control.

## Phase 1: Create the MVP solution and tables

After explicit approval for dev Dataverse writes, create or prepare a dev solution containing only the MVP tables:

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

Do not create the full multi-project schema before the MVP vertical slice works.

## Phase 2: Seed one form

Seed one published TACATDP form version with a small manually reviewed JSON/YAML artifact or manual import:

1. one `Forms` row;
2. one `FormVersions` row with published status;
3. a small set of `Sections`;
4. MVP-supported `Questions`;
5. `Choices` for select one / select many fields;
6. simple `ValidationRules`;
7. one `FormAssignments` row for the test user.

Do not build the full XLSForm compiler in this phase.

## Phase 3: Build the Canvas metadata renderer

Implement generic screens/components:

1. Assigned forms list.
2. Submission history for selected form.
3. Form runner shell.
4. Field renderer for text, integer, decimal, date, select one, select many, file/photo attachment, and GPS if quick enough.
5. Save Draft and Submit actions.
6. Locked read-only behavior.

## Phase 4: Verify vertical slice

Verify:

1. user sees only assigned published forms;
2. user opens assigned form;
3. app renders questions from metadata;
4. required/relevance/constraint subset works;
5. draft saves;
6. submit changes status;
7. submitted record remains editable until locked;
8. locked record is read-only;
9. attachment persists;
10. history shows the user's own submissions.

## Deferred phases

After MVP validation, plan:

- XLSForm-to-Dataverse metadata compiler;
- repeat groups and nested repeats;
- advanced ODK/XPath expression support;
- offline-first sync;
- barcode;
- admin publishing UI;
- version migration;
- dashboards/export projections;
- richer review/locking workflow.

## Dataverse schema delivery artifacts

Use `docs/dataverse-schema-cli/` for the reviewed CLI/Web API schema setup requirements, ADR, user stories, checklist, delivery plan, and verification notes.

## Canvas renderer artifacts

Use `docs/canvas-renderer-mvp/` for the systematic Canvas implementation plan after the Dataverse schema and seed are verified.
