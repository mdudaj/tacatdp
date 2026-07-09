# Research: Canvas Metadata Renderer MVP

## Sources checked

- Microsoft Dataverse connector for Canvas apps: `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-common-data-service`
- Canvas app delegation overview: `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview`
- Power Fx `User()` function: `https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-user`
- Power Fx `Filter`, `Search`, and `LookUp`: `https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-filter-lookup`
- Power Fx `Patch`: `https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-patch`
- Power Apps Attachments control: `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-attachments`
- Power Apps Edit form and Display form controls: `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-form-detail`
- Power Fx signals including `Location` and `Connection`: `https://learn.microsoft.com/en-us/power-platform/power-fx/reference/signals`
- Power Fx `Choices` function: `https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-choices`

## Findings

1. Canvas apps can connect directly to Dataverse tables. By default, a Dataverse connection targets the current environment, which aligns with solution-based ALM if the app and tables move together.
2. Dataverse security roles control table and row access. Showing the environment in Studio does not guarantee table/record access for the signed-in user.
3. `User().Email` returns the current Power Apps user's UPN, not necessarily SMTP email. For the MVP, filter assignments by both the Dataverse system-user lookup when present and the `UserEmail` fallback field.
4. Delegation matters. `Filter`, `LookUp`, `Sort`, `SortByColumns`, equality, comparisons, and boolean operators delegate to Dataverse for supported data types. Nondelegable formulas may only process the first 500 or 2,000 rows and can return incomplete results.
5. Avoid `Choices()` for runtime form choices because it is not delegable and is meant for lookup-column choices. TACATDP form choices are rows in the `Choices` table and should be queried directly.
6. Use `Patch` for the metadata-driven runtime because submissions and answers span multiple tables and cannot be modeled as one static edit form. Wrap writes with `IfError`/error handling and store the returned Dataverse record for child rows.
7. The Attachments control only supports upload/delete inside a form and its `Items` property must be the attachment column of a Dataverse table or list, not a transformed table. For the MVP, use an Edit form bound to `SubmissionFiles` for the file field, or defer rich attachment UX if a generic dynamic form cannot host it cleanly.
8. `Location` can provide GPS values but may prompt the user for permission and continuously recalculate while used. Capture location on demand and store a compact JSON object in `SubmissionAnswers.ValueJson`.
9. Edit form controls provide built-in validation and submit behavior for static records, but the metadata renderer needs dynamic controls, so forms should be used selectively for Dataverse file upload and not as the main question renderer.

## Architecture implication

Build one Canvas app as a runtime engine:

- `AssignedFormsScreen` filters `FormAssignments` for the current user and published active form version.
- `HistoryScreen` lists the user's own submissions for the selected form/version.
- `RunnerScreen` loads sections, questions, choices, validation rules, and existing answers into local state for responsive rendering.
- Save Draft / Submit writes to `Submissions`, `SubmissionAnswers`, and `SubmissionFiles` using `Patch`.
- File attachment uses a small static Dataverse form bound to `SubmissionFiles` because the Attachments control cannot operate outside a form.
- GPS capture uses `Location` only when the user selects capture.

## Constraints for first slice

- Keep queries delegable where the source table can grow: assignments, submissions, questions, choices, and answers.
- Avoid full expression parsing. Implement only required validation from seeded `ValidationRules` and optionally one simple relevance/constraint rule after the base loop works.
- Avoid repeat groups, barcode, offline-first sync, and admin publishing UI.
- Keep the Canvas app in the Dataverse solution once built.
