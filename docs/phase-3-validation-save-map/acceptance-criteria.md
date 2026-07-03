# Acceptance Criteria: Phase 3 Validation and Save Map

## System-level acceptance criteria

1. Given the Phase 3 app has 33 chronological screens, when the validation/save implementation begins, then each screen has an explicit validation and save target in `product-requirements-document.md`.
2. Given a visible required field is blank, when an enumerator presses Continue, then navigation is blocked, inline error text appears below the field, and the validation summary includes that field.
3. Given a required field is hidden by relevance logic, when an enumerator presses Continue, then that hidden field does not block navigation.
4. Given an enumerator presses Save Draft during placeholder mode, when all placeholder save operations succeed, then the draft state is visibly saved and the placeholder record includes `SubmissionKey`.
5. Given a placeholder or future SharePoint save operation fails, when Save Draft or Submit is attempted, then the UI shows save-failed state and does not show a successful save.
6. Given a field is a multi-select answer, when it is saved, then each selected value becomes a child row shaped for `TACATDP_MultiSelectAnswers`.
7. Given a production cost detail is added, when it is saved, then it becomes one normalized row shaped for `TACATDP_ProductionCostLines`.
8. Given ODK metadata fields are captured automatically or omitted, when the app is reviewed, then fields from `start` through `username` are not visible data-entry rows.
9. Given the maker repacks the app, when the app is opened/imported in Studio, then the app must not regress to a generated custom-component source pattern known to trigger `ErrOpeningDocument_UnknownError`.
10. Given a section has large reference choices, when the implementation uses reference data, then it uses delegation-safe filtering or records an explicit bounded-data rationale.

## Screen-specific acceptance criteria

| Screen range | Acceptance behavior |
| --- | --- |
| `Screen_01_demographics` | Starts with `Customer ID`; validates required demographics, phone format, loan amount, location cascade, and profile save target. |
| `Screen_02_agricultural_production` | Validates required crop/technology selections and saves multi-select answers as child rows. |
| `Screen_03` through `Screen_04` | Validates section-specific required visible fields and saves to resource-efficiency and social-inclusion targets. |
| `Screen_05` through `Screen_25` | Uses a consistent beneficiary-stage validation/save pattern and numeric count validation. |
| `Screen_26_beneficiary_summary` | Shows summary/completion state and does not introduce unrelated required input. |
| `Screen_27` through `Screen_31` | Validates safeguards, insurance, GHG, water, yield, and income fields against their section targets. |
| `Screen_32_production_cost_income` | Validates production income summary fields and supports navigation to production cost detail entry. |
| `Screen_33_production_cost_detail` | Validates one line item and saves a normalized production-cost child row. |

## Review acceptance criteria

1. Protocol trace `20260703-071158-1facb9` has attached requirements, PRD, stories, acceptance criteria, traceability, readiness, definition of done, verification summary, and handoff artifacts.
2. The artifact pack records the model route used for planning and the route recommended for implementation.
3. The next implementation slice can proceed without rereading the whole conversation history.

