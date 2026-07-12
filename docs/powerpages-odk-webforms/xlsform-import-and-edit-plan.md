# XLSForm Import, Edit Semantics, and Record List Plan

Date: 2026-07-12

## Evidence

- The current MVP bug is reproducible from source behavior: `AssignedFormsView.vue` opens saved records with `editInstance`, but `PowerPagesApiClient.submitOdkSubmission` previously selected the target submission only from the submitted XML `instanceID`. ODK XForms engine edit mode may assign a new `instanceID` for an edited instance, so relying on the emitted XML id can create a new Dataverse `Submissions` row.
- Local ODK dependency source documents edit initialization behavior: when editing, the previous `instanceID` can become `deprecatedID`, and a new instance id may be assigned for `uid` preload behavior. Therefore TACATDP must bind edit submit to the selected Dataverse submission row, not only to the emitted XML id.
- `@getodk/web-forms` README documents `editInstance` as the prop used to resolve and load instance/attachment resources for editing, and `submit` / `submitChunked` as the valid-form events.
- The revised XLSForm artifact exists at `docs/Revised_TACATDP impact evaluation_20260712.xlsx`.
- XLSX inspection found:
  - `survey`: 583 rows.
  - `choices`: 71,486 rows.
  - `settings.form_title`: `TACATDP_Impact_Data_Tracking_Tool`.
  - `settings.form_id`: `tacatdp_impact_evaluation`.
  - `settings.version`: `2607121652`.
  - `settings.instance_name`: `concat(${Customer_ID}, ":", ${Customer_Name})`.
- Official pyxform sources:
  - GitHub `XLSForm/pyxform` says pyxform converts XLSForm spreadsheets into ODK XForms and is actively maintained by ODK.
  - PyPI shows `pyxform 4.5.0`, released 2026-06-25, requiring Python `>=3.10`.
  - pyxform supports `xls2xform path_to_XLSForm [output_path]`.
- ODK/XLSForm docs recommend settings `form_title`, `form_id`, `version`, and `instance_name`. ODK docs describe `version` as a unique form version code, commonly timestamp-like, and `instance_name` as an expression used to represent a filled form.

## Requirements

### Edit Semantics

- Opening a saved record and submitting it must update the selected Dataverse submission by creating a new `SubmissionVersions` row for the same `Submissions` row.
- Edit submit must not create a new `Submissions` row even if ODK Web Forms emits a new XML `instanceID`.
- The canonical Dataverse `mp_instanceid` for edit mode is the selected saved record's `instanceId`.
- The submitted XML stored in `SubmissionVersions.XFormSubmissionXml` must have `<instanceID>` normalized to the canonical selected record id for consistency.
- A new submission may create a new `Submissions` row only from the Add new path.

### Record Display

- Data list cards must show the XLSForm `settings.instance_name` result as the primary card title when available.
- For the revised TACATDP form, the MVP display expression is `concat(${Customer_ID}, ":", ${Customer_Name})`.
- If `instance_name` cannot be computed or fields are empty, fall back to the canonical instance id.
- Search must include both display name and canonical instance id.

### Pagination

- Saved and Draft lists remain 10 records per page.
- Pagination must sit after the current list, be visually separated from cards, and use icon+text controls with clear disabled states.
- Page state must reset to page 1 after submit, search text changes, and tab changes.

### Form Versioning

- New published XLSForm versions should default to timestamp-style version codes from the XLSForm settings sheet.
- For the current revised artifact, use `2607121652` unless the form owner confirms a newer timestamped workbook.
- Future generated versions should use a stable timestamp convention such as `YYYYMMDDHHmm` or preserve the XLSForm `settings.version` if populated.

### XLSForm Import

- Use pyxform as the compiler for the MVP full form, not a hand-authored XForm string.
- The import pipeline must:
  - accept one XLSForm `.xlsx`;
  - run pyxform/xls2xform validation and conversion;
  - extract settings metadata;
  - persist the generated XForm XML to `FormVersions.XFormXml`;
  - seed/update the published form version and assignments;
  - preserve the source workbook under `docs/` or `artifacts/` without committing temporary lock files.
- The pipeline must not use `submission_url` from the XLSForm for browser submission because TACATDP writes through Power Pages `/_api` into Dataverse.

## Implementation Plan

1. **Bug fix: edit submit**
   - Inspect `AssignedFormsView.vue`, `PowerPagesApiClient.submitOdkSubmission`, and ODK `FormInstanceEditMode` source.
   - Pass `selectedEditSubmission` into submit.
   - In the API client, use selected `submissionId` and `instanceId` as the canonical edit target.
   - Normalize stored XML `<instanceID>` to the selected record id.
   - Validate that edit submit creates version `n+1` and does not create a new submission header.

2. **Record labels**
   - Add `displayName` to `SubmissionSummary`.
   - Store `instanceName` in `SubmissionVersions.SubmissionJson`.
   - For the revised form, compute `Customer_ID:Customer_Name` as the MVP expression result.
   - Replace card title with `displayName || instanceId`.
   - Include `displayName` in search.

3. **Pagination polish**
   - Keep pagination below the rendered list.
   - Style pagination as a compact action bar with CRDB token colors, icon buttons, page text, disabled states, and mobile stacking.
   - Validate page reset on submit/search/tab change.

4. **Full XLSForm import**
   - Add package review for `pyxform`.
   - Install `pyxform==4.5.0` in a project-local tool environment after approval.
   - Add `scripts/xlsform-compile.py` that wraps `xls2xform` or pyxform library calls.
   - Compile `docs/Revised_TACATDP impact evaluation_20260712.xlsx` to XForm XML.
   - Validate generated XML parses and has unique body refs.
   - Update the Dataverse seed script to load generated XML and settings metadata instead of embedding `RICH_TACATDP_XFORM`.
   - Execute Dataverse write only after dry-run output is reviewed.

## Verification Gates

- `python3 scripts/validate-webforms-spa-foundation.py` passes.
- `npm run build` passes in `powerpages/webforms-spa/`.
- pyxform conversion produces an XForm XML file from `Revised_TACATDP impact evaluation_20260712.xlsx`.
- Generated XForm has form id `tacatdp_impact_evaluation`, version `2607121652`, and an instance-name path matching `Customer_ID` and `Customer_Name`.
- Browser edit test:
  - open an existing saved card;
  - edit one value;
  - submit;
  - Saved list count does not increase from the edit;
  - card remains the same logical record;
  - latest version number increments by 1.
- Browser add-new test:
  - Add new creates one new card;
  - card title uses `Customer_ID:Customer_Name` when populated.

## References

- pyxform GitHub: https://github.com/XLSForm/pyxform
- pyxform PyPI: https://pypi.org/project/pyxform/
- XLSForm settings and instance name: https://docs.getodk.org/xlsform/
- XLSForm reference: https://xlsform.org/en/
- ODK Web Forms package source in `powerpages/webforms-spa/node_modules/@getodk/web-forms/README.md`
- ODK XForms engine edit behavior in `powerpages/webforms-spa/node_modules/@getodk/xforms-engine/src/client/form/FormInstance.ts`
