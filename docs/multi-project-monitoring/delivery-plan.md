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

## Phase 4: Dev Dataverse implementation

After explicit approval:

1. Create the core platform solution.
2. Create metadata/control-plane tables.
3. Create runtime data tables.
4. Create controlled vocabulary tables.
5. Import TACATDP metadata and vocabulary terms.
6. Validate relationships and alternate keys.

## Phase 5: App integration

1. Keep current Canvas screens while source layout is revised.
2. Bind screens to metadata/runtime tables or generated TACATDP projections.
3. Implement save/read for one pilot section.
4. Validate repeats and multi-select.
5. Validate large reference filtering.

## Phase 6: Export/projection support

1. Generate TACATDP codebook.
2. Generate wide export profiles.
3. Generate Power BI-friendly views/dataflows.
4. Preserve normalized source-of-truth data.

