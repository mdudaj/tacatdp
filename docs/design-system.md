# TACATDP Power Apps Design System

## Purpose

Define the UX and component layout rules for the TACATDP canvas app before implementation begins. This keeps Milestone 1 placeholder screens aligned with the final app instead of creating throwaway page-local layouts.

## Skill guidance

Use these Karakana skills together for UX and component layout work:

1. `design-system-governance` - governs durable UI rules, reusable components, spacing, accessibility, and visual consistency.
2. `power-platform-canvas-apps` - governs Power Apps, Microsoft Lists, Power Fx, delegation, save orchestration, and Fluent/Material design tradeoffs.
3. `requirements-elicitation` - keeps UX decisions tied to Phase 3 requirements and unresolved choices.

No additional skill is needed yet. If future work reveals repeated Power Apps component implementation patterns that are not covered by `power-platform-canvas-apps`, add a narrower implementation skill later.

## Design direction

TACATDP should look native to Microsoft 365:

- Use Power Apps modern controls and Fluent UI where feasible.
- Use Material Design principles for structure, labels, helper text, error states, progress, navigation clarity, touch targets, and accessibility.
- Avoid page-local styling and one-off screen layouts.
- Prefer reusable components and tokens over copied control settings.

## App layout contract

Every data-entry screen should follow this structure:

1. **App header**
   - App title.
   - Current submission status.
   - Save status.
   - Optional enumerator identity.
2. **Section progress**
   - Current section name.
   - Step position, for example `Section 3 of 10`.
   - Complete/incomplete/error status.
3. **Content surface**
   - One active section at a time.
   - Section card with title, description, and visible fields.
   - Inline validation messages.
4. **Footer command bar**
   - Back.
   - Save draft.
   - Continue.
   - Review/Submit on final step.
5. **Validation summary**
   - Visible after blocked Continue/Submit.
   - Lists missing or invalid visible fields.

## Component contract

| Component | Purpose | Required behavior |
| --- | --- | --- |
| `cmpAppHeader` | Top-level app context | Shows app title, submission status, save state, and user identity when available |
| `cmpSectionProgress` | Survey progress | Shows step number, section title, and completion/error state |
| `cmpSectionCard` | Section content surface | Provides consistent section spacing, title, helper text, and field stack |
| `cmpFieldShell` | Field wrapper | Provides label, hint, required marker, input slot, and error text |
| `cmpValidationSummary` | Blocked navigation summary | Shows actionable errors for visible fields only |
| `cmpReferenceComboBox` | Reference-data selector | Supports delegable filtering and stores value/label |
| `cmpFooterCommandBar` | Screen actions | Provides consistent Back, Save Draft, Continue, Review, and Submit actions |
| `cmpSaveStatus` | Save feedback | Shows draft/saving/saved/failed state without silent failures |

## Placeholder rules for Milestone 1

While Microsoft Lists cannot yet be created in the controlled Windows environment:

1. Build placeholder screens/components against local collections or static sample records only.
2. Use the real component names and layout contract from this document.
3. Use sample data shaped like `schemas/xlsform-to-list-mapping.csv` and `schemas/sharepoint-fields.csv`.
4. Do not hard-code final SharePoint list IDs, URLs, credentials, or connection names.
5. Keep formulas structured so local collections can be swapped for Microsoft Lists data sources later.
6. Mark all local data sources as placeholder in screen/component comments or documentation.
7. Do not implement destructive writes or production publish steps.

## Field layout rules

Each field row must include:

- visible label,
- optional hint/helper text,
- required marker only when the field is currently relevant,
- input control,
- inline validation message,
- consistent vertical spacing.

Do not use placeholder text as the only label.

## Validation UX rules

- Validate visible fields before Continue and Submit.
- Hidden/skipped fields must not block progress.
- Show inline field errors and a section-level validation summary.
- Error text must say how to fix the problem.
- Save failures must show a visible failed state and user notification.

## Navigation rules

- Use wizard/stepper navigation for the full survey.
- Use tabs only inside a section for peer panels.
- Avoid icon-only critical actions.
- The primary action should be visually consistent across screens.
- Users should always know current section, completion state, and next action.

## Accessibility rules

- Every input must have a visible label and accessible name.
- Interactive controls should have large touch targets for field devices.
- Preserve visible focus.
- Use high-contrast-compatible color choices.
- Do not communicate errors by color alone.
- Dynamic save/error/submit states must also be visible as text.

## Verification

Before Phase 3 implementation is considered ready:

1. Screens follow the app layout contract.
2. Components listed in this document exist or have explicit placeholders.
3. Placeholder data is clearly marked and replaceable.
4. No screen uses one-off styling for core layout.
5. Validation and progress patterns are visible in the placeholder prototype.
6. The implementation is checked with the `design-system-governance` and `power-platform-canvas-apps` skills.
