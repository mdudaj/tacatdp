# PRD: Project Platform Vision and TACATDP Prototype

## Context and evidence

TACATDP started as one Power Apps survey conversion. During Dataverse planning, we identified that hard-coding TACATDP sections as the platform data model would make future projects difficult. Research into ODK Central, OpenClinica/CDISC ODM, REDCap, and InvenioRDM shows that robust form/data platforms separate project metadata, instrument definitions, runtime submission data, repeat instances, entities/encounters, and controlled vocabularies.

Evidence:

- `docs/multi-project-monitoring/research.md`
- `docs/dataverse-first/`
- `schemas/xlsform-to-list-mapping.csv`
- `docs/list-schema-design.md`
- ODK Central docs for projects, forms, submissions, entities, and repeats
- OpenClinica/CDISC ODM hierarchy: study, event, form, item group, item
- InvenioRDM v13 controlled vocabulary patterns:
  - `https://inveniordm.docs.cern.ch/`
  - `https://inveniordm.docs.cern.ch/features/customization/`
  - `https://inveniordm.docs.cern.ch/reference/rest_api_vocabularies/`

## Problem

A TACATDP-specific Dataverse schema can deliver one project but will not scale cleanly to multiple projects with different instruments, repeats, longitudinal follow-ups, and controlled vocabularies. The reusable platform is the long-term vision, but implementing the full multi-project platform now is a large research and engineering effort. TACATDP should be delivered first as a single-project prototype that validates the core patterns.

## Goals

| Goal | Success measure |
| --- | --- |
| Preserve project-platform vision. | Project is first-class and all definitions/data can become project-scoped. |
| Deliver TACATDP prototype first. | One TACATDP end-to-end flow can be built without waiting for full multi-project generalization. |
| Support arbitrary forms and versions. | Instruments and versions can evolve without rewriting core tables. |
| Support repeating groups. | Runtime data stores repeat group instances with occurrence identity. |
| Support multi-select. | Multi-select choices are stored as normalized rows. |
| Support longitudinal monitoring. | Entities/cases and encounters link repeated visits/submissions. |
| Support controlled variables/vocabularies. | Reusable terms can be bound to fields and filtered per project. |
| Preserve analytics. | Project-specific exports/projections can be generated from normalized runtime data. |
| Support metadata-driven form UX. | A reusable form runner can load and render different projects/instruments from metadata instead of requiring hand-built screens per project. |

## Users / actors

- Platform admin: creates projects, vocabularies, and permissions.
- Project manager: configures project instruments and versions.
- Data collector/enumerator: submits project data.
- Reviewer/QA: reviews submissions and data quality.
- Data manager: manages vocabularies, imports reference data, exports datasets.
- Analyst: consumes normalized or projected reporting data.

## Proposed conceptual model

### Control plane metadata

| Concept | Purpose |
| --- | --- |
| `Project` | Top-level project/program boundary. |
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

## Controlled vocabulary requirements

The controlled variables feature should follow the confirmed InvenioRDM v13 vocabulary pattern, adapted for monitoring data:

| Requirement | PRD expectation |
| --- | --- |
| Stable identifiers | Each term must have a stable code/ID independent of display label changes. |
| Vocabulary type/scheme | Terms must belong to a scheme/type, such as geography, crop, branch, unit, cost item, intervention, or project-specific code list. |
| Localized labels | Terms must support localized titles/labels and descriptions, including English and Swahili where needed. |
| Flexible metadata | Terms must support extensible properties for source XLSForm value, sort order, parent filters, authority metadata, or project metadata. |
| Tags/filtering | Terms must support tags or equivalent classifications so UI controls and APIs can filter them. |
| Links/external IDs | Terms should support external authority identifiers and links where applicable. |
| Search/autocomplete | The platform should eventually expose search/suggest behavior for large vocabularies, mirroring InvenioRDM's vocabulary API pattern. |
| Specific vocabularies | Large or special vocabularies, such as villages, organizations, funders, facilities, or subjects, may need dedicated views/endpoints rather than generic dropdown loading. |
| Project binding | Projects must be able to use a subset of global terms without duplicating the global vocabulary. |
| Field binding | Field definitions must bind to a scheme and specify single-select, multi-select, or reference lookup behavior. |

## Key architecture decisions

1. The normalized runtime model is the source of truth.
2. TACATDP-specific section tables should become projections or generated performance optimizations, not the core model.
3. Repeating groups are represented as `GroupInstance` rows with repeat indexes and optional parent group instance.
4. Multi-select values are represented as `MultiSelectAnswer` rows that reference vocabulary terms.
5. Controlled variables are represented through vocabulary schemes and terms, using the InvenioRDM-style pattern of stable IDs, vocabulary types, localized labels/descriptions, flexible properties, tags, links, and search/suggest support.
6. Form versions must be immutable once published; new changes create a new `InstrumentVersion`.
7. Submitted data must point to the exact `InstrumentVersion`, `GroupDefinition`, and `FieldDefinition` active at collection time.
8. The long-term Canvas UX should be a metadata-driven form runner. The current 33 TACATDP screens are a transitional scaffold or generated projection, not the reusable multi-project application architecture.
9. The near-term implementation should be a TACATDP single-project prototype. Multi-project and generic renderer implementation remain the app vision and research track, not a prerequisite for the first working prototype.

## Safety and constraints

- Do not create Dataverse tables until schema artifacts are reviewed.
- Do not store secrets, environment IDs, or tenant-specific credentials in source.
- Keep project-level access and data separation explicit.
- Preserve TACATDP current deliverables while planning the more generic platform model.
- Do not continue hand-building one screen per TACATDP section as the platform default before the form-renderer contract is reviewed.
- Do not let the full multi-project vision block a TACATDP prototype; document prototype shortcuts and revisit them before platform generalization.

## Acceptance criteria

See `acceptance-criteria.md`.
