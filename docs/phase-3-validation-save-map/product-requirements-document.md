# Product Requirements Document: Phase 3 Validation and Save Map

## Context and evidence

TACATDP Phase 3 converts a long XLSForm-style survey into a guided Power Apps Canvas app backed by Microsoft Lists/SharePoint. The current ordered native-control branch imports successfully in Studio and contains 33 chronological screens with 393 field rows and 226 scaffold-required rows. The next slice must define screen-level validation and save behavior before formulas or live data connections are implemented.

Key evidence:

- `artifacts/powerapps/phase3-preview/summary.json`
- `app-src/Src/Screen_*.pa.yaml`
- `schemas/xlsform-to-list-mapping.csv`
- `schemas/sharepoint-lists-schema.json`
- `docs/design-system.md`
- `docs/phase-3-requirements.md`
- `docs/phase-3-delivery-plan.md`
- `docs/phase-3-maker-runbook.md`
- `docs/powerapps-import-recovery.md`

## Problem

The app has an importable native-control screen scaffold, but it does not yet have durable, screen-by-screen requirements for validation, validation-summary behavior, placeholder save orchestration, and later Microsoft Lists replacement. Implementing formulas without that map risks ad-hoc fixes, hidden-field validation bugs, incorrect list writes, repeated import failures, and UX drift.

## Users and actors

- Enumerator: enters TACATDP survey data and needs clear progress, validation, and save state.
- Power Apps maker: implements formulas, wiring, and later SharePoint connections in the authorized environment.
- QA reviewer: verifies required, relevance, constraint, navigation, save, and accessibility behavior screen by screen.
- Data engineer: validates that saved records match Microsoft Lists schema and reporting needs.
- Karakana agent: follows protocol artifacts, model routes, and handoff evidence before implementation.

## Goals and success measures

| Goal | Success measure |
| --- | --- |
| Make validation behavior explicit for every Phase 3 screen. | All 33 screens are listed with row counts, required counts, validation pattern, and save target. |
| Preserve ODK/XLSForm semantics. | Required, relevance, constraints, multi-select, and repeat/line-item rules are mapped to Power Apps behavior. |
| Keep UX consistent and usable. | One field per row, visible label, helper/error text, validation summary, wizard navigation, and touch-safe spacing remain required. |
| Keep import/open risk controlled. | The next slice works from the native-control import candidate and does not promote unverified generated component YAML. |
| Support offline environment constraints. | Placeholder collections are used until the authorized Windows/Power Apps environment and Microsoft Lists connections are available. |
| Preserve traceability. | Requirements, user stories, acceptance criteria, readiness, verification, and handoff are attached to Karakana trace `20260703-071158-1facb9`. |

## Non-goals

- Creating, modifying, or writing to production SharePoint/Microsoft Lists.
- Publishing or importing the app into a production Power Apps environment.
- Replacing the native-control import candidate with custom generated Canvas components.
- Implementing final Power Fx formulas in this artifact-only slice.
- Solving offline synchronization beyond documented draft/save state seams.

## Functional requirements

| ID | Requirement | Source / evidence | Priority |
| --- | --- | --- | --- |
| VSM-RQ-01 | Each Phase 3 screen must have a declared validation pattern. | `summary.json`, `Screen_*.pa.yaml` | P0 |
| VSM-RQ-02 | Continue must validate only visible/relevant fields. | `docs/phase-3-requirements.md` | P0 |
| VSM-RQ-03 | Inline error text must appear below invalid visible fields. | `docs/design-system.md` | P0 |
| VSM-RQ-04 | A section-level validation summary must list all blockers when navigation or submit is blocked. | `docs/design-system.md`, `docs/phase-3-maker-runbook.md` | P0 |
| VSM-RQ-05 | Save Draft must write placeholder records first and expose save-failed state on error. | `docs/milestone-1-placeholder-plan.md`, `docs/phase-3-delivery-plan.md` | P0 |
| VSM-RQ-06 | All saved rows must carry a stable `SubmissionKey`. | `docs/phase-3-requirements.md`, `schemas/sharepoint-lists-schema.json` | P0 |
| VSM-RQ-07 | Multi-select answers must save as child rows in `TACATDP_MultiSelectAnswers`. | `schemas/xlsform-to-list-mapping.csv` | P0 |
| VSM-RQ-08 | Production cost detail rows must save as child rows in `TACATDP_ProductionCostLines`. | `schemas/xlsform-to-list-mapping.csv` | P0 |
| VSM-RQ-09 | Scalar section fields must map to their target section lists using internal column names from the schema. | `schemas/xlsform-to-list-mapping.csv`, `schemas/sharepoint-lists-schema.json` | P0 |
| VSM-RQ-10 | Reference and cascading location choices must be delegation-safe and not fully loaded into app-start collections when large. | `docs/phase-3-requirements.md` | P1 |
| VSM-RQ-11 | ODK metadata fields must not be visible entry fields. | `summary.json`, current ordered source | P0 |
| VSM-RQ-12 | App source must remain packable/importable after implementation. | `docs/powerapps-import-recovery.md` | P0 |

## UX requirements

- Behavior: wizard-style section progression with Back, Continue, Save Draft, and final review/submit states.
- Look and feel: one field per row; visible label above input; helper/error text below input; consistent section spacing and command area.
- States: incomplete, valid, invalid, saving, saved, save-failed, submitted, hidden/skipped.
- Accessibility: labels must be visible; errors must not rely on color alone; focus order must follow top-to-bottom row order; touch targets should be at least 44 px high.
- Design-system fit: validation and save behavior must conform to `docs/design-system.md` and the `power-platform-canvas-apps` skill.

## Architecture and data requirements

- `SubmissionKey` is the parent key for all placeholder and future Microsoft Lists rows.
- Placeholder collections are the first implementation target:
  - `colPlaceholderSubmissions` -> `TACATDP_Submissions`
  - `colPlaceholderProfile` -> `TACATDP_Profile`
  - `colPlaceholderMultiSelectAnswers` -> `TACATDP_MultiSelectAnswers`
  - `colPlaceholderProductionCostLines` -> `TACATDP_ProductionCostLines`
  - section-specific placeholder collections -> section lists in `sharepoint-lists-schema.json`
- The save map must preserve normalized child-row storage for multi-select answers and production-cost lines.
- SharePoint required columns must not be used for fields that can be skipped by relevance logic; app-layer validation owns required behavior.
- Formula implementation should centralize repeated validation and save-state patterns where Power Apps Studio supports it.

## Screen-by-screen validation and save map

| Screen | Rows | Required | Primary save target | Validation and save notes |
| --- | ---: | ---: | --- | --- |
| `Screen_01_demographics` | 21 | 14 | `TACATDP_Profile` | Validate demographic required fields, cascading location choices, phone format, loan minimum, and placeholder profile save. |
| `Screen_02_agricultural_production` | 8 | 8 | `TACATDP_MultiSelectAnswers` | Normalize crop/category/adaptation/technology selections as child rows. |
| `Screen_03_resource_efficiency` | 14 | 12 | `TACATDP_ResourceEfficiency` | Validate visible irrigation, water, and energy fields before Continue. |
| `Screen_04_social_inclusion` | 9 | 5 | `TACATDP_SocialInclusion` | Validate group/gender/social inclusion fields only when relevant. |
| `Screen_05_household_quantification` | 7 | 4 | `TACATDP_Beneficiaries` | Save household beneficiary counts with numeric validation. |
| `Screen_06_training_gap` | 10 | 7 | `TACATDP_Beneficiaries` | Save training/gender action beneficiary counts with numeric validation. |
| `Screen_07_beneficiaries_overview` | 2 | 1 | Navigation/state only | Explain beneficiary stages and block only true required visible inputs. |
| `Screen_08_farm_preparation` | 10 | 6 | `TACATDP_Beneficiaries` | Save farm preparation beneficiary stage row. |
| `Screen_09_farm_operations` | 10 | 6 | `TACATDP_Beneficiaries` | Save farm operations beneficiary stage row. |
| `Screen_10_input_supply` | 10 | 6 | `TACATDP_Beneficiaries` | Save input supply beneficiary stage row. |
| `Screen_11_weeding` | 10 | 6 | `TACATDP_Beneficiaries` | Save weeding/field management beneficiary stage row. |
| `Screen_12_pest_control` | 10 | 6 | `TACATDP_Beneficiaries` | Save pre-harvest/pest control beneficiary stage row. |
| `Screen_13_harvesting` | 10 | 6 | `TACATDP_Beneficiaries` | Save harvesting beneficiary stage row. |
| `Screen_14_postharvest` | 10 | 6 | `TACATDP_Beneficiaries` | Save post-harvest handling beneficiary stage row. |
| `Screen_15_storage` | 10 | 6 | `TACATDP_Beneficiaries` | Save storage/warehousing beneficiary stage row. |
| `Screen_16_transport` | 10 | 6 | `TACATDP_Beneficiaries` | Save crop transport beneficiary stage row. |
| `Screen_17_processing` | 10 | 6 | `TACATDP_Beneficiaries` | Save value addition/processing beneficiary stage row. |
| `Screen_18_aquaculture` | 10 | 6 | `TACATDP_Beneficiaries` | Save aquaculture beneficiary stage row. |
| `Screen_19_fisheries_landing` | 10 | 6 | `TACATDP_Beneficiaries` | Save fisheries landing beneficiary stage row. |
| `Screen_20_aquaponics` | 10 | 6 | `TACATDP_Beneficiaries` | Save aquaponics beneficiary stage row. |
| `Screen_21_marketing` | 10 | 6 | `TACATDP_Beneficiaries` | Save marketing/trading beneficiary stage row. |
| `Screen_22_consumption` | 9 | 6 | `TACATDP_Beneficiaries` | Save consumption/user beneficiary stage row. |
| `Screen_23_trainers_trainees` | 10 | 6 | `TACATDP_Beneficiaries` | Save trainers and trainees beneficiary stage row. |
| `Screen_24_collective_engagement` | 10 | 6 | `TACATDP_Beneficiaries` | Save collective engagement beneficiary stage row. |
| `Screen_25_other_value_chain` | 10 | 6 | `TACATDP_Beneficiaries` | Save other value-chain beneficiary stage row. |
| `Screen_26_beneficiary_summary` | 24 | 0 | Review/state only | Show computed beneficiary totals and links to incomplete stages; no direct section save. |
| `Screen_27_safeguards_climate` | 16 | 15 | `TACATDP_SafeguardsClimate` | Validate safeguards and climate risk answers before Continue. |
| `Screen_28_insurance_guarantee` | 7 | 4 | `TACATDP_InsuranceGuarantee` | Validate insurance/guarantee linkage fields. |
| `Screen_29_ghg_quantification` | 25 | 12 | `TACATDP_GHGWaterYield` | Validate GHG quantification fields and numeric constraints. |
| `Screen_30_water_efficiency` | 12 | 8 | `TACATDP_GHGWaterYield` | Validate water efficiency fields and numeric constraints. |
| `Screen_31_yield_income` | 12 | 3 | `TACATDP_ProductionIncome` | Validate yield and income impact fields. |
| `Screen_32_production_cost_income` | 41 | 20 | `TACATDP_ProductionIncome` | Validate production income summary fields and navigation to detail lines. |
| `Screen_33_production_cost_detail` | 6 | 5 | `TACATDP_ProductionCostLines` | Validate stage, item, unit, quantity, and cost; save one normalized line row. |

## Safety, privacy, and operational constraints

- No credentials, tokens, connection strings, tenant secrets, or production URLs may be committed.
- Production SharePoint writes, permission changes, app import/publish, and destructive list changes require explicit approval.
- Use the authorized Windows/Power Apps environment for Studio import/open checks and App Checker.
- Use placeholder data until the real Microsoft Lists connection is approved and available.

## Acceptance criteria

See `acceptance-criteria.md`.

## Definition of Ready

See `artifact-readiness.md`.

## Definition of Done

See `definition-of-done.md`.

## Traceability

See `requirements-traceability.md`.

## Open questions

- Should `copilot/order-screens-demographics` be squash-merged into TACATDP `main` before the formula implementation slice starts?
- What is the approved target SharePoint site and list naming convention for the controlled environment?
- What target device sizes should be treated as blocking for screen-level UX verification?
- What offline/low-connectivity behavior is expected beyond local draft placeholder state?

