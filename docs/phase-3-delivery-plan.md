# Phase 3 Delivery Plan

## Delivery strategy

Deliver Phase 3 as architecture and implementation preparation before editing the canvas app source heavily. The goal is to avoid turning the exported YAML into an unmaintainable hand-edited form.

Use `docs/phase-3-maker-runbook.md` as the ordered Power Apps Studio execution guide and manual QA gate for the active scaffold pack under `app-src/phase3-scaffolds/` and the promoted Canvas source artifacts under `app-src/Src/`.

## Milestones

### 1. Placeholder UX and component prototype

Status: selected as Milestone 1 while the Windows/PowerShell environment is controlled and Microsoft Lists cannot yet be created.

Inputs:

- `docs/design-system.md`
- `docs/milestone-1-placeholder-plan.md`
- `schemas/sharepoint-fields.csv`
- `schemas/xlsform-to-list-mapping.csv`

Outputs:

- Placeholder app shell.
- Placeholder section progress.
- Placeholder reusable components.
- Placeholder `scrHome`, `scrProfile`, `scrAgriculture`, and `scrReviewSubmit`.
- Local sample collections shaped for later replacement with Microsoft Lists.

### 2. Confirm runtime environment

Inputs:

- SharePoint site URL.
- Created Microsoft Lists.
- Imported reference data.
- Power Apps Studio access.
- Target device profile.

Outputs:

- Confirmed data source names in Power Apps.
- Connection names and list availability documented.

### 3. Define app shell and reusable components

Create or specify these reusable patterns:

- `cmpAppHeader`
- `cmpSectionProgress`
- `cmpSectionCard`
- `cmpFieldShell`
- `cmpValidationSummary`
- `cmpReferenceComboBox`
- `cmpFooterCommandBar`
- `cmpSaveStatus`

The names are proposed Power Apps component names; they can be adjusted to match Power Apps Studio conventions.

### 4. Define screen map

Recommended screens:

| Screen | Purpose |
| --- | --- |
| `scrHome` | Start/resume submissions |
| `scrProfile` | Customer, demographics, location, georeference |
| `scrAgriculture` | Crops, technologies, climate risk/adaptation |
| `scrResourceEfficiency` | Irrigation, water, energy |
| `scrSocialInclusion` | Farmer group, household, training |
| `scrBeneficiaries` | Value-chain beneficiary counts |
| `scrSafeguardsClimate` | Safeguards and climate risk |
| `scrInsuranceGuarantee` | Insurance and guarantee linkage |
| `scrGHGWaterYield` | GHG, water efficiency, yield/income |
| `scrProductionIncome` | Cost/income summary and production metrics |
| `scrReviewSubmit` | Review validation status and submit |

### 5. Define Power Fx formula conventions

Use clear naming:

- `varSubmissionKey`
- `varCurrentSection`
- `varSaveState`
- `varValidationAttempted`
- `colSectionErrors`
- `colVisibleFields`
- `colSelectedMultiAnswers`
- `colProductionCostLines`

Reusable formula categories:

- `Is<FieldName>Visible`
- `Is<FieldName>Valid`
- `FieldNameError`
- `CanContinue<Section>`
- `Save<Section>`

### 6. Implement data loading

Data loading should be section-aware:

1. Load current parent submission by `SubmissionKey`.
2. Load only the active section row.
3. Load child rows for active section only.
4. Load large reference choices on demand with delegable filters.
5. Do not load all villages at app start.

### 7. Implement save orchestration

Recommended flow:

1. Ensure `TACATDP_Submissions` parent exists.
2. Validate active section.
3. Patch active section scalar list.
4. Replace or upsert active section multi-select child rows.
5. Replace or upsert production cost lines for production section.
6. Update parent `LastSavedAt` and `SubmissionStatus`.
7. Surface failures through `Notify`, save status text, and validation summary.

### 8. Implement review and submit

The review step should:

- show section completion status,
- block submit on incomplete required visible fields,
- allow jumping back to incomplete sections,
- mark parent `SubmissionStatus` as `Submitted`,
- set `SubmittedAt`.

### 9. Verification

Minimum verification scenarios:

1. Create a new happy-path submission.
2. Save draft and resume.
3. Verify skipped fields do not block Continue/Submit.
4. Trigger each known constraint category:
   - phone format,
   - loan amount minimum,
   - yield after >= baseline,
   - non-negative counts,
   - youth count <= total members,
   - target group count-selected >= 1.
5. Select region/district/ward/village and confirm village filtering is complete and delegable.
6. Save multi-select answers and confirm child rows.
7. Save production cost lines and confirm normalized rows.
8. Run App Checker and address delegation warnings affecting large lists.
9. Use Monitor during save to confirm failed writes are surfaced.

## Implementation order

1. Build placeholder app shell and section progress using local sample data.
2. Implement placeholder `scrProfile` as the design-system pilot.
3. Implement placeholder `scrAgriculture` to demonstrate reference ComboBox and `select_multiple` UX.
4. Implement placeholder validation summary and save status.
5. Implement placeholder `scrReviewSubmit`.
6. Connect generated Microsoft Lists as data sources after the Windows/PowerShell environment is ready.
7. Swap placeholder collections for real data sources section by section.
8. Implement real `Patch` save orchestration.
9. Replicate section patterns across remaining screens.
10. Repack/export source and validate source-control diff.

Before any publish or production connection, complete the manual QA checklist in `docs/phase-3-maker-runbook.md` and confirm that all `placeholder_*` sources have been replaced or remain intentionally blocked.

## Risks

- Power Apps YAML source may not support large manual structural edits reliably; Studio validation is required.
- Modern controls may lack a needed behavior, requiring a controlled fallback to classic controls.
- Reference-data imports may be slow for 66,297 villages.
- Offline collection is not designed yet; if required, it changes the data loading/save strategy.
- Complex formulas can drift if copied section-by-section; reusable components/formula conventions are required.
- Placeholder screens can become technical debt if they do not follow `docs/design-system.md`.
