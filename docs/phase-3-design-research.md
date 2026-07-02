# Phase 3 Design Research

## Platform design direction

Power Apps canvas apps run inside the Microsoft 365 ecosystem, so the primary visual language should be Power Apps modern controls and Fluent UI conventions. Material Design should inform structure and usability, not override the Microsoft host look-and-feel.

Recommended stance:

- **Use Fluent/modern controls for visual consistency with Microsoft 365.**
- **Use Material Design principles for form clarity, validation, progress, navigation, touch targets, and accessibility.**

## Research findings

### Power Apps modern controls and Fluent UI

Microsoft's modern controls use Fluent UI and are intended to improve consistency, accessibility, and theming in canvas apps. For TACATDP this supports:

- consistent controls across survey sections,
- built-in accessible states where controls support them,
- a Microsoft 365-native look,
- less custom styling in exported YAML.

Important patterns:

- Use modern controls when they support the required behavior.
- Use containers for responsive layout.
- Use command bars or consistent footer actions for primary/secondary actions.
- Use tabs only for peer content, not as the main survey progression pattern.
- Test on target device sizes in Power Apps Studio.

### Material Design form principles

Material Design 3 guidance reinforces patterns useful for long survey workflows:

- keep labels visible instead of using placeholder-only fields,
- put helper and error text near the field,
- use clear red/error states with actionable messages,
- group related fields into sections,
- use determinate progress when progress is measurable,
- keep touch targets large enough for field use,
- preserve focus visibility and keyboard/screen-reader reachability.

### Power Apps performance and large forms

The current TACATDP form has 292 maintained inputs and large reference lists. The app should avoid one giant screen and avoid loading all reference data into memory.

Important patterns:

- Split the app into section screens.
- Load reference data on demand.
- Use delegable filters for large reference lists.
- Avoid nondelegable `Search` or transformations against `TACATDP_RefVillages`.
- Use Power Apps Monitor and App Checker during implementation.
- Use named formulas or reusable formulas for shared validation where possible.
- Use components for repeated UI/logic patterns, but avoid heavy data access inside components.

## TACATDP design system proposal

The durable design-system contract is now captured in `docs/design-system.md`. Phase 3 implementation should treat that file as the source of truth for shell, component, validation, navigation, and accessibility rules.

### App shell

- Header: app title, current submission status, save state, optional user identity.
- Progress: section stepper/list with completion state.
- Main content: one active section at a time.
- Footer command bar: Back, Save draft, Continue, Submit/Review depending on step.
- Error summary: appears after failed navigation/save and links or points to fields.

### Section surface

Each section should use a consistent card/surface:

- section title,
- short description/helper text,
- completion state,
- visible fields only,
- inline validation messages,
- section-level required/invalid count.

### Field pattern

Each field should have:

- visible label,
- optional helper/hint text,
- required marker when relevant,
- input control,
- inline validation message,
- consistent spacing from the next field.

### Navigation pattern

Use wizard/stepper navigation for the overall survey because the XLSForm is sequential and large. Use tabs only inside complex sections where peer panels share one task.

### Validation pattern

- Validate on section continue and on final submit.
- Use inline messages for field errors.
- Use a section summary for blocked navigation.
- Do not block on hidden/skipped fields.
- Do not rely on SharePoint required columns for skip-eligible fields.

### Accessibility pattern

- Ensure every control has an accessible label.
- Preserve visible focus.
- Use high-contrast-compatible colors.
- Keep touch targets large enough for mobile/tablet use.
- Avoid icon-only critical actions.
- Announce save/submit/error states with visible Notify or status text.

## Open design decisions

1. Target device priority: desktop, tablet, phone, or all three.
2. Whether offline/draft work is required before SharePoint save.
3. Whether to use modern controls exclusively or mix classic controls where modern controls lack needed behavior.
4. Whether bilingual labels should be switchable English/Swahili in-app.
5. Whether review/submit should be a final screen or a modal/panel.

## Milestone 1 placeholder design

Until Microsoft Lists can be created in the controlled Windows environment, Milestone 1 should build placeholder screens/components using local sample collections. Placeholder work must still follow `docs/design-system.md` so the UX and component layout can be reviewed before live data sources exist.
