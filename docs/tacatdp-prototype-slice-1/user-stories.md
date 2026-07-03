# User Stories: TACATDP Prototype Slice 1

## P1-US-01: Start a TACATDP prototype submission

As an enumerator, I want to start a TACATDP prototype submission so that the app can capture data for the first project without asking me to understand the future Project platform.

Acceptance:

1. The app initializes project/instrument/version context for TACATDP.
2. The current submission has a stable submission key.
3. The UI makes clear when placeholder/prototype storage is being used.

## P1-US-02: Complete demographics with cascading geography

As an enumerator, I want to enter demographics and choose region, district, ward, and village from filtered lists so that location data is accurate and not overloaded by full village lists.

Acceptance:

1. Districts filter by selected region.
2. Wards filter by selected region and district.
3. Villages filter by selected region, district, and ward.
4. Required visible fields and constraints show inline errors before navigation/save.

## P1-US-03: Capture one multi-select answer

As an enumerator, I want to select multiple agricultural values so that the prototype proves child-row storage for multi-select questions.

Acceptance:

1. Each selected value is represented as a separate child row or placeholder row.
2. Deselecting a value removes or marks the corresponding child row.
3. Review summary displays selected values.

## P1-US-04: Add one production-cost line item

As an enumerator, I want to add a production-cost line item so that the prototype proves repeat/line-item behavior.

Acceptance:

1. I can add a line with stage, cost item, unit, quantity, and cost.
2. I can edit or remove the line before submission.
3. Review summary displays the line and calculated total.

## P1-US-05: Save draft and review

As a reviewer, I want to see saved prototype data and validation blockers so that I can verify the slice is ready before wider implementation.

Acceptance:

1. Save Draft persists the in-scope fields and child rows.
2. Failed saves show an explicit failed state.
3. Review summary lists incomplete required fields and saved repeat/multi-select data.
