# PRD: Multi-Project Monitoring Platform Data Model

## Context and evidence

TACATDP started as one Power Apps survey conversion. During Dataverse planning, we identified that hard-coding TACATDP sections as the platform data model would make future monitoring projects difficult. Research into ODK Central, OpenClinica/CDISC ODM, REDCap, and InvenioRDM shows that robust platforms separate project metadata, instrument definitions, runtime submission data, repeat instances, entities/encounters, and controlled vocabularies.

Evidence:

- `docs/multi-project-monitoring/research.md`
- `docs/dataverse-first/`
- `schemas/xlsform-to-list-mapping.csv`
- `docs/list-schema-design.md`
- ODK Central docs for projects, forms, submissions, entities, and repeats
- OpenClinica/CDISC ODM hierarchy: study, event, form, item group, item
- InvenioRDM controlled vocabulary patterns

## Problem

A TACATDP-specific Dataverse schema can deliver one project but will not scale cleanly to multiple monitoring projects with different instruments, repeats, longitudinal follow-ups, and controlled vocabularies. We need a reusable platform model that can host TACATDP as the first configured project.

## Goals

| Goal | Success measure |
| --- | --- |
| Support multiple monitoring projects. | Project is first-class and all definitions/data are project-scoped. |
| Support arbitrary forms and versions. | Instruments and versions can evolve without rewriting core tables. |
| Support repeating groups. | Runtime data stores repeat group instances with occurrence identity. |
| Support multi-select. | Multi-select choices are stored as normalized rows. |
| Support longitudinal monitoring. | Entities/cases and encounters link repeated visits/submissions. |
| Support controlled variables/vocabularies. | Reusable terms can be bound to fields and filtered per project. |
| Preserve analytics. | Project-specific exports/projections can be generated from normalized runtime data. |

## Users / actors

- Platform admin: creates projects, vocabularies, and permissions.
- Project manager: configures monitoring project instruments and versions.
- Data collector/enumerator: submits project data.
- Reviewer/QA: reviews submissions and data quality.
- Data manager: manages vocabularies, imports reference data, exports datasets.
- Analyst: consumes normalized or projected reporting data.

## Proposed conceptual model

### Control plane metadata

| Concept | Purpose |
| --- | --- |
| `MonitoringProject` | Top-level project/program boundary. |
| `ProjectRoleAssignment` | Project-specific user/role mapping. |
| `Instrument` | Form/survey definition container. |
| `InstrumentVersion` | Versioned form definition, draft/published/retired. |
| `EventDefinition` | Optional monitoring occasion, visit, reporting period, or follow-up event. |
| `InstrumentEventBinding` | Which instrument/version is used for which event. |
| `GroupDefinition` | Section/item group; can be repeatable. |
| `FieldDefinition` | Variable/question metadata. |
| `FieldRule` | Required, relevance, constraint, calculation, validation messages. |
| `VocabularyScheme` | Controlled vocabulary namespace/scheme. |
| `VocabularyTerm` | Controlled term/code with labels and metadata. |
| `ProjectVocabularyBinding` | Project-specific vocabulary subset. |
| `FieldVocabularyBinding` | Field-to-vocabulary binding and allowed terms. |

### Runtime data

| Concept | Purpose |
| --- | --- |
| `TrackedEntity` | Long-lived subject/case/site/customer/farmer/facility. |
| `EntityIdentifier` | Project-specific and external identifiers for entities. |
| `Encounter` | Monitoring visit/event/follow-up occurrence for an entity. |
| `Submission` | One filled instrument instance. |
| `SubmissionReview` | Review status, comments, approvals/rejections. |
| `GroupInstance` | One occurrence of a section/group/repeating group. |
| `AnswerValue` | Scalar answer linked to field and group instance. |
| `MultiSelectAnswer` | One selected term per multi-select field. |
| `Attachment` | Files/photos/media/geospatial attachments. |
| `AuditEvent` | Change, review, import, sync, or correction history. |

### Export/projection layer

| Concept | Purpose |
| --- | --- |
| `ProjectExportProfile` | Defines wide/long export shapes per project. |
| `ProjectionTable/View` | Optional generated reporting shape. |
| `VariableDictionaryExport` | Human-readable codebook/data dictionary. |

## Key architecture decisions

1. The normalized runtime model is the source of truth.
2. TACATDP-specific section tables should become projections or generated performance optimizations, not the core model.
3. Repeating groups are represented as `GroupInstance` rows with repeat indexes and optional parent group instance.
4. Multi-select values are represented as `MultiSelectAnswer` rows that reference vocabulary terms.
5. Controlled variables are represented through vocabulary schemes and terms, inspired by InvenioRDM-style vocabularies.
6. Form versions must be immutable once published; new changes create a new `InstrumentVersion`.
7. Submitted data must point to the exact `InstrumentVersion`, `GroupDefinition`, and `FieldDefinition` active at collection time.

## Safety and constraints

- Do not create Dataverse tables until schema artifacts are reviewed.
- Do not store secrets, environment IDs, or tenant-specific credentials in source.
- Keep project-level access and data separation explicit.
- Preserve TACATDP current deliverables while planning the more generic platform model.

## Acceptance criteria

See `acceptance-criteria.md`.

