# Product Requirements Document: Dataverse-First TACATDP Backend

## Context and evidence

TACATDP converts a long XLSForm-style survey into a guided Power Apps Canvas app. Earlier planning used Microsoft Lists because Dataverse privileges were unavailable. The development environment now has Dataverse enabled, making a stronger relational backend available.

Evidence:

- `docs/multi-project-monitoring/`
- `docs/dataverse-first/research.md`
- `docs/list-schema-design.md`
- `schemas/xlsform-to-list-mapping.csv`
- `schemas/sharepoint-lists-schema.json`
- `docs/phase-3-validation-save-map/product-requirements-document.md`
- `docs/phase-3-requirements.md`
- `docs/phase-3-delivery-plan.md`

## Problem

The current Microsoft Lists plan works around missing Dataverse access by splitting a large form into multiple SharePoint lists and manually joining records with `SubmissionKey`. That approach is acceptable as a fallback but adds avoidable complexity for relationships, validation, large reference data, ALM, and save orchestration. TACATDP needs a robust development architecture now that Dataverse is available.

## Users / actors

- Enumerator: enters survey data in a guided app.
- Maker: builds tables, app screens, formulas, and solution components.
- Data manager: imports reference data and exports/analyses submissions.
- Reviewer/QA: validates completeness, constraints, and save behavior.
- Admin: manages environment, licensing, security roles, and solution deployment.

## Goals and success measures

| Goal | Success measure |
| --- | --- |
| Move to Dataverse-first architecture. | Planning artifacts identify multi-project Dataverse metadata, runtime, vocabulary, projection, relationship, key, and ALM paths. |
| Preserve XLSForm semantics. | Required, relevance, constraints, choices, multi-select, repeats, calculations, and versions remain mapped through generic metadata. |
| Improve relational integrity. | Projects, instruments, versions, entities, encounters, submissions, group instances, answer rows, and vocabulary terms use Dataverse relationships plus stable alternate keys. |
| Keep app implementation safe. | No production write/publish occurs before explicit approval and readiness checks. |
| Keep fallback path. | Microsoft Lists artifacts remain available but marked fallback. |

## Functional requirements

| ID | Requirement | Source / evidence | Priority |
| --- | --- | --- | --- |
| DV-RQ-01 | Use Dataverse as the primary development backend. | User decision, enabled Dataverse environment | P0 |
| DV-RQ-02 | Create a Power Platform solution to contain generic platform tables, relationships, vocabulary tables, app components, flows, projections, and environment variables. | Microsoft ALM guidance, multi-project PRD | P0 |
| DV-RQ-03 | Model TACATDP as the first `MonitoringProject`, not as the hard-coded platform schema. | `docs/multi-project-monitoring/` | P0 |
| DV-RQ-04 | Model instruments, versions, events, groups, fields, field rules, and vocabulary bindings as metadata/control-plane records. | ODK, CDISC ODM, REDCap patterns | P0 |
| DV-RQ-05 | Model submissions, group instances, scalar answers, multi-select answers, attachments, reviews, and audit events as normalized runtime records. | ODK submissions/repeats, CDISC item group data | P0 |
| DV-RQ-06 | Model long-lived entities/cases and encounters/follow-ups for longitudinal monitoring. | ODK Entities, OpenClinica events | P0 |
| DV-RQ-07 | Model controlled variables as reusable vocabulary schemes and terms, including large geography/reference vocabularies. | InvenioRDM vocabulary patterns, XLSForm choice inventory | P0 |
| DV-RQ-08 | Define alternate keys for integration/upsert values such as project code, instrument version, `SubmissionKey`, entity keys, field codes, and vocabulary term codes. | Microsoft alternate key guidance | P1 |
| DV-RQ-09 | Keep large reference filters delegable in Power Apps. | Microsoft delegation guidance | P0 |
| DV-RQ-10 | Update save-map and validation artifacts to refer to the generic Dataverse platform model first, with TACATDP-specific exports/projections generated from it. | Existing validation/save-map artifacts, multi-project model | P0 |

## UX requirements

No UX layout change is introduced by the backend pivot. Existing requirements remain:

- one field per row by default;
- visible labels above inputs;
- helper/error text below inputs;
- validation summary;
- draft/saved/submitted/save-failed states;
- wizard-style navigation;
- accessible focus order and touch targets.

## Architecture and data requirements

### Platform table groups

The multi-project monitoring model in `docs/multi-project-monitoring/data-model.md` supersedes a TACATDP-only table design. TACATDP-specific section tables such as `tacatdp_Profile`, `tacatdp_Agriculture`, or `tacatdp_ProductionIncome` should not be the core source-of-truth model. If needed later, they may be generated as projections, views, or performance/readability surfaces from the normalized platform model.

| Group | Platform concepts | Purpose |
| --- | --- | --- |
| Project and governance | `MonitoringProject`, role assignments, project settings | Multi-project boundary and access control. |
| Instrument metadata | `Instrument`, `InstrumentVersion`, `EventDefinition`, `InstrumentEventBinding` | Versioned forms and monitoring occasions. |
| Form structure metadata | `GroupDefinition`, `FieldDefinition`, `FieldRule` | Sections, repeatable groups, fields, relevance, constraints, calculations, order. |
| Controlled vocabularies | `VocabularyScheme`, `VocabularyTerm`, labels, relations, project bindings, field bindings, external IDs | Reusable controlled variables, choices, reference data, and large vocabularies. |
| Runtime entities | `TrackedEntity`, identifiers, `Encounter` | Longitudinal cases/sites/customers/farmers/facilities and follow-ups. |
| Runtime submissions | `Submission`, `GroupInstance`, `AnswerValue`, `MultiSelectAnswer`, `Attachment`, review, audit | Normalized collected data and repeat instances. |
| Export/projection layer | export profiles, generated views/tables, variable dictionary | Project-specific wide/long reporting outputs derived from normalized source data. |

### Key rules

- Dataverse GUID primary keys are internal; human/integration keys such as `ProjectCode`, `InstrumentCode`, `SubmissionKey`, `EntityKey`, `FieldCode`, and `TermCode` remain alternate keys where appropriate.
- Use relationships for project, instrument, version, group, field, entity, encounter, submission, group instance, answer, and vocabulary integrity.
- Use generic normalized runtime tables as source of truth; use TACATDP-specific tables only as projections if later justified.
- Use vocabulary terms for controlled variables and large/filtered choices; avoid huge static choice columns.
- Store selected term references plus code/label snapshots where export fidelity matters.
- Preserve current field inventory and XLSForm names in metadata-generation artifacts.

## Safety, privacy, and operational constraints

- Do not commit environment IDs, connection strings, tokens, secrets, or tenant-specific credentials.
- Do not create or modify production Dataverse tables without explicit approval.
- Use trial/dev environment first.
- Package future Dataverse work in a solution.
- Document any production licensing/tenant dependency before committing to deployment.

## Acceptance criteria

See `acceptance-criteria.md`.

## Definition of ready

See `artifact-readiness.md`.

## Definition of done

See `definition-of-done.md`.

## Traceability

See `requirements-traceability.md`.
