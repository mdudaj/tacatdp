# Delivery Plan: Dynamic Data Collection Platform

## Current MVP target

By July 7, 2026, deliver:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

`docs/mvp-july-7.md` is the canonical near-term scope.

## Phase 1: MVP schema and seed data

After explicit approval for dev Dataverse writes:

1. Create the small MVP tables: `Forms`, `FormVersions`, `Sections`, `Questions`, `Choices`, `ValidationRules`, `FormAssignments`, `Submissions`, `SubmissionAnswers`, `SubmissionFiles`.
2. Seed one TACATDP form manually or from a small JSON/YAML artifact.
3. Publish one form version.
4. Assign it to one test user.

Do not build a full XLSForm compiler in this phase.

## Phase 2: Canvas runtime MVP

Build the generic Canvas runtime surfaces:

1. Assigned forms list.
2. Submission history for selected form.
3. Form runner shell.
4. Field renderer for text, integer, decimal, date, select one, select many, file/photo attachment, and GPS if quick enough.
5. Save Draft.
6. Submit.
7. Edit-until-locked / locked read-only behavior.

## Phase 3: MVP verification

Verify:

1. Entra/Power Apps auth identifies the user.
2. Only assigned active published forms appear.
3. Form metadata renders without hard-coded TACATDP screens.
4. Required, one-prior-answer relevance, and simple constraints work.
5. Draft, submit, edit, lock, attachment, and history work.

## Phase 4: Post-MVP expansion

Only after the vertical slice works, add:

- XLSForm-to-Dataverse compiler;
- repeat groups and nested repeats;
- complex XPath expressions;
- offline-first sync;
- barcode;
- admin publishing UI;
- version migration;
- dashboards and export projections;
- richer review and locking workflow.

## Existing artifacts

The existing multi-project schema and renderer artifacts remain useful as long-term reference, but they should not expand the July 7 MVP. Any implementation task that adds deferred scope must explicitly justify why it is necessary for the vertical slice.
