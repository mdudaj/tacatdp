# PRD: Dataverse Schema CLI Delivery for TACATDP MVP

## Goal

Create a reviewed, repeatable delivery path for setting up the July 7 MVP Dataverse schema in the dev environment.

## MVP schema

Use only:

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

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| DVCLI-RQ-01 | Validate PAC authentication and target environment before any schema work. | P0 |
| DVCLI-RQ-02 | Validate `.env` without printing secrets. | P0 |
| DVCLI-RQ-03 | Validate `mvp-tables.json` contains exactly the MVP table set. | P0 |
| DVCLI-RQ-04 | Validate the full MVP schema definition, including table purposes, columns, required flags, choices, lookup targets, relationships, assignment fields, submission status, generic answers, and files. | P0 |
| DVCLI-RQ-05 | Generate a dry-run operation plan for table and column creation. | P0 |
| DVCLI-RQ-06 | Use PAC for auth and solution lifecycle. | P0 |
| DVCLI-RQ-07 | Use Dataverse Web API metadata operations for table/column/relationship creation after approval. | P0 |
| DVCLI-RQ-08 | Include `MSCRM.SolutionUniqueName` in approved metadata create operations. | P0 |
| DVCLI-RQ-09 | Keep seed data small and limited to one published form, representative questions, choices, rules, and one assignment. | P0 |
| DVCLI-RQ-10 | Refuse production target or destructive metadata operations by default. | P0 |

## Non-goals

- Full XLSForm compiler.
- Full platform schema.
- Repeat groups or nested repeats.
- Admin publishing UI.
- Production deployment.
- Deleting or mutating existing production metadata.

## Risks

- Dataverse metadata APIs are powerful and can create hard-to-clean schema drift if run against the wrong environment.
- Table/relationship update semantics are riskier than create-only setup.
- PAC data import is not suitable for large volumes, so large reference loads need a later path.

## Safety constraints

- Dev target only.
- Dry-run output must be reviewed before writes.
- Secrets must stay in `.env` or secret manager only.
- No delete/reset/publish/import to production.
