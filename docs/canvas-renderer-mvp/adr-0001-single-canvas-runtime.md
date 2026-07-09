# ADR-0001: Build One Metadata-Driven Canvas Runtime

## Status

Accepted for the July 7 MVP.

## Context

The Dataverse MVP schema and seed data are now deployed. The next decision is whether to generate screens for the seeded form or build one generic Canvas runtime that renders metadata.

Generating one screen per form would be faster for a single survey but would not prove the platform direction. The product goal is ODK-style dynamic form delivery on Microsoft Power Platform. The seeded schema already contains `Forms`, `FormVersions`, `Sections`, `Questions`, `Choices`, `ValidationRules`, `FormAssignments`, `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`.

## Decision

Build one Canvas app runtime that renders the seeded published form from Dataverse metadata.

The app will have four primary surfaces:

1. Assigned forms.
2. Submission history.
3. Form runner.
4. Attachment capture.

The runner will render only the MVP question types: text, integer, decimal, date, select one, select many, file/photo attachment, and GPS point if quick enough.

## Consequences

- The first Canvas implementation proves the long-term metadata architecture.
- Dynamic rendering will require more Power Fx state management than static generated screens.
- Attachment handling needs a special path because the Power Apps Attachments control requires a Dataverse/list form context.
- The first slice should avoid advanced expression engines, repeats, and offline sync.

## Rejected options

- Generate a separate Canvas screen for each form: faster but undermines metadata-runtime proof.
- Build full XLSForm compiler first: too broad for the MVP.
- Use SharePoint/Microsoft Lists: current successful Dataverse schema makes this a fallback only.
