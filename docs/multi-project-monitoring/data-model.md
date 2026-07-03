# Multi-Project Monitoring Data Model

## Recommended Dataverse-first schema groups

### 1. Project and governance

| Table | Key columns | Notes |
| --- | --- | --- |
| `mp_Project` | `ProjectCode`, `Name`, `Status`, `OwnerTeam` | Top-level monitoring project/program. |
| `mp_ProjectRoleAssignment` | `Project`, `UserOrTeam`, `Role` | Project-scoped access model. |
| `mp_ProjectSetting` | `Project`, `SettingKey`, `Value` | Non-secret project configuration. |

### 2. Instrument metadata

| Table | Key columns | Notes |
| --- | --- | --- |
| `mp_Instrument` | `Project`, `InstrumentCode`, `Name`, `Purpose` | Form/survey concept. |
| `mp_InstrumentVersion` | `Instrument`, `VersionCode`, `LifecycleStatus`, `PublishedAt` | Draft/published/retired version. |
| `mp_EventDefinition` | `Project`, `EventCode`, `Name`, `Repeatable` | Visit/reporting period/follow-up occasion. |
| `mp_InstrumentEventBinding` | `EventDefinition`, `InstrumentVersion`, `Required` | Which form applies to which event. |
| `mp_GroupDefinition` | `InstrumentVersion`, `ParentGroup`, `GroupCode`, `Name`, `Repeatable`, `DisplayOrder` | Section or repeating group. |
| `mp_FieldDefinition` | `GroupDefinition`, `FieldCode`, `DataType`, `RequiredMode`, `DisplayOrder` | Question/variable metadata. |
| `mp_FieldRule` | `FieldDefinition`, `RuleType`, `Expression`, `Message` | Required, relevance, constraint, calculate, default. |

### 3. Controlled vocabularies

| Table | Key columns | Notes |
| --- | --- | --- |
| `mp_VocabularyScheme` | `SchemeCode`, `Name`, `Authority`, `Version`, `Status` | Example: TACATDP crop, ROR affiliation, region, OECD subject. |
| `mp_VocabularyTerm` | `Scheme`, `TermCode`, `PreferredLabel`, `Status`, `SortOrder` | Stable coded value. |
| `mp_VocabularyTermLabel` | `Term`, `LanguageCode`, `Label`, `LabelType` | Preferred/alternate labels; supports i18n and aliases. |
| `mp_VocabularyTermRelation` | `SourceTerm`, `RelationType`, `TargetTerm` | Parent/child, exactMatch, broader, narrower. |
| `mp_ProjectVocabularyBinding` | `Project`, `Scheme`, `FilterRule`, `Status` | Project-specific allowed subset. |
| `mp_FieldVocabularyBinding` | `FieldDefinition`, `Scheme`, `SelectionMode`, `RequiredTermFilter` | Binds select_one/select_multiple/reference fields. |
| `mp_ExternalAuthorityIdentifier` | `Term`, `Authority`, `Identifier`, `Uri` | ROR, DataCite, custom registry IDs. |

### 4. Runtime entities and submissions

| Table | Key columns | Notes |
| --- | --- | --- |
| `mp_TrackedEntity` | `Project`, `EntityType`, `EntityKey`, `DisplayName`, `Status` | Farmer, customer, school, facility, household, site. |
| `mp_EntityIdentifier` | `TrackedEntity`, `IdentifierType`, `IdentifierValue` | Customer ID, facility code, national ID hash, etc. |
| `mp_Encounter` | `Project`, `TrackedEntity`, `EventDefinition`, `EncounterDate`, `Status` | Visit/follow-up/reporting period occurrence. |
| `mp_Submission` | `Project`, `InstrumentVersion`, `Encounter`, `SubmissionKey`, `Status`, timestamps | One filled form instance. |
| `mp_GroupInstance` | `Submission`, `GroupDefinition`, `ParentGroupInstance`, `RepeatIndex`, `InstanceKey` | One section/repeat occurrence. |
| `mp_AnswerValue` | `Submission`, `GroupInstance`, `FieldDefinition`, typed value columns | Scalar answer source of truth. |
| `mp_MultiSelectAnswer` | `Submission`, `GroupInstance`, `FieldDefinition`, `VocabularyTerm` | One row per selected option. |
| `mp_Attachment` | `Submission`, `FieldDefinition`, `File`, `MediaType`, checksum | Photos/files/media. |
| `mp_SubmissionReview` | `Submission`, `ReviewState`, `Reviewer`, `Comment` | Review/approval workflow. |
| `mp_AuditEvent` | `Project`, `Entity`, `Action`, `Actor`, timestamp | Data lineage and corrections. |

## AnswerValue typed columns

`mp_AnswerValue` should avoid storing everything as text. Use typed nullable columns and exactly one active value per row:

- `TextValue`
- `NumberValue`
- `DecimalValue`
- `CurrencyValue`
- `DateValue`
- `DateTimeValue`
- `BooleanValue`
- `GeopointLatitude`
- `GeopointLongitude`
- `GeopointAltitude`
- `GeopointAccuracy`
- `JsonValue` for rare complex data

Store original/raw values when useful for audit or import fidelity.

## Repeat groups

Repeats are not columns. A repeat is:

1. `GroupDefinition.Repeatable = true`.
2. One or more `GroupInstance` rows for a submission.
3. `RepeatIndex` and `InstanceKey` identify occurrence order.
4. Nested repeats use `ParentGroupInstance`.
5. Answers inside a repeat point to that repeat's `GroupInstance`.

## Multiple select

Multiple select is not delimited text in the source model:

1. The field has `FieldVocabularyBinding.SelectionMode = Multiple`.
2. Each selected term creates one `mp_MultiSelectAnswer`.
3. Export profiles can generate ODK/REDCap-style wide columns if needed.

## Controlled variables / controlled vocabularies

Controlled variables should be implemented as reusable vocabulary schemes and terms:

- stable codes;
- preferred labels;
- multilingual labels;
- aliases/synonyms;
- hierarchy and mappings;
- external authority identifiers;
- term lifecycle status;
- project-specific subsets;
- field-specific bindings;
- import/export fixtures.

This supports TACATDP choices now and future project vocabularies later.

## TACATDP mapping stance

TACATDP becomes:

- `mp_Project(ProjectCode = "tacatdp")`
- one or more `mp_Instrument` records for the Phase 3 survey;
- 33 current screens mapped to `GroupDefinition` or UI screen definitions;
- 292 XLSForm fields mapped to `FieldDefinition`;
- current select lists mapped to `VocabularyScheme` and `VocabularyTerm`;
- current `TACATDP_MultiSelectAnswers` and `TACATDP_ProductionCostLines` mapped to normalized runtime tables.

The old section-list/table names remain useful as export profiles or generated views but should not be the long-term source of truth.

