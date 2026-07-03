# Requirements Traceability: TACATDP Prototype Slice 1

| Requirement | Story | Acceptance criteria | Source artifact | Implementation surface |
| --- | --- | --- | --- | --- |
| P1-RQ-01 Submission context | P1-US-01 | AC-01 | `docs/app-vision.md`, `schemas/dataverse/form-renderer-contract.json` | App startup/prototype context |
| P1-RQ-02 Demographics layout | P1-US-02 | AC-02 | `docs/design-system.md`, `docs/phase-3-maker-runbook.md` | Demographics screen/field rows |
| P1-RQ-03 Required-visible validation | P1-US-02 | AC-03 | `docs/xlsform-field-inventory.csv`, `docs/xlsform-logic-map.csv` | Validation formulas/state |
| P1-RQ-04 Constraint validation | P1-US-02 | AC-04 | `docs/xlsform-field-inventory.csv` rows for phone and loan amount | Validation formulas/state |
| P1-RQ-05 Cascading geography | P1-US-02 | AC-05 | `schemas/dataverse/tacatdp-village-reference.csv`, `schemas/reference-data/*` | Region/district/ward/village controls |
| P1-RQ-06 Multi-select storage | P1-US-03 | AC-06 | `schemas/dataverse/tacatdp-field-definitions.csv` | Multi-select child collection/table |
| P1-RQ-07 Repeat line item | P1-US-04 | AC-07 | `Screen_33_production_cost_detail`, `schemas/xlsform-to-list-mapping.csv` | Production-cost line UI/storage |
| P1-RQ-08 Save draft | P1-US-05 | AC-08, AC-09 | `docs/phase-3-validation-save-map/product-requirements-document.md` | Save draft formulas/storage |
| P1-RQ-09 Save failure | P1-US-05 | AC-08 | `docs/design-system.md` | Save error state |
| P1-RQ-10 Review summary | P1-US-05 | AC-09 | `docs/phase-3-validation-save-map/product-requirements-document.md` | Review summary screen |
| P1-RQ-11 Prototype shortcut classification | P1-US-05 | AC-10 | `docs/app-vision.md` | Prototype debt register |
