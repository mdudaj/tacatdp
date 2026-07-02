# TACATDP Power Apps Implementation Plan

## Phase 0: Repository baseline

Status: mostly complete.

1. Confirm repository remote is `git@github.com:mdudaj/tacatdp.git`.
2. Keep exported Power Apps source under `app-src/`.
3. Add project documentation under `docs/`.
4. Add the XLSForm workbook or a sanitized copy to the repository if it is safe to version, or store it in an agreed non-Git location and document the path.

## Phase 1: XLSForm analysis

Status: complete for first-pass extraction.

1. Read workbook sheets: `survey`, `choices`, `settings`, and any custom sheets.
2. Produce a field inventory from the workbook.
   - Done: `docs/xlsform-field-inventory.csv`
3. Identify and remove ODK-only metadata fields such as `start`, `end`, `deviceid`, and `username`.
   - Done: exclude `starttime`, `endtime`, `deviceid`, `subscriberid`, `simid`, `devicephonenum`, and `username` from the data-entry flow.
4. Identify unsupported or high-risk XLSForm constructs:
   - repeats
   - nested groups
   - select_multiple fields
   - cascading choices
   - calculations
   - external choice lists
   - media fields
   - geolocation fields
   - signatures or attachments
5. Produce a logic map for input-field required, relevant, constraint, default, and choice-filter expressions.
   - Done: `docs/xlsform-logic-map.csv`

First-pass findings:

- 582 source survey rows
- 292 maintained input fields
- 290 excluded non-input rows
- 47 input choice lists
- 71,487 choice rows
- 288 input required rules
- 48 input relevance rules
- 16 constraint rules
- 98 source calculations excluded from the input inventory
- 9 choice filters
- 20 `select_multiple` questions
- 1 `geopoint` question
- 0 duplicate input field names

## Phase 2: Microsoft Lists schema design

Status: schema artifacts prepared; research and recommended architecture documented in `docs/list-schema-design.md`, with import guidance in `docs/schema-import-guide.md`.

1. Decide whether the data model is one primary list, multiple linked lists, or a normalized design for repeats/select_multiple values.
   - Recommended: hybrid parent/section/child/reference-list model.
2. Map each included XLSForm field to a Microsoft Lists column.
   - Done: `schemas/xlsform-to-list-mapping.csv`
3. Define column internal names, display names, types, required flags, and choice values.
   - Done: `schemas/sharepoint-lists-schema.json` and `schemas/sharepoint-fields.csv`
4. Decide audit field strategy:
   - Microsoft-created/modified fields
   - `User().Email`
   - enumerator/team metadata
   - submission timestamp
5. Confirm list/site names and permissions.
   - Pending: target SharePoint site URL and permissions.

Recommended direction for this workbook:

1. Use one primary submissions list for scalar survey answers.
2. Use separate reference lists for high-volume choices and cascading location data.
3. Use either Microsoft Lists multi-choice columns or child response lists for `select_multiple` fields; choose child lists if reporting needs stable one-row-per-choice analytics.
4. Keep calculations out of the input schema unless a derived value must be persisted for reporting/export; otherwise calculate in-app and/or in downstream reporting.

## Phase 3: App architecture

1. Replace the one-screen generated form with a guided multi-section structure based on XLSForm groups.
2. Define reusable formulas or variables for:
   - section completion
   - field visibility
   - field validation
   - submit eligibility
   - save error handling
3. Decide whether to use `SubmitForm` for generated form cards, `Patch` for a custom form, or a hybrid.
4. Use `SubmitForm` where generated form behavior is sufficient.
5. Use explicit `Patch` only where custom multi-screen behavior requires it, with manual validation before saving.

## Phase 4: Implement field controls and logic

1. Create controls/cards for all included fields.
2. Apply Power Fx `Visible` formulas from XLSForm `relevant` expressions.
3. Apply required-field and constraint validation.
4. Implement choices and filtered choices.
5. Implement calculated/read-only fields.
6. Add section navigation and progress indicators.
7. Add final review and submit experience.

## Phase 5: Packaging and import

1. Install or confirm Power Platform CLI availability.
2. Pack the source into an importable app package.
3. Import/open the app in Power Apps Studio.
4. Resolve schema/control issues surfaced by Studio.
5. Re-export/unpack if Studio normalizes source files.

## Phase 6: Verification

1. Validate required fields, constraints, and skip logic against a test matrix derived from the XLSForm.
2. Submit happy-path records to Microsoft Lists.
3. Submit invalid records and confirm clear blocking errors.
4. Test skipped fields and confirm they do not block submission.
5. Test save failure handling.
6. Test on target devices and screen sizes.

## Immediate next actions

1. Confirm target Microsoft Lists site/list names and whether the app must support offline collection.
2. Decide storage strategy for `select_multiple`, large reference choices, calculated values, and `Georeference`.
3. Create the Microsoft Lists schema mapping columns in `docs/xlsform-field-inventory.csv`.
4. Decide whether the app should be delivered as a standalone canvas app package or as part of a Power Platform solution.
