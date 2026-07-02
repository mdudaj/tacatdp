# Phase 2: Microsoft Lists Schema Design

## Purpose

Design a Microsoft Lists-backed data model for the TACATDP Power Apps canvas app that supports the extracted XLSForm requirements without forcing all 292 input fields into one fragile list.

## Source inventory

Current generated inventory:

- `docs/xlsform-field-inventory.csv`
- `docs/xlsform-logic-map.csv`
- `docs/xlsform-choice-lists.csv`
- `docs/xlsform-summary.md`

Input field profile:

| Input type | Count |
| --- | ---: |
| integer | 122 |
| decimal | 54 |
| select_one | 75 |
| select_multiple | 20 |
| text | 19 |
| geopoint | 1 |
| date | 1 |
| **Total** | **292** |

Logic and choice profile:

- 288 required input rules
- 48 input relevance rules
- 16 input constraint rules
- 9 input choice filters
- 47 input-used choice lists
- 71,487 source choice rows
- Largest choice lists: `village` 66,297 rows, `ward` 3,966 rows, `branch` 239 rows, `district` 184 rows

## Microsoft Lists and Power Apps constraints

Research findings from Microsoft documentation:

1. Microsoft Lists are SharePoint lists. Power Apps connects to them through the SharePoint connector.
2. Power Apps delegation is critical. If a formula is not delegable, Power Apps retrieves only the first 500 records by default, configurable to 2,000, then filters locally. That is unsafe for lists such as `village` with 66,297 rows.
3. SharePoint connector data types map to Power Apps as basic types (`Text`, `Number`, `Boolean`, `DateTime`) or `Complex` types (`Choice`, `Lookup`, `Person`, managed metadata, and similar).
4. SharePoint delegable operations are better for simple `Text`, `Number`, `Boolean`, and `DateTime` columns. Complex columns have more limitations, especially for sorting and subfield search.
5. SharePoint connector supports large lists, but app formulas must use delegable filters and indexed columns for predictable behavior.
6. A single wide list is a poor fit for this workbook because it has 292 input fields, 176 numeric fields, repeated cost-stage structures, and large/cascading reference choices.

Key references:

- Microsoft Power Apps delegation overview: `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview`
- Microsoft Power Apps SharePoint connector data type/delegation reference: `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online`
- Microsoft SharePoint connector reference: `https://learn.microsoft.com/en-us/connectors/sharepointonline/`
- Microsoft SharePoint limits: `https://learn.microsoft.com/en-us/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits`

## Schema options

### Option A: One wide submissions list

Store one submission as one Microsoft Lists item with one column per XLSForm input field.

**Pros**

- Simplest conceptual model.
- Power Apps generated form can bind directly to one list.
- Exports one row per submission.

**Cons**

- Not suitable for 292 input fields and 176 numeric fields.
- Repeated value-chain cost stage fields become many duplicated columns.
- `select_multiple` fields are awkward for reporting if stored as multi-choice or delimited text.
- Complex columns and many choices can create delegation and performance issues.
- Large reference choices cannot be safely implemented as static choices.

**Decision:** Not recommended.

### Option B: Section-split wide lists

Store one parent submission item, then one item per major section in separate section lists. Each section list stores only scalar fields for that section and links back by `SubmissionKey`.

**Pros**

- Keeps each list smaller and closer to the Power Apps screen/section flow.
- Avoids one-list column pressure.
- Easier to save a section at a time.
- Easier to secure/review section data independently.

**Cons**

- Requires multiple `Patch`/save operations.
- Requires save-state handling across lists.
- Reporting requires joining by `SubmissionKey`.

**Decision:** Recommended for scalar section data.

### Option C: Fully normalized answer list

Store each answer as one row in a generic answers list: `SubmissionKey`, `QuestionName`, `AnswerValue`, `AnswerNumber`, `AnswerDate`, and metadata.

**Pros**

- Very flexible for changing survey versions.
- Avoids wide-list limits.
- Easy to preserve XLSForm names exactly.

**Cons**

- Harder to build simple form screens.
- Harder to enforce typed column validation at the Microsoft Lists level.
- Produces many rows per submission.
- Reporting and Power BI models need pivoting or semantic modeling.

**Decision:** Useful for dynamic survey engines, but not recommended as the primary scalar storage model for this app.

### Option D: Hybrid model

Use a parent submission list, section lists for scalar input fields, child answer lists for repeated/multi-select data, and reference lists for choices.

**Pros**

- Best fit for the current workbook.
- Keeps scalar data typed and section-oriented.
- Handles `select_multiple` cleanly.
- Handles 71,487 reference choice rows without hard-coding choices in the app.
- Keeps large/cascading filters delegable by using simple indexed text/number keys.

**Cons**

- More lists to create and maintain.
- Requires explicit save orchestration and error handling.
- Reporting requires a model that understands parent/child relationships.

**Decision:** Recommended.

### Option E: Dataverse instead of Microsoft Lists

Dataverse would be stronger for relationships, large reference data, typed validation, and transactional saves.

**Pros**

- Better relational modeling and delegation.
- Better choice/reference tables.
- Better app lifecycle support.

**Cons**

- May require licensing and environment setup beyond the stated Microsoft Lists requirement.
- Not aligned with the current integration target.

**Decision:** Keep as a fallback if Microsoft Lists constraints become blocking.

## Recommended list architecture

### 1. `TACATDP_Submissions`

One row per survey submission.

Recommended columns:

| Column | Type | Purpose |
| --- | --- | --- |
| `Title` | Single line text | Human-readable submission title |
| `SubmissionKey` | Single line text, indexed, unique | App-generated GUID used across all related lists |
| `FormId` | Single line text | XLSForm form ID |
| `FormVersion` | Single line text | XLSForm version |
| `SubmissionStatus` | Single line text or choice | Draft, Submitted, SyncFailed, Reviewed |
| `EnumeratorEmail` | Single line text | `User().Email` value |
| `EnumeratorName` | Single line text | `User().FullName` value |
| `StartedAt` | Date and time | App start timestamp replacing ODK `starttime` |
| `SubmittedAt` | Date and time | Final submit timestamp replacing ODK `endtime` |
| `LastSavedAt` | Date and time | Draft/save timestamp |
| `Customer_ID` | Number or text | Key respondent identifier |
| `Customer_Name` | Single line text | Respondent name |
| `RegionValue` | Single line text or number | Denormalized location key for filtering/export |
| `DistrictValue` | Single line text or number | Denormalized location key |
| `WardValue` | Single line text or number | Denormalized location key |
| `VillageValue` | Single line text or number | Denormalized location key |

Use text key columns for important filters instead of relying on Lookup subfields in app formulas.

### 2. Section scalar lists

Create one list per major form area. Each item links to `TACATDP_Submissions` with `SubmissionKey`.

Recommended starting lists:

| List | Content |
| --- | --- |
| `TACATDP_Profile` | Customer, demographics, loan, location, georeference, land ownership |
| `TACATDP_Agriculture` | Crop, technology, climate risk, adaptation, yield |
| `TACATDP_ResourceEfficiency` | Irrigation, water, energy, adopted energy |
| `TACATDP_SocialInclusion` | Farmer group, household, gender, training |
| `TACATDP_Beneficiaries` | Value-chain beneficiary counts and summary fields |
| `TACATDP_SafeguardsClimate` | Environmental/social safeguards and climate risk assessment |
| `TACATDP_InsuranceGuarantee` | Insurance, guarantee, exposure, grievance |
| `TACATDP_GHGWaterYield` | GHG, water efficiency, yield and income impact |
| `TACATDP_ProductionIncome` | Cost/income summary fields that are not repeated cost lines |

Each section list should include:

- `Title`
- `SubmissionKey`, indexed
- `FormVersion`
- `SectionStatus`
- Scalar input columns for that section only
- `LastSavedAt`

### 3. `TACATDP_MultiSelectAnswers`

Store one row per selected option for `select_multiple` questions.

Recommended columns:

| Column | Type | Purpose |
| --- | --- | --- |
| `Title` | Single line text | `${SubmissionKey}-${QuestionName}-${ChoiceValue}` |
| `SubmissionKey` | Single line text, indexed | Parent submission key |
| `SectionKey` | Single line text, indexed | Section/screen key |
| `QuestionName` | Single line text, indexed | XLSForm input name |
| `ChoiceListName` | Single line text | XLSForm choice list |
| `ChoiceValue` | Single line text, indexed | Stored XLSForm choice value |
| `ChoiceLabelEn` | Single line text | English label snapshot |
| `ChoiceLabelSw` | Single line text | Swahili label snapshot |
| `SortOrder` | Number | Choice order |

Do not store multi-select values as comma-separated text if the data will be analyzed by question/choice.

### 4. `TACATDP_ProductionCostLines`

Normalize the repeated value-chain cost stage fields instead of storing `vc1_*` through `vc18_*` as many separate columns.

Recommended columns:

| Column | Type | Purpose |
| --- | --- | --- |
| `Title` | Single line text | `${SubmissionKey}-${StageCode}` |
| `SubmissionKey` | Single line text, indexed | Parent submission key |
| `StageCode` | Single line text, indexed | `vc1` through `vc18` |
| `StageLabel` | Single line text | Display label |
| `CostItemValue` | Single line text | Selected cost item value |
| `CostItemLabel` | Single line text | Selected cost item label |
| `UnitValue` | Single line text | Unit of measure value |
| `UnitLabel` | Single line text | Unit label |
| `Quantity` | Number | Quantity |
| `UnitCostTZS` | Currency or Number | Unit cost |
| `LineTotalTZS` | Currency or Number | Quantity * unit cost |

This removes 72 repeated cost-stage columns from the scalar schema and makes reporting by value-chain stage easier.

### 5. Reference data lists

Use reference lists rather than static choices for large or filtered options.

Recommended reference lists:

| List | Content | Notes |
| --- | --- | --- |
| `TACATDP_RefRegions` | Region values/labels | Small list |
| `TACATDP_RefDistricts` | District values/labels with `RegionValue` | Index `RegionValue` |
| `TACATDP_RefWards` | Ward values/labels with `RegionValue`, `DistrictValue` | Index parent keys |
| `TACATDP_RefVillages` | Village values/labels with `RegionValue`, `DistrictValue`, `WardValue` | Required for 66,297 villages |
| `TACATDP_RefBranches` | CRDB branches with `ZoneValue` | Index `ZoneValue` |
| `TACATDP_RefChoices` | Other choice lists | Use `ChoiceListName`, `ChoiceValue`, labels, and optional filter keys |

For app performance, filter reference lists by simple indexed columns:

```powerfx
Filter(TACATDP_RefVillages, RegionValue = varRegion && DistrictValue = varDistrict && WardValue = varWard)
```

Avoid formulas that filter large lists using nondelegable transformations, `Search` over complex subfields, or unindexed parent columns.

## Column type conventions

| XLSForm type | Microsoft Lists type | Power Apps control | Notes |
| --- | --- | --- | --- |
| `text` | Single line text | Text input | Use Multiple lines only for long narrative fields |
| `integer` | Number, decimal places 0 | Text input with numeric validation | Use Number rather than text unless leading zeros matter |
| `decimal` | Number or Currency | Text input with numeric validation | Use Currency for TZS amounts if currency formatting/reporting is needed |
| `date` | Date and time, date only | Date picker | Preserve date-only behavior |
| `geopoint` | Text plus optional latitude/longitude number columns | Location capture controls | Store raw geopoint text and split latitude/longitude for reporting |
| `select_one` small static list | Choice or text value + label | Combo box/dropdown | Prefer text value/label when filtering/reporting matters |
| `select_one` large/filtered list | Text key + label from reference list | Combo box with reference list | Do not use static Choice for large lists |
| `select_multiple` | Child rows in `TACATDP_MultiSelectAnswers` | Combo box multi-select | Avoid comma-separated storage for analytics |

## Naming conventions

Use stable, readable names and preserve the XLSForm field name in the mapping.

Recommended list naming:

- Prefix app-owned lists with `TACATDP_`.
- Use plural/reference names for lookup data, for example `TACATDP_RefVillages`.
- Use singular section nouns where each item is one submission-section record, for example `TACATDP_Profile`.

Recommended column naming:

- Use ASCII internal names.
- Use PascalCase for system columns: `SubmissionKey`, `FormVersion`, `LastSavedAt`.
- Preserve XLSForm names in `docs/xlsform-field-inventory.csv`.
- For stored survey answer columns, prefer readable PascalCase display names but document the XLSForm source name in the mapping.
- For choice fields, store both value and label when reporting/export must preserve XLSForm codes and human-readable text.

## Validation and skip-logic conventions

1. Required fields should be enforced in Power Apps only when their data card/section is relevant.
2. Microsoft Lists required columns should be used carefully. If a field can be skipped by relevance logic, do not make the SharePoint column required.
3. Constraints should be implemented in Power Fx because many constraints are cross-field or XLSForm-specific.
4. Use section-level validation before writing each section list.
5. Use save-result tracking so multi-list saves cannot fail silently.

## Recommended decision

Use the hybrid design:

1. `TACATDP_Submissions` as the parent list.
2. Section scalar lists for typed one-to-one section data.
3. `TACATDP_MultiSelectAnswers` for all `select_multiple` answers.
4. `TACATDP_ProductionCostLines` for repeated value-chain cost stages.
5. Dedicated reference lists for location and branches.
6. A generic `TACATDP_RefChoices` list for smaller non-location choices.

This design follows Power Apps delegation guidance, avoids a brittle single wide list, supports the large cascading choice lists, and keeps reporting viable.

## Phase 2 next steps

1. Assign each input field in `docs/xlsform-field-inventory.csv` to a target list and target column.
2. Confirm whether TZS amount fields should be Number or Currency.
3. Confirm whether `select_multiple` answers must be analytics-ready; if yes, use `TACATDP_MultiSelectAnswers`.
4. Confirm whether location values should store numeric XLSForm codes, labels, or both.
5. Confirm target SharePoint site and list names.
6. Create a schema mapping CSV from the field inventory.
