# Delivery Plan: Project Platform Vision and TACATDP Prototype

## Phase 1: Preserve app vision

Review:

- `../app-vision.md`
- `research.md`
- `product-requirements-document.md`
- `data-model.md`
- `controlled-vocabularies.md`

Decision needed:

- confirm Project as the general top-level concept;
- confirm metadata-driven platform model as long-term vision;
- confirm TACATDP as the first single-project prototype;
- confirm generic normalized runtime data as a guardrail, not a blocker.

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

## Phase 5: TACATDP prototype implementation

After explicit approval, implement one TACATDP project prototype before attempting broad multi-project generalization:

1. Use `docs/tacatdp-prototype-slice-1/` as the first implementation scope.
2. Create or prepare only the Dataverse pieces needed for one TACATDP prototype slice.
3. Implement one normal section end-to-end.
4. Implement the region/district/ward/village cascade using delegated reference data.
5. Implement one multi-select pattern.
6. Implement one repeat/line-item pattern.
7. Validate save, edit, review, and export/codebook implications.
8. Record prototype shortcuts and classify each as acceptable, needs refactor, or blocks platform generalization.

## Phase 6: App integration

1. Use the renderer contract as a guide, but do not require a full generic renderer before the prototype.
2. Prefer prototype code that can later migrate into the form runner.
3. Bind the prototype to metadata/runtime tables or reviewed local placeholder collections shaped like those tables.
4. Validate repeats, multi-select, relevance, constraints, and large reference filtering.
5. Keep fixed screens as TACATDP prototype/projection artifacts.

## Phase 7: Multi-project research continuation

1. Research how ODK Collect, Enketo, REDCap, OpenClinica, and related tools handle form loading, offline behavior, expression evaluation, repeat UX, and web/mobile parity.
2. Decide whether the long-term renderer is Power Apps-only, shared metadata with Power Apps and custom web renderers, or a custom renderer outside Power Apps.
3. Refine the renderer contract after TACATDP prototype lessons.

## Phase 8: Export/projection support

1. Generate TACATDP codebook.
2. Generate wide export profiles.
3. Generate Power BI-friendly views/dataflows.
4. Preserve normalized source-of-truth data.
