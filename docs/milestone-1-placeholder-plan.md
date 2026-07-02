# Milestone 1 Placeholder Plan

## Context

Microsoft Lists creation is currently blocked by the controlled Windows environment while PowerShell 7+ and PnP.PowerShell access are being resolved. Milestone 1 should therefore focus on the app shell, design system, placeholder screens, and replaceable local data scaffolding.

## Goal

Create a reviewable Power Apps prototype structure that matches the final TACATDP app architecture without depending on live Microsoft Lists connections.

## Scope

Milestone 1 includes:

1. App shell placeholder.
2. Section progress placeholder.
3. Screen map placeholder.
4. Reusable component placeholders.
5. Local sample collections matching the generated schema shape.
6. Placeholder validation summary and save-status behavior.
7. Documentation showing exactly where Microsoft Lists will replace placeholder data.

Milestone 1 excludes:

1. Live SharePoint/Microsoft Lists writes.
2. Production app import or publish.
3. Reference-data import into Microsoft Lists.
4. Final Power Fx save orchestration against real data sources.
5. Offline sync design beyond placeholder/draft state concepts.

## Placeholder data strategy

Use local collections with names that make their temporary status obvious:

| Placeholder collection | Future data source |
| --- | --- |
| `colPlaceholderSubmissions` | `TACATDP_Submissions` |
| `colPlaceholderProfile` | `TACATDP_Profile` |
| `colPlaceholderReferenceChoices` | `TACATDP_RefChoices` and location reference lists |
| `colPlaceholderMultiSelectAnswers` | `TACATDP_MultiSelectAnswers` |
| `colPlaceholderProductionCostLines` | `TACATDP_ProductionCostLines` |

Sample rows should be derived from:

- `schemas/sharepoint-fields.csv`
- `schemas/xlsform-to-list-mapping.csv`
- `schemas/reference-data/*.csv` samples only, not the full village list in-app.

## Milestone 1 screens

| Screen | Placeholder objective |
| --- | --- |
| `scrHome` | Start/resume cards using sample submissions |
| `scrProfile` | First guided section with local sample values |
| `scrAgriculture` | Demonstrate select/multi-select placeholder patterns |
| `scrReviewSubmit` | Show section completion and blocked-submit placeholder |

These screens are enough to validate shell, progress, field layout, validation, and navigation before expanding all sections.

## Milestone 1 components

Implement or stub:

- `cmpAppHeader`
- `cmpSectionProgress`
- `cmpSectionCard`
- `cmpFieldShell`
- `cmpValidationSummary`
- `cmpReferenceComboBox`
- `cmpFooterCommandBar`
- `cmpSaveStatus`

Each component should follow `docs/design-system.md`.

## Acceptance criteria

1. The prototype clearly shows the TACATDP survey shell and section navigation.
2. Placeholder data is visibly temporary and easy to replace.
3. `scrProfile` demonstrates field labels, hints, required markers, errors, and save state.
4. `scrAgriculture` demonstrates reference choice and `select_multiple` behavior with sample data.
5. `scrReviewSubmit` demonstrates section completion and blocked-submit UX.
6. No live SharePoint writes are required.
7. The design system contract is followed.

## Exit criteria

Milestone 1 is complete when the placeholder prototype can be reviewed for UX and component structure while Microsoft Lists setup remains blocked.

Once Lists are available, the next milestone swaps placeholder collections for real data sources section by section.
