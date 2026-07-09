# Requirements Traceability: Canvas Metadata Renderer MVP

| Requirement | Story | Acceptance criteria | Dataverse tables | Notes |
| --- | --- | --- | --- | --- |
| CANVAS-RQ-01 | CANVAS-US-01 | AC-01 | system user context | Uses Power Apps auth and `User()`. |
| CANVAS-RQ-02 | CANVAS-US-01 | AC-02 | `FormAssignments`, `FormVersions`, `Forms` | Filter by active assignment and published version. |
| CANVAS-RQ-03 | CANVAS-US-03 | AC-03 | `Forms`, `FormVersions` | Seeded form/version. |
| CANVAS-RQ-04 | CANVAS-US-03 | AC-03 | `Sections`, `Questions` | Ordered metadata load. |
| CANVAS-RQ-05 | CANVAS-US-03 | AC-04 | `Questions`, `SubmissionAnswers`, `SubmissionFiles` | MVP field types only. |
| CANVAS-RQ-06 | CANVAS-US-03 | AC-04 | `Choices` | Do not use Power Fx `Choices()` for form options. |
| CANVAS-RQ-07 | CANVAS-US-05 | AC-05 | `ValidationRules` | Required rules first. |
| CANVAS-RQ-08 | CANVAS-US-04 | AC-06, AC-12 | `Submissions`, `SubmissionAnswers` | Draft persistence. |
| CANVAS-RQ-09 | CANVAS-US-05 | AC-07 | `Submissions`, `SubmissionAnswers` | Submit status transition. |
| CANVAS-RQ-10 | CANVAS-US-06 | AC-08 | `Submissions` | Lock behavior from status. |
| CANVAS-RQ-11 | CANVAS-US-07 | AC-09 | `SubmissionFiles` | Attachment form path. |
| CANVAS-RQ-12 | CANVAS-US-08 | AC-10 | `SubmissionAnswers` | GPS JSON. |
| CANVAS-RQ-13 | CANVAS-US-09 | AC-07, AC-12 | `Submissions` | History. |
| CANVAS-RQ-14 | CANVAS-US-10 | AC-05, AC-06, AC-07 | all write tables | Error handling around `Patch`. |

## Supporting artifacts

- Requirements note: `requirements-note.md`
- Implementation tasks: `implementation-tasks.md`
- Screen/formula blueprint: `screen-flow-and-formula-blueprint.md`
- Delivery checklist: `delivery-checklist.md`
