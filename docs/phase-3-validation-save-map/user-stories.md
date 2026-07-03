# User Stories: Phase 3 Validation and Save Map

## Story VSM-US-01: Screen-level required validation

As an enumerator, I want each screen to validate required visible fields before I continue, so that I do not move through the survey with missing required data.

Acceptance criteria:

1. Continue evaluates only controls whose relevance/visibility formula is true.
2. Blank visible required fields are blocked.
3. Hidden/skipped required fields do not block navigation.
4. Each blocked field shows inline error text below the field.
5. A validation summary lists every blocked field on the screen.

## Story VSM-US-02: One-row field UX

As an enumerator, I want every data-entry field presented in a readable one-field-per-row layout, so that long TACATDP sections remain understandable on field devices.

Acceptance criteria:

1. Each field row has a visible label above the input.
2. Helper or error text appears directly below the input.
3. Field row spacing remains consistent across all 33 screens.
4. Error state is not communicated by color alone.
5. Focus order follows the visual top-to-bottom row order.

## Story VSM-US-03: Save Draft placeholder behavior

As an enumerator, I want to save a draft while lists are not yet connected, so that makers and reviewers can test save UX without production SharePoint writes.

Acceptance criteria:

1. Save Draft writes to placeholder collections that mirror future Microsoft Lists.
2. Saved placeholder records include `SubmissionKey`.
3. Save state visibly changes to saving, saved, or save-failed.
4. Save failures show an explicit error state and do not appear successful.
5. The placeholder-to-real-list replacement seam is documented.

## Story VSM-US-04: Microsoft Lists save mapping

As a data engineer, I want every screen to declare its target Microsoft Lists save destination, so that later SharePoint wiring preserves the intended schema.

Acceptance criteria:

1. Scalar demographic and section fields map to their section lists.
2. `select_multiple` values map to `TACATDP_MultiSelectAnswers`.
3. Production cost detail rows map to `TACATDP_ProductionCostLines`.
4. All saved child rows carry `SubmissionKey`.
5. Internal column names come from `schemas/sharepoint-lists-schema.json`.

## Story VSM-US-05: Beneficiary stage consistency

As a program reviewer, I want beneficiary stage screens to use the same validation and save pattern, so that stage totals are comparable and reviewable.

Acceptance criteria:

1. Screens 08 through 25 use the same beneficiary-stage validation pattern.
2. Numeric count fields reject invalid nonnumeric values.
3. Each stage saves a stage-specific row or record in the beneficiary save target.
4. `Screen_26_beneficiary_summary` presents totals and completion status without adding unrelated data-entry fields.

## Story VSM-US-06: Final review readiness

As a QA reviewer, I want validation blockers to be traceable across screens, so that final submit cannot bypass incomplete required visible data.

Acceptance criteria:

1. Each screen exposes a section completion state.
2. The final review can identify incomplete sections.
3. Submit remains blocked while any required visible section field is invalid.
4. Review links or directions identify which screen needs correction.

## Story VSM-US-07: Import-safe implementation

As a maker, I want validation and save behavior added without breaking app import/open behavior, so that we do not return to `ErrOpeningDocument_UnknownError`.

Acceptance criteria:

1. Implementation starts from the native-control import candidate.
2. Generated custom component YAML is not promoted into live `Src/` unless Studio or supported tooling normalizes it.
3. Packing/import checks use the documented `.msapp` recovery strategy.
4. App Checker is run in Studio before export handoff.

