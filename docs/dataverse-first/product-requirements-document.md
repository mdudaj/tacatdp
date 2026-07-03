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
| Move to Dataverse-first architecture. | Planning artifacts identify Dataverse tables, relationships, keys, and ALM path. |
| Preserve XLSForm semantics. | Required, relevance, constraints, choices, multi-select, repeats, and calculations remain mapped. |
| Improve relational integrity. | Parent, section, child, and reference tables use Dataverse relationships plus stable alternate keys. |
| Keep app implementation safe. | No production write/publish occurs before explicit approval and readiness checks. |
| Keep fallback path. | Microsoft Lists artifacts remain available but marked fallback. |

## Functional requirements

| ID | Requirement | Source / evidence | Priority |
| --- | --- | --- | --- |
| DV-RQ-01 | Use Dataverse as the primary development backend. | User decision, enabled Dataverse environment | P0 |
| DV-RQ-02 | Create a TACATDP Power Platform solution to contain tables, relationships, choices, app components, flows, and environment variables. | Microsoft ALM guidance | P0 |
| DV-RQ-03 | Model one Submission parent table with `SubmissionKey`, status, timestamps, enumerator metadata, and review fields. | Existing `TACATDP_Submissions` design | P0 |
| DV-RQ-04 | Model section tables related to Submission. | Existing section list design | P0 |
| DV-RQ-05 | Model `MultiSelectAnswer` child rows. | Existing multi-select mapping | P0 |
| DV-RQ-06 | Model `ProductionCostLine` child rows. | Existing production cost mapping | P0 |
| DV-RQ-07 | Model Regions, Districts, Wards, Villages, Branches, and generic reference choices as reference tables. | XLSForm choice inventory | P0 |
| DV-RQ-08 | Define alternate keys for integration/upsert values such as `SubmissionKey`, reference codes, and composite question-choice identifiers. | Microsoft alternate key guidance | P1 |
| DV-RQ-09 | Keep large reference filters delegable in Power Apps. | Microsoft delegation guidance | P0 |
| DV-RQ-10 | Update save-map and validation artifacts to refer to Dataverse tables first. | Existing validation/save-map artifacts | P0 |

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

### Proposed table groups

The multi-project monitoring model in `docs/multi-project-monitoring/data-model.md` supersedes a TACATDP-only table design. TACATDP should be implemented as the first configured `MonitoringProject` with instrument/group/field metadata, controlled vocabularies, submissions, group instances, answer values, and export projections.

| Group | Proposed Dataverse table(s) | Notes |
| --- | --- | --- |
| Parent | `tacatdp_Submission` | One row per survey; alternate key `SubmissionKey`. |
| Profile | `tacatdp_Profile` | 1:1 or 1:N related section row for demographics/location/loan/geopoint. |
| Section scalar data | `tacatdp_Agriculture`, `tacatdp_ResourceEfficiency`, `tacatdp_SocialInclusion`, `tacatdp_SafeguardsClimate`, `tacatdp_InsuranceGuarantee`, `tacatdp_GHGWaterYield`, `tacatdp_ProductionIncome` | Section tables related to Submission. |
| Beneficiaries | `tacatdp_BeneficiaryStage` or section-specific beneficiary tables | Prefer one normalized stage table if it keeps formulas/reporting simpler. |
| Multi-select | `tacatdp_MultiSelectAnswer` | One row per selected choice. |
| Production cost | `tacatdp_ProductionCostLine` | One row per stage/item/unit/quantity/cost line. |
| Reference geography | `tacatdp_Region`, `tacatdp_District`, `tacatdp_Ward`, `tacatdp_Village` | Parent-child relationships and alternate keys. |
| Other reference | `tacatdp_Branch`, `tacatdp_ReferenceChoice` | Choice list name/value/label/filter keys. |

### Key rules

- Dataverse GUID primary keys are internal. `SubmissionKey` remains the app/integration key.
- Use relationships for parent/child integrity; do not rely only on text keys.
- Use alternate keys for import/upsert and integration.
- Use reference tables for large and filtered choices; avoid huge static choice columns.
- Store both value and label where export fidelity matters.
- Preserve current field inventory and XLSForm names in schema-generation artifacts.

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
