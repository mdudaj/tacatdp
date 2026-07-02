# Phase 3 Maker Execution Runbook

## Purpose

This runbook turns the Phase 3 placeholder scaffolds into an ordered Power Apps Studio workflow. The deliverable is repack/import-ready Canvas app artifacts that can be validated in Power Apps Studio, exported, unpacked, reviewed, repacked, and imported again. Do not publish the app and do not connect production SharePoint/Microsoft Lists until the controlled Windows/Power Apps environment is ready.

## Inputs

Use these artifacts together:

| Artifact | Purpose |
| --- | --- |
| `app-src/Src/` | Current unpacked Power Apps source exported from Studio. Treat this as the live app source. |
| `app-src/Src/ScreenShell.pa.yaml`, `FieldRow.pa.yaml`, `ValidationSummary.pa.yaml`, `CommandBar.pa.yaml` | Promoted component artifacts used by the active Canvas source. |
| `app-src/Src/Screen_*.pa.yaml` | Promoted screen artifacts used by the active Canvas source. |
| `artifacts/powerapps/phase3-scaffolds/phase3-canvas-yaml-pack.json` | Inventory of generated component and screen blueprints. |
| `artifacts/powerapps/phase3-scaffolds/components/*.pa.yaml` | Component blueprints for the Phase 3 shell, field rows, command bar, and validation summary. |
| `artifacts/powerapps/phase3-scaffolds/screens/*.pa.yaml` | Screen blueprints for section-level implementation. |
| `docs/design-system.md` | UX/layout contract for one-field-per-row screens, spacing, validation, navigation, and accessibility. |
| `docs/phase-3-requirements.md` | Phase 3 functional and non-functional requirements. |
| `schemas/xlsform-to-list-mapping.csv` | Source of truth for field-to-list mapping. |
| `schemas/sharepoint-lists-schema.json` | Intended Microsoft Lists schema. |

## Non-negotiable gates

1. `artifacts/powerapps/phase3-scaffolds/` is the source scaffold pack for building repack/import-ready Canvas artifacts. Do not overwrite `app-src/Src/` directly from these files without validating the result through Power Apps Studio and the pack/unpack flow.
2. Placeholder data sources are temporary. Keep them named and documented as placeholders until real Microsoft Lists are available.
3. Do not publish, share, or connect production SharePoint/Microsoft Lists from this phase without explicit approval.
4. Every data-entry field must use one field per row by default, with a visible label above the input and helper/error text below it.
5. Hidden or skipped fields must not block Continue, Save Draft, or Submit validation.
6. Run App Checker before any export/import handoff and resolve high-risk formula, accessibility, and delegation findings.

## Scaffold inventory

The active scaffold pack is:

`artifacts/powerapps/phase3-scaffolds/`

It contains:

| Type | Count | Location |
| --- | ---: | --- |
| Component blueprints | 4 | `artifacts/powerapps/phase3-scaffolds/components/` |
| Screen blueprints | 33 | `artifacts/powerapps/phase3-scaffolds/screens/` |
| Pack manifest | 1 | `artifacts/powerapps/phase3-scaffolds/phase3-canvas-yaml-pack.json` |

The active source also contains promoted copies under `app-src/Src/`: 4 component files and 33 screen files. Keep the scaffold pack and promoted source synchronized until Power Apps Studio has normalized and re-exported the app.

## Maker execution order

### 1. Prepare the app safely

1. Open the app in Power Apps Studio from the current exported package.
2. Confirm the app opens without source repair prompts.
3. Save a Studio version checkpoint before adding Phase 3 screens.
4. Confirm `app-src/Src/Screen1.pa.yaml` still represents the current one-screen starter form.
5. Use the generated scaffold files as the build source for the Canvas artifact, then validate the resulting app source through Studio and the pack/unpack flow before treating it as import-ready.

### 2. Create placeholder app state

Create temporary placeholder collections in `App.OnStart` or named formulas where Studio supports them:

| Placeholder | Intended future source |
| --- | --- |
| `placeholder_tacatdp_submissions` | `TACATDP_Submissions` |
| `placeholder_tacatdp_production_cost_repeat` | `TACATDP_ProductionCostLines` |
| `placeholder_zone` | Zone/reference list |
| `placeholder_branch` | Branch/reference list |
| `placeholder_region` | Region/reference list |
| `placeholder_district` | District/reference list |
| `placeholder_ward` | Ward/reference list |
| `placeholder_village` | Village/reference list |

Minimum placeholder startup behavior:

1. Clear and seed `colValidationSummary`.
2. Clear and seed one sample submission record with a temporary `SubmissionKey`.
3. Seed small region/district/ward/village samples only; do not model full village volume in local collections.
4. Add a visible banner or label stating `Placeholder data only - replace before publish`.

The current source seeds placeholder collections in `app-src/Src/App.pa.yaml` so the promoted source has a concrete placeholder seam before live Microsoft Lists are ready.

### 3. Build reusable components first

Create components in this order:

1. `ScreenShell`
2. `FieldRow`
3. `ValidationSummary`
4. `CommandBar`

Map them to the design-system roles:

| Scaffold component | Design-system role | Required behavior |
| --- | --- | --- |
| `ScreenShell` | App header, section progress, content surface | 24px screen padding, clear title, section/progress text, placeholder warning. |
| `FieldRow` | Field wrapper | One field per row, visible label, required marker, helper text, inline error text, minimum 44px interactive target. |
| `ValidationSummary` | Blocked navigation summary | Appears above command bar after Continue/Submit is blocked. |
| `CommandBar` | Footer command bar | Back, Save Draft, Continue/Next, and Submit formulas are visible and consistent. |

Component QA before screens:

1. Resize the app canvas and confirm component spacing does not collapse.
2. Confirm label, helper, and error text remain readable.
3. Confirm keyboard focus order goes top-to-bottom.
4. Confirm errors are text-visible and not color-only.

### 4. Build the screen skeleton

Create screens in the same order as `phase3-canvas-yaml-pack.json`. Start with:

1. `Screen_main`
2. `Screen_section_2`
3. `Screen_section_3`
4. `Screen_section_4`
5. Continue through the remaining scaffolded screens.
6. Add `Screen_summary` before the production-cost repeat detail screen.
7. Add `Screen_production_cost_repeat_Detail` last.

For each screen:

1. Add `ScreenShell` at the top.
2. Add field rows in the scaffolded order.
3. Use one field row per visible question unless a repeat/line-item component is explicitly required.
4. Add `ValidationSummary` above the command bar.
5. Add `CommandBar` at the bottom.
6. Wire Back/Next navigation only to existing adjacent screens.
7. Keep save/submit formulas in placeholder mode until real Microsoft Lists are connected.

### 5. Wire validation behavior

For each screen:

1. Clear `colValidationSummary` when Continue or Submit starts.
2. Validate only visible/relevant fields.
3. Collect one row per blocked field with screen, field label, message, and control name.
4. Show inline error text below the relevant field row.
5. Show the section-level validation summary when `CountRows(colValidationSummary) > 0`.
6. Block navigation when the summary has errors.

Required validation pattern:

```powerfx
Clear(colValidationSummary);
If(
    <field is visible> && IsBlank(<field value>),
    Collect(
        colValidationSummary,
        {
            Screen: "<screen name>",
            Field: "<field label>",
            Message: "<field label> is required.",
            Control: "<control name>"
        }
    )
);
If(CountRows(colValidationSummary) = 0, Navigate(<next screen>, ScreenTransition.Fade));
```

### 6. Wire placeholder save behavior

Use local collections only in this phase:

1. Save Draft patches or updates the placeholder submission collection.
2. Save failures must show a visible failed state; do not silently continue.
3. Multi-select and repeat sections can use local child collections shaped like `TACATDP_MultiSelectAnswers` and `TACATDP_ProductionCostLines`.
4. Keep formulas shaped so collection names can be swapped section-by-section for Microsoft Lists later.

### 7. Prepare for later Microsoft Lists replacement

Before replacing placeholders later:

1. Confirm the SharePoint site URL.
2. Confirm list display names and internal names.
3. Import reference data.
4. Confirm Power Apps data-source names in Studio.
5. Replace placeholder collections section by section, not all at once.
6. Re-run App Checker after each replacement.
7. Use Monitor for save tests to confirm failed writes are surfaced.

## Manual QA checklist

### Layout and spacing

- [ ] Each data-entry screen uses one field per row by default.
- [ ] Labels are visible above inputs.
- [ ] Helper text and error text appear below inputs.
- [ ] Screens use 24px outer padding.
- [ ] Field rows use consistent vertical spacing, targeting 16px row gaps.
- [ ] Interactive controls meet a minimum 44px touch target.
- [ ] Long labels wrap without overlapping inputs.

### Accessibility

- [ ] Keyboard/tab focus order is top-to-bottom.
- [ ] Every input has a visible label and accessible name.
- [ ] Validation errors are communicated with text, not color alone.
- [ ] Save state and placeholder state are visible as text.
- [ ] Header, progress, content, summary, and command bar are visually distinct.

### Navigation

- [ ] Back and Next routes match the scaffold order.
- [ ] Users can tell the current section and next action.
- [ ] Blocked Continue keeps the user on the same screen.
- [ ] Summary/review route does not bypass incomplete required visible fields.

### Validation

- [ ] Required visible fields block Continue.
- [ ] Hidden/skipped fields do not block Continue.
- [ ] Inline field error appears below the relevant field.
- [ ] Section validation summary appears above the command bar.
- [ ] Validation summary rows identify the field and fix needed.

### Placeholder data

- [ ] Placeholder collections are clearly named with `placeholder_`.
- [ ] No production SharePoint URL, list ID, credential, or connection name is hard-coded.
- [ ] Placeholder warning is visible in the app.
- [ ] Save Draft uses local placeholder state only.
- [ ] Publish is blocked until placeholders are replaced.

### App Checker and export readiness

- [ ] App Checker has no unresolved severe formula errors.
- [ ] App Checker has no unresolved accessibility findings affecting data entry.
- [ ] Delegation warnings are documented and not caused by large reference lists.
- [ ] Studio save succeeds after changes.
- [ ] Export/unpack source can be reviewed without losing `artifacts/powerapps/phase3-scaffolds/`.

## Completion criteria for this slice

Phase 3 maker execution is ready when:

1. Components exist in `app-src/Src/` with matching names.
2. Screen skeletons exist in `app-src/Src/` and are listed in `_EditorState.pa.yaml` in scaffold order.
3. Placeholder data state is visible and isolated.
4. The changed Canvas source can be exported/unpacked, reviewed, repacked, and imported without losing scaffolded screens or components.
5. Manual QA checklist items are completed or documented as blocked by Windows/Power Apps readiness.
6. The app remains unpublished until placeholder sources are replaced and approved.
