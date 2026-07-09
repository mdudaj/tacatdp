# Implementation Tasks: Canvas Metadata Renderer MVP

## Build tasks

| Task | Output | Depends on |
| --- | --- | --- |
| CANVAS-T01 | Create Canvas app shell in dev and add it to `tacatdp_prototype`. | Deployed schema and seed. |
| CANVAS-T02 | Add Dataverse data sources for all MVP tables. | CANVAS-T01. |
| CANVAS-T03 | Build assigned forms gallery. | CANVAS-T02. |
| CANVAS-T04 | Build history screen for selected form/version. | CANVAS-T03. |
| CANVAS-T05 | Load selected form metadata into collections. | CANVAS-T04. |
| CANVAS-T06 | Render text, integer, decimal, date fields. | CANVAS-T05. |
| CANVAS-T07 | Render select one and select many from `Choices`. | CANVAS-T05. |
| CANVAS-T08 | Implement draft save to `Submissions` and `SubmissionAnswers`. | CANVAS-T06, CANVAS-T07. |
| CANVAS-T09 | Implement required validation and submit status transition. | CANVAS-T08. |
| CANVAS-T10 | Implement history reopen and edit-until-locked display mode. | CANVAS-T09. |
| CANVAS-T11 | Implement attachment subflow for `SubmissionFiles`. | CANVAS-T08. |
| CANVAS-T12 | Implement GPS capture or explicitly defer it. | CANVAS-T08. |
| CANVAS-T13 | Verify mobile layout, accessibility labels, and error handling. | CANVAS-T03 through CANVAS-T12. |
| CANVAS-T14 | Document formulas, known delegation warnings, and verification results. | CANVAS-T13. |

## Recommended build order

1. Assigned forms.
2. History.
3. Metadata load.
4. Field renderer without writes.
5. Draft save.
6. Submit.
7. Edit until locked.
8. Attachment.
9. GPS if time allows.
10. Verification and solution packaging.

## Stop conditions

Stop and reassess if:

- assigned forms cannot be filtered without a delegation issue;
- the assigned user cannot read/write the MVP tables;
- attachment upload cannot be made to work in a Dataverse form context;
- Canvas formulas become large enough that the renderer is no longer reviewable.
