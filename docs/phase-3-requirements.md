# Phase 3 App Architecture Requirements

## Objective

Design the TACATDP Power Apps canvas app architecture so the Dataverse-first backend can support an ODK-like guided data-entry experience with skip logic, validation, draft saving, reference data, and clear section progression.

Dataverse is now the primary development backend. Microsoft Lists/SharePoint artifacts remain available as a fallback and as evidence for the existing hybrid decomposition.

## Functional requirements

### App structure

1. The app must replace the current one-screen starter form with a guided multi-section survey flow.
2. The app must align screens/sections with the XLSForm section structure and generated hybrid schema.
3. The app must create one `SubmissionKey` per survey submission and use it across parent, section, child, and reference-dependent records.
4. The app must support draft, saved, submitted, and save-failed states.
5. The app must include a final review/submit step before marking a submission complete.

### Section architecture

1. Each major section must have a screen or reusable section component.
2. Each section must show only relevant fields based on translated XLSForm `relevance` logic.
3. Each section must validate visible required fields and constraints before Continue.
4. Each section must save to its target Dataverse section table or child table according to the Dataverse schema plan derived from `schemas/xlsform-to-list-mapping.csv`.
5. Sections with many repeated fields, especially beneficiary and production-cost sections, must use reusable subcomponents.

### Reference data

1. Location selection must use delegable cascading filters: region, district, ward, village.
2. Branch selection must filter by zone.
3. Crop/technology-dependent choice filters must preserve the XLSForm filter behavior.
4. Large reference lists must not be fully loaded into collections at app start.
5. `select_one` controls must store both value and label where defined by the schema.

### Multi-select and line-item data

1. `select_multiple` questions must save selected values as rows in the Dataverse `MultiSelectAnswer` table.
2. Production cost stage data must save as rows in the Dataverse `ProductionCostLine` table.
3. Re-opening an existing draft must reconstruct multi-select and line-item control state from child lists.

### Validation

1. Required validation must apply only when a field is visible/relevant.
2. XLSForm constraints must be translated to Power Fx validation formulas.
3. Inline validation messages must appear near fields.
4. A section-level validation summary must appear when Continue or Submit is blocked.
5. Save failures must be visible and must not appear successful.

### UX and design system

1. The app must use a consistent app shell with header, progress, content surface, and command bar/footer actions.
2. The visual design should use Power Apps modern controls and Fluent UI where feasible.
3. Material Design principles should guide form labels, helper text, errors, progress, navigation clarity, and accessibility.
4. Navigation must be clear enough for field enumerators to know where they are, what is incomplete, and how to continue.
5. The app must be usable on the agreed target device sizes.
6. The app must follow the component and layout contract in `docs/design-system.md`.

### Milestone 1 placeholders

1. Milestone 1 must use placeholder/local sample data while Dataverse schema generation and dev environment table creation are prepared.
2. Placeholder data must be clearly named and documented as temporary.
3. Placeholder screens must use the final design-system shell and component structure.
4. Placeholder formulas must be structured so real Microsoft Lists data sources can replace them later.
5. Milestone 1 must not require live SharePoint writes or app publication.

## Non-functional requirements

1. Power Fx formulas for shared logic should be centralized through named formulas, components, or clearly named variables where feasible.
2. Large-list filtering must be delegable or explicitly documented as safe due to small bounded data.
3. App source changes must remain packable/importable.
4. The app must be testable through Power Apps Studio App Checker, Monitor, and manual scenario scripts.
5. Scripts and app source must not store secrets or credentials.

## Acceptance criteria

1. Phase 3 architecture identifies screens, components, data sources, and save flow.
2. Every target Dataverse table derived from `schemas/xlsform-to-list-mapping.csv` has an app save/read strategy.
3. Large reference choices have delegable ComboBox/filter patterns.
4. Required, relevance, and constraint logic has a Power Fx translation strategy.
5. The UI design system defines shell, section, field, validation, progress, and command patterns.
6. The delivery plan defines implementation order and verification steps.
7. Milestone 1 placeholder screens can be reviewed without live Dataverse writes.

## Dependencies

- Dataverse schema artifacts must be generated and reviewed.
- Target Power Platform dev environment, solution, publisher prefix, and permissions must be confirmed.
- Target device priority must be confirmed.
- Offline/draft expectations must be confirmed.
