# Acceptance Criteria: TACATDP Prototype Slice 1

## AC-01 Submission context

Given the prototype starts, when the user begins Slice 1, then the app has TACATDP project, instrument, version, and submission key context available.

## AC-02 Demographics layout

Given the user views demographics, when fields render, then each input has a visible label above the control, helper/error text below the control, consistent spacing, and one-field-per-row layout.

## AC-03 Required-visible validation

Given a required visible field is blank, when the user continues or saves, then navigation/save is blocked and an inline text error plus validation summary entry is shown.

## AC-04 Constraint validation

Given the phone or loan amount field has an invalid value, when the user continues or saves, then the source constraint message is shown and the app does not save as successful.

## AC-05 Cascading geography

Given the user selects a region, district, and ward, when village choices load, then only villages matching those selected codes are available through the dedicated village reference source.

## AC-06 Multi-select child rows

Given the user selects multiple values for the chosen agricultural multi-select field, when the prototype saves, then each selected value is represented as one child row or placeholder row with submission key, field/question identity, choice value, and label/code snapshot.

## AC-07 Repeat/line item

Given the user adds a production-cost line, when the prototype saves, then the line is represented as one repeat/line-item record with stage, item, unit, quantity, cost, and submission key.

## AC-08 Save failure visibility

Given save fails, when the user attempts Save Draft or Continue, then the app shows visible failed state and does not navigate as if the save succeeded.

## AC-09 Review summary

Given the user opens review summary, when in-scope data exists, then the summary shows demographics completion, selected multi-select values, production-cost line items, totals, and validation blockers.

## AC-10 Prototype debt register

Given implementation is complete, when the slice is reviewed, then all project-specific shortcuts are documented as acceptable prototype debt, needs refactor, or blocks platform generalization.
