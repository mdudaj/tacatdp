# Dataverse-First Requirements Note

## Bounded outcome

Revise TACATDP planning artifacts so the next development slice targets Dataverse as the primary backend instead of Microsoft Lists/SharePoint.

This is an architecture and requirements pivot only. It does not create Dataverse tables, import data, publish apps, or connect to production environments.

## Drivers

- The development tenant now has Dataverse enabled.
- TACATDP's data model has relationships, child rows, large reference tables, validation rules, and ALM needs that are stronger fits for Dataverse than Microsoft Lists.
- Microsoft Lists work remains useful as a fallback and as a source decomposition, but it should not drive the primary implementation if Dataverse is available.

## Requirements

| ID | Requirement | Priority | Evidence |
| --- | --- | --- | --- |
| DV-RQ-01 | TACATDP must use Dataverse as the primary development backend. | P0 | User decision and enabled Dataverse environment |
| DV-RQ-02 | The model must preserve project, instrument, version, group, field, submission, repeat, answer, entity, encounter, and vocabulary boundaries. | P0 | Multi-project monitoring model |
| DV-RQ-03 | Every submission must keep a stable `SubmissionKey` alternate/integration key while relating to project, instrument version, entity, and encounter records. | P0 | Existing save-map artifacts and ODK-style workflow |
| DV-RQ-04 | TACATDP section data must be represented through generic group definitions, group instances, field definitions, and answer rows; TACATDP-specific section tables are projections only if needed. | P0 | Multi-project monitoring model |
| DV-RQ-05 | `select_multiple` answers must remain normalized as child rows linked to field definitions and vocabulary terms. | P0 | `TACATDP_MultiSelectAnswers` mapping |
| DV-RQ-06 | Production cost stage details must be modeled as repeat/group instances and answer rows or line-item projections, not fixed TACATDP-only core tables. | P0 | `TACATDP_ProductionCostLines` mapping |
| DV-RQ-07 | Large reference choices must be vocabulary/reference tables with delegable filters, not huge static choices. | P0 | 66,297 villages and delegation guidance |
| DV-RQ-08 | Power Platform solution packaging must be planned before implementation. | P1 | Power Platform ALM guidance |
| DV-RQ-09 | Microsoft Lists scripts and docs must be marked fallback until production confirms platform choice. | P1 | Existing Lists work remains reviewable |
| DV-RQ-10 | No production Dataverse write, app publish, or environment permission change may occur without explicit approval. | P0 | TACATDP safety gates |

## Non-goals

- Generating Dataverse tables in this slice.
- Importing data into Dataverse in this slice.
- Migrating any CRDB production data.
- Publishing or importing a production Power App.
- Deleting Microsoft Lists artifacts.

## Open questions

- What publisher prefix should be used for the TACATDP Dataverse solution?
- Should the dev environment use the trial tenant only or also prepare a separate test environment?
- Which users/security roles are needed for maker, enumerator, reviewer, and data manager roles?
- Which fields need Dataverse business rules versus app-only Power Fx validation?
- Should choices use Dataverse choice columns for small lists or reference tables consistently for export fidelity?

## Design stance

Use a metadata-driven, multi-project core model, not one fixed Dataverse table per TACATDP section as the long-term source of truth. Project-specific typed/wide tables may still be generated later for analytics, exports, performance, or maker ergonomics, but they are projections derived from the normalized model.
