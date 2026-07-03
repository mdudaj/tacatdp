# Delivery Plan: Multi-Project Monitoring Model

## Phase 1: Approve conceptual model

Review:

- `research.md`
- `product-requirements-document.md`
- `data-model.md`
- `controlled-vocabularies.md`

Decision needed:

- confirm metadata-driven platform model;
- confirm TACATDP as first project configuration;
- confirm generic normalized runtime data as source of truth.

## Phase 2: Generate Dataverse schema artifacts

Create reviewable artifacts only:

- `schemas/dataverse/platform-tables.json`
- `schemas/dataverse/platform-columns.csv`
- `schemas/dataverse/platform-relationships.csv`
- `schemas/dataverse/platform-alternate-keys.csv`
- `schemas/dataverse/tacatdp-field-definitions.csv`
- `schemas/dataverse/tacatdp-vocabulary-terms.csv`
- `schemas/dataverse/import-order.md`

No environment writes in this phase.

## Phase 3: TACATDP metadata migration

Transform existing TACATDP artifacts:

- XLSForm field inventory -> `FieldDefinition`
- screen/section map -> `GroupDefinition`
- choice lists -> `VocabularyScheme` and `VocabularyTerm`
- mapping rows -> field/group/source traceability
- production cost lines -> repeatable group or line-item configuration

## Phase 4: Form renderer UX contract

Create reviewable artifacts only:

- `docs/multi-project-monitoring/form-renderer-ux.md`
- `schemas/dataverse/form-renderer-contract.json`
- group/page layout metadata for `GroupDefinition`
- field appearance/control metadata for `FieldDefinition`
- first supported rule-expression subset for required, relevance, constraint, choice filter, and calculation behavior
- pilot flow for one normal TACATDP group and one repeat group

The fixed 33-screen TACATDP source should pause as a platform-default implementation path until this contract is reviewed.

## Phase 5: Dev Dataverse implementation

After explicit approval:

1. Create the core platform solution.
2. Create metadata/control-plane tables.
3. Create runtime data tables.
4. Create controlled vocabulary tables.
5. Import TACATDP metadata and vocabulary terms.
6. Validate relationships and alternate keys.

## Phase 6: App integration

1. Build a generic form runner shell rather than hand-building all TACATDP screens.
2. Bind the runner to metadata/runtime tables or reviewed local placeholder collections shaped like those tables.
3. Implement save/read for one pilot group and one repeat group.
4. Validate repeats, multi-select, relevance, constraints, and large reference filtering.
5. Keep current fixed screens only as transitional/projection artifacts.

## Phase 7: Export/projection support

1. Generate TACATDP codebook.
2. Generate wide export profiles.
3. Generate Power BI-friendly views/dataflows.
4. Preserve normalized source-of-truth data.
