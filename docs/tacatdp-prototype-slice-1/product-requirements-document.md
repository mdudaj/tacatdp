# PRD: TACATDP Prototype Slice 1

## Problem

The app vision now separates the long-term reusable Project platform from the near-term TACATDP prototype. We need a small implementation slice that proves TACATDP can collect, validate, save, and review real project data without blocking on full multi-project generalization.

## Goals

| Goal | Success measure |
| --- | --- |
| Prove a one-project prototype path. | TACATDP can run one bounded flow without requiring a full generic renderer. |
| Validate core input UX. | Fields use one row per field, visible labels, helper text, inline errors, and review summary. |
| Validate cascading reference lookup. | Region, district, ward, and village selection filters correctly, with village modeled as high-volume reference data. |
| Validate multi-select storage shape. | One multi-select question saves selections as child rows or placeholder rows shaped for `mp_MultiSelectAnswer`. |
| Validate repeat/line-item storage shape. | One production-cost item saves as a repeat/line item shaped for `GroupInstance` plus answer rows or the prototype equivalent. |
| Preserve platform seams. | Prototype choices are traceable to Project, InstrumentVersion, GroupDefinition, FieldDefinition, Submission, and answer concepts. |

## Users

- Enumerator/data collector: fills and saves the prototype flow.
- Reviewer/QA: reviews the saved prototype summary and validation state.
- Builder/developer: implements the prototype while preserving future platform seams.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| P1-RQ-01 | The prototype starts a TACATDP submission with a project/instrument/version identity, even if hard-coded for the prototype. | P0 |
| P1-RQ-02 | Demographics fields render in one-field-per-row layout with visible labels and helper/error text. | P0 |
| P1-RQ-03 | Required-visible demographics fields block Continue/Save until valid. | P0 |
| P1-RQ-04 | Phone and loan amount constraints from the source field inventory are enforced with visible messages. | P0 |
| P1-RQ-05 | Region, district, ward, and village cascade filters use delegation-safe lookup shapes; village uses the dedicated village reference source. | P0 |
| P1-RQ-06 | One agricultural multi-select field saves one row per selected choice in a child collection/table shape. | P0 |
| P1-RQ-07 | One production-cost repeat line supports add/edit/remove for stage, item, unit, quantity, and cost. | P0 |
| P1-RQ-08 | Save Draft persists the in-scope submission, multi-select, and repeat data to approved prototype storage. | P0 |
| P1-RQ-09 | Save failures show visible failed state and must not navigate as if successful. | P0 |
| P1-RQ-10 | Review summary shows demographics completion, selected multi-select values, repeat-line totals, and validation blockers. | P1 |
| P1-RQ-11 | Implementation notes classify shortcuts as acceptable prototype debt, needs refactor, or blocks platform generalization. | P1 |

## Non-functional requirements

- No secrets, tenant IDs, environment IDs, or credentials in source.
- No Dataverse, Power Platform, SharePoint, or production writes without explicit approval.
- Keep formulas and data shapes readable and reviewable.
- Preserve accessibility: visible labels, text errors, logical focus order, and minimum touch targets.

## Prototype data-storage expectation

This slice may use local collections or reviewed dev Dataverse tables after approval. If local collections are used, they should be shaped to migrate toward:

- `Project`
- `InstrumentVersion`
- `Submission`
- `GroupInstance`
- `AnswerValue`
- `MultiSelectAnswer`
- `mp_VillageReference`

## Open decisions before implementation

1. Whether Slice 1 uses local placeholder collections only or approved dev Dataverse tables.
2. Whether the first multi-select field is `crop_name`, `technology`, or another agricultural production field.
3. Whether production-cost repeat starts from existing `Screen_33_production_cost_detail` or a simplified prototype repeat component.
