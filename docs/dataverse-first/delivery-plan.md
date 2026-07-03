# Dataverse-First Delivery Plan

## Phase 0: Confirm dev environment

1. Confirm the trial/dev environment has Dataverse enabled.
2. Choose or create a Power Platform solution for TACATDP.
3. Choose publisher prefix, for example `tacatdp`.
4. Record environment-specific values outside source control.

## Phase 1: Dataverse schema design

Inputs:

- `schemas/xlsform-to-list-mapping.csv`
- `schemas/sharepoint-lists-schema.json`
- `docs/xlsform-field-inventory.csv`
- `docs/xlsform-choice-lists.csv`
- `docs/dataverse-first/product-requirements-document.md`

Outputs:

- Dataverse table inventory.
- Column inventory with Dataverse data types.
- Relationship inventory.
- Alternate-key inventory.
- Choice/reference-table decision matrix.
- Import-order plan.

## Phase 2: Dataverse schema generation artifacts

Create reviewable generated artifacts before environment writes:

- `schemas/dataverse/tables.json`
- `schemas/dataverse/columns.csv`
- `schemas/dataverse/relationships.csv`
- `schemas/dataverse/alternate-keys.csv`
- `schemas/dataverse/import-order.md`
- optional Power Platform CLI or PAC script plan.

## Phase 3: Dev environment creation

After explicit approval:

1. Create tables in the dev solution.
2. Create relationships and alternate keys.
3. Import small reference tables first.
4. Import large reference tables such as villages with batching/dataflows.
5. Validate lookups and delegation.

## Phase 4: Canvas app connection pivot

1. Keep current screen source and UX layout.
2. Replace placeholder/Microsoft Lists data source assumptions with Dataverse table names.
3. Update save formulas section by section.
4. Validate one screen before replicating.
5. Use App Checker and Monitor.

## Phase 5: Review and deployment readiness

1. Export unmanaged solution from dev.
2. Review solution components.
3. Define test/prod deployment path.
4. Use managed solution for non-dev environments when ready.
5. Document licensing/admin dependencies.

## Immediate next slice

Generate the Dataverse schema design artifacts from the existing XLSForm/list-mapping files without writing to any environment.

