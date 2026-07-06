# Legacy Requirements Note

Status: superseded for July 7 MVP. The active implementation scope is `docs/mvp-july-7.md`: one assigned published form rendered dynamically from Dataverse metadata with draft/save/submit/history and one attachment field. Microsoft Lists and full XLSForm conversion content below is retained as historical/fallback context.

# TACATDP Power Apps Requirements

## Product objective

Build a Microsoft Power Apps canvas application for TACATDP impact evaluation data collection by transforming the existing XLSForm into a Microsoft Lists-backed app with ODK-like skip patterns, required fields, validations, choice lists, and grouped survey flow, while improving usability beyond the original ODK form where Power Apps enables it.

## Source inputs

### Required inputs

- `Revised_TACATDP impact evaluation_modified_groups.xlsx`
  - Status: available at `docs/Revised_TACATDP impact evaluation_modified_groups.xlsx`.
  - Extracted into generated inventory files:
    - `docs/xlsform-summary.md`
    - `docs/xlsform-field-inventory.csv`
    - `docs/xlsform-logic-map.csv`
    - `docs/xlsform-choice-lists.csv`

### Existing starter implementation

- `app-src/Src/App.pa.yaml`
- `app-src/Src/Screen1.pa.yaml`
- `app-src/Src/_EditorState.pa.yaml`
- `app-src/TACATDP Impact Tracking.msapr`

The starter implementation currently contains a generated form bound to `TACATDP_Main_Data_Fields_Under_300`.

## Workbook-derived scope

The XLSForm source contains 582 survey rows and 71,487 choice rows. The maintained app inventory now contains only data-entry fields: 292 input fields using 47 choice lists, with 288 input required rules, 48 input relevance rules, 16 input constraint rules, and 9 input choice filters. Notes, groups, calculations, and ODK runtime metadata are excluded from the maintained input inventory.

Primary implementation implications:

1. The app needs a guided multi-section structure; the XLSForm has 49 `begin_group` rows, including major sections for agricultural production, irrigation/water/energy, gender and social inclusion, household quantification, ARA-CSA training, beneficiary quantification, safeguards, insurance/guarantees, GHG quantification, water efficiency, yield/income, and detailed production cost/income quantification.
2. The location hierarchy must support filtered `region -> district -> ward -> village` selection.
3. Large choice lists, especially `village` with 66,297 rows, must be implemented as reference data rather than hard-coded control choices.
4. The app must support 20 `select_multiple` input questions.
5. The app must support one `geopoint` question, `Georeference`, using a Power Apps location capture approach or an agreed manual coordinate fallback.
6. XLSForm notes should be rendered only as labels, headings, or helper text; they must not become Microsoft Lists data-entry columns.

## Functional requirements

### Form structure

1. The app must represent the XLSForm survey structure in Power Apps.
2. XLSForm groups should become clear user-facing sections or screens.
3. The app must remove ODK runtime metadata fields from the data-entry flow: `starttime`, `endtime`, `deviceid`, `subscriberid`, `simid`, `devicephonenum`, and `username`, unless a later requirement explicitly maps them to Microsoft 365 audit fields.
4. The app must preserve question labels, hints, choice labels, note text, and group headings from the XLSForm as UI content.
5. The app should split long workflows into manageable sections with clear progress indication.

### Skip patterns

1. Each XLSForm `relevant` expression must be translated into equivalent Power Fx visibility logic.
2. Hidden skipped fields must not block progression or submission.
3. Hidden skipped fields should either remain blank or be cleared according to the agreed data policy.
4. Section-level relevance should hide entire groups when possible instead of only hiding individual fields.

### Validation

1. XLSForm `required` rules must be enforced before section navigation and before final submission.
2. XLSForm `constraint` rules must be translated into Power Fx validation formulas.
3. Validation messages must use XLSForm `constraint_message` text where available.
4. Required and constraint validation must apply only when the field is relevant/visible.
5. Numeric, date, phone, and text fields must enforce appropriate Power Apps control types and Microsoft Lists column types.
6. Submission must be blocked when visible required fields or constraints fail.

### Choice lists

1. `select_one` fields must become single-select controls.
2. `select_multiple` fields must become multi-select controls or an agreed storage model.
3. XLSForm choices must preserve stored values and user-facing labels.
4. Choice dependencies or filtered choices must be implemented where the XLSForm uses cascading or dynamic choice logic.
5. Location choices must be filtered with the XLSForm logic: `CRDB_Branch` by `zone`, `district` by `region`, `ward` by `region` and `district`, and `village` by `region`, `district`, and `ward`.
6. Technology/crop-dependent choices must preserve XLSForm filters for `crop_adaptation`, `climate_risk`, `adaptation`, `additional`, and `SDGs`.

### Calculations and defaults

1. XLSForm calculations must be mapped to Power Fx formulas only where needed for validation, section summaries, or reporting.
2. Computed values should not be treated as input fields.
3. Defaults should be translated into Power Apps default formulas where practical.

### Microsoft Lists persistence

1. The app must write submissions to Microsoft Lists.
2. The Microsoft Lists schema must align with the final field inventory after ODK-only removals.
3. The app must handle save success and failure with clear user feedback.
4. The app must avoid silent save failures.
5. The app must define how large forms are stored if the field count exceeds practical list/form limits.

### User experience

1. The app should feel like a guided survey, not a raw SharePoint list form.
2. Users should always know which section they are in and whether the current section is complete.
3. Error messages should appear near the relevant fields and in a summary when attempting to continue or submit.
4. Controls should be usable on the target devices, including tablets or phones if field collection is mobile.
5. The app should use consistent spacing, labels, required markers, and navigation controls.

## Non-functional requirements

1. The app source must remain version controlled in Git.
2. Changes must be reviewable as source diffs where possible.
3. Packaging/import steps must be repeatable.
4. The implementation must not store secrets or credentials in source files.
5. Validation should be testable through a field mapping/logic inventory before manual app testing.
6. The solution should minimize unsupported manual YAML edits and validate all packed outputs in Power Apps Studio.

## Data requirements

The generated field inventory includes:

- XLSForm row number
- XLSForm `type`
- field `name`
- label
- hint
- required rule
- relevant rule
- constraint
- constraint message
- choice list name
- Power Apps control type
- Microsoft Lists column name
- Microsoft Lists column type
- inclusion/exclusion decision
- notes and risks

## Acceptance criteria

1. The repository contains the XLSForm-derived field inventory.
2. ODK-only fields are identified and excluded or explicitly remapped.
3. Every included XLSForm question has a Microsoft Lists schema mapping.
4. Every included `relevant` expression has a Power Fx equivalent.
5. Every included `required` and `constraint` rule has a Power Apps validation implementation.
6. The app can be packed for import.
7. The imported app can create a valid submission in Microsoft Lists.
8. Invalid visible fields block progression/submission with useful messages.
9. Skipped fields do not block progression/submission.

## Current blockers

- The target Microsoft Lists schema/site/list names are not yet confirmed.
- The final packaging/import path for the `.msapr`/canvas source export needs confirmation with available Power Platform tooling.
- The storage model for large choices, `select_multiple` fields, calculated fields, and location reference data still needs final design.
