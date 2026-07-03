# Delivery Plan: TACATDP Prototype Slice 1

## Step 1: Confirm implementation storage

Default to local placeholder collections shaped like future Dataverse tables unless explicit approval is given for dev Dataverse table creation/import.

## Step 2: Implement submission context

Create TACATDP prototype context:

- project code: `tacatdp`
- instrument code: `impact_evaluation`
- version code: `phase3_source_v1`
- submission key
- save status

## Step 3: Implement demographics flow

Use `Screen_01_demographics` or a focused prototype equivalent:

- one field per row;
- visible labels;
- helper/error text;
- required-visible validation;
- phone and loan amount constraints;
- location cascade.

## Step 4: Implement delegated geography cascade

Use source-shaped reference data:

- regions;
- districts filtered by region;
- wards filtered by region and district;
- villages filtered by region, district, and ward using dedicated village reference shape.

## Step 5: Implement one multi-select pattern

Recommended first field: `crop_name`, unless implementation review selects another agricultural field.

Persist one row per selected value in a child shape aligned with `mp_MultiSelectAnswer`.

## Step 6: Implement one repeat/line-item pattern

Use production cost detail as the repeat pilot:

- stage;
- cost item;
- unit;
- quantity;
- cost;
- add/edit/remove;
- line total and summary.

## Step 7: Implement save draft and review summary

Save in-scope parent and child data to approved prototype storage. Review summary must show saved values, blockers, and totals.

## Step 8: Record prototype debt

Add an implementation note classifying shortcuts as:

- acceptable prototype debt;
- needs refactor;
- blocks platform generalization.
