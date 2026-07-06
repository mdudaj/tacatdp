# Requirements Note: July 7 Metadata-Driven MVP

The active MVP is a dynamic Dataverse-backed data collection vertical slice:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

This replaces the previous near-term emphasis on TACATDP fixed screens, repeat pilots, and broad multi-project schema implementation. Those remain useful later, but the July 7 delivery must prove the runtime path first.

Key scope decisions:

- Use Power Apps / Entra authentication.
- Use `FormAssignments` for assigned forms.
- Use metadata tables for forms, versions, sections, questions, choices, and simple validation rules.
- Use generic submission, answer, and file tables.
- Store select-many and GPS in `ValueJson` for MVP if needed.
- Defer full XLSForm compiler, repeat groups, offline sync, barcode, dashboards, and admin publishing UI.
