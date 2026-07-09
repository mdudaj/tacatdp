# TACATDP Dataverse MVP Schema Definition

Status: review-ready, no environment write.

This is the full July 7 MVP schema contract. `mvp-tables.json` keeps the table inventory, `mvp-columns.csv` keeps the script-friendly column list, and `mvp-schema-definition.json` is the machine-readable definition for table, column, choice, and relationship review.

## Delivery Scope

- Target: one assigned published form rendered dynamically in Canvas from Dataverse metadata.
- Storage: generic submission and answer tables with one file/photo attachment table.
- Identity: Dataverse/Entra users through `systemuser` lookups where available, plus email fallback fields.
- Writes: none from these artifacts; live creation requires a separate approved Dataverse Web API deployment command.
- Solution placement: metadata create calls must include `MSCRM.SolutionUniqueName=$POWER_PLATFORM_SOLUTION_UNIQUE_NAME`.

## Dataverse Type Mapping

| Artifact type | Dataverse metadata type | MVP usage |
| --- | --- | --- |
| `Text` | `StringAttributeMetadata` | short labels, codes, email snapshots |
| `MultilineText` | `MemoAttributeMetadata` | help text, expressions, JSON snapshots |
| `WholeNumber` | `IntegerAttributeMetadata` | display order and integer answers |
| `Decimal` | `DecimalAttributeMetadata` | decimal answers |
| `Date` | `DateTimeAttributeMetadata` with date-only behavior | date answers |
| `DateTime` | `DateTimeAttributeMetadata` | publish/start/submit timestamps |
| `Boolean` | `BooleanAttributeMetadata` | required flags and boolean answers |
| `Choice` | `PicklistAttributeMetadata` | fixed lifecycle/status/type values |
| `File` | `FileAttributeMetadata` | photo/document attachment binary |
| `Lookup:<table>` | `LookupAttributeMetadata` plus `OneToManyRelationshipMetadata` | table relationships |

## Tables

### Forms

Purpose: Form/instrument container

Primary name column: `Name`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `FormCode` | `Text` | Yes | `StringAttributeMetadata` | Stable form code |
| `Name` | `Text` | Yes | `StringAttributeMetadata` | Display name |
| `Status` | `Choice` | Yes | `PicklistAttributeMetadata` | Draft/Active/Retired Values: `Draft`, `Active`, `Retired`. |

### FormVersions

Purpose: Published version metadata and lifecycle status

Primary name column: `VersionCode`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `Form` | `Lookup:Forms` | Yes | `LookupAttributeMetadata` | Parent form Lookup to `Forms`. |
| `VersionCode` | `Text` | Yes | `StringAttributeMetadata` | Stable version code |
| `LifecycleStatus` | `Choice` | Yes | `PicklistAttributeMetadata` | Draft/Published/Retired Values: `Draft`, `Published`, `Retired`. |
| `PublishedAt` | `DateTime` | No | `DateTimeAttributeMetadata(UserLocal)` | Publish timestamp |

### Sections

Purpose: Ordered form sections/pages

Primary name column: `Name`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `FormVersion` | `Lookup:FormVersions` | Yes | `LookupAttributeMetadata` | Parent form version Lookup to `FormVersions`. |
| `SectionCode` | `Text` | Yes | `StringAttributeMetadata` | Stable section code |
| `Name` | `Text` | Yes | `StringAttributeMetadata` | Display name |
| `DisplayOrder` | `WholeNumber` | Yes | `IntegerAttributeMetadata` | Renderer order |

### Questions

Purpose: Question metadata and renderer hints

Primary name column: `QuestionCode`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `Section` | `Lookup:Sections` | Yes | `LookupAttributeMetadata` | Parent section Lookup to `Sections`. |
| `QuestionCode` | `Text` | Yes | `StringAttributeMetadata` | Stable question code |
| `Type` | `Choice` | Yes | `PicklistAttributeMetadata` | text/integer/decimal/date/select_one/select_many/file_photo/gps Values: `text`, `integer`, `decimal`, `date`, `select_one`, `select_many`, `file_photo_attachment`, `gps`. |
| `Label` | `Text` | Yes | `StringAttributeMetadata` | Visible label |
| `HelpText` | `MultilineText` | No | `MemoAttributeMetadata` | Helper text |
| `Required` | `Boolean` | No | `BooleanAttributeMetadata` | Required true/false |
| `DisplayOrder` | `WholeNumber` | Yes | `IntegerAttributeMetadata` | Renderer order |

### Choices

Purpose: Select-one/select-many options

Primary name column: `ChoiceCode`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `Question` | `Lookup:Questions` | Yes | `LookupAttributeMetadata` | Parent question Lookup to `Questions`. |
| `ChoiceCode` | `Text` | Yes | `StringAttributeMetadata` | Stored value code |
| `Label` | `Text` | Yes | `StringAttributeMetadata` | Displayed label |
| `DisplayOrder` | `WholeNumber` | No | `IntegerAttributeMetadata` | Choice order |

### ValidationRules

Purpose: Required, simple relevance, and simple constraints

Primary name column: `Name`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `Question` | `Lookup:Questions` | Yes | `LookupAttributeMetadata` | Parent question Lookup to `Questions`. |
| `Name` | `Text` | Yes | `StringAttributeMetadata` | Primary display name for Dataverse metadata |
| `RuleType` | `Choice` | Yes | `PicklistAttributeMetadata` | required/relevant/constraint Values: `required`, `relevant`, `constraint`. |
| `Expression` | `MultilineText` | No | `MemoAttributeMetadata` | MVP subset only |
| `Message` | `MultilineText` | No | `MemoAttributeMetadata` | Visible error/help message |

### FormAssignments

Purpose: Assign active published form versions to users

Primary name column: `UserEmail`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `FormVersion` | `Lookup:FormVersions` | Yes | `LookupAttributeMetadata` | Assigned published form version Lookup to `FormVersions`. |
| `User` | `Lookup:SystemUser` | No | `LookupAttributeMetadata` | Dataverse user where available Lookup to `SystemUser`. |
| `UserEmail` | `Text` | No | `StringAttributeMetadata` | Email fallback/filter key |
| `Status` | `Choice` | Yes | `PicklistAttributeMetadata` | Active/Inactive Values: `Active`, `Inactive`. |

### Submissions

Purpose: One form instance with Draft/Submitted/Locked status

Primary name column: `UserEmail`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `FormVersion` | `Lookup:FormVersions` | Yes | `LookupAttributeMetadata` | Submitted form version Lookup to `FormVersions`. |
| `AssignedUser` | `Lookup:SystemUser` | No | `LookupAttributeMetadata` | Collector user where available Lookup to `SystemUser`. |
| `UserEmail` | `Text` | No | `StringAttributeMetadata` | Collector email snapshot |
| `Status` | `Choice` | Yes | `PicklistAttributeMetadata` | Draft/Submitted/Locked Values: `Draft`, `Submitted`, `Locked`. |
| `StartedAt` | `DateTime` | No | `DateTimeAttributeMetadata(UserLocal)` | Start timestamp |
| `SubmittedAt` | `DateTime` | No | `DateTimeAttributeMetadata(UserLocal)` | Submit timestamp |

### SubmissionAnswers

Purpose: Generic typed answer rows

Primary name column: `ValueText`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `Submission` | `Lookup:Submissions` | Yes | `LookupAttributeMetadata` | Parent submission Lookup to `Submissions`. |
| `Question` | `Lookup:Questions` | Yes | `LookupAttributeMetadata` | Question answered Lookup to `Questions`. |
| `ValueText` | `Text` | No | `StringAttributeMetadata` | Text/select code snapshot |
| `ValueNumber` | `WholeNumber` | No | `IntegerAttributeMetadata` | Integer value |
| `ValueDecimal` | `Decimal` | No | `DecimalAttributeMetadata` | Decimal value |
| `ValueDate` | `Date` | No | `DateTimeAttributeMetadata(DateOnly)` | Date value |
| `ValueBoolean` | `Boolean` | No | `BooleanAttributeMetadata` | Boolean value |
| `ValueJson` | `MultilineText` | No | `MemoAttributeMetadata` | Select-many/GPS/rare complex MVP values |

### SubmissionFiles

Purpose: Photos/documents linked to submission/question

Primary name column: `FileName`

| Column | Type | Required | Dataverse metadata | Notes |
| --- | --- | --- | --- | --- |
| `Submission` | `Lookup:Submissions` | Yes | `LookupAttributeMetadata` | Parent submission Lookup to `Submissions`. |
| `Question` | `Lookup:Questions` | Yes | `LookupAttributeMetadata` | Attachment question Lookup to `Questions`. |
| `File` | `File` | Yes | `FileAttributeMetadata` | Dataverse file column |
| `FileName` | `Text` | No | `StringAttributeMetadata` | Original filename |
| `MediaType` | `Text` | No | `StringAttributeMetadata` | MIME/media type |

## Relationships

| Relationship | Referenced table | Referencing table | Lookup column | Required | Notes |
| --- | --- | --- | --- | --- | --- |
| `Forms_FormVersions_Form` | `Forms` | `FormVersions` | `Form` | Yes | Parent form |
| `FormVersions_Sections_FormVersion` | `FormVersions` | `Sections` | `FormVersion` | Yes | Parent form version |
| `Sections_Questions_Section` | `Sections` | `Questions` | `Section` | Yes | Parent section |
| `Questions_Choices_Question` | `Questions` | `Choices` | `Question` | Yes | Parent question |
| `Questions_ValidationRules_Question` | `Questions` | `ValidationRules` | `Question` | Yes | Parent question |
| `FormVersions_FormAssignments_FormVersion` | `FormVersions` | `FormAssignments` | `FormVersion` | Yes | Assigned published form version |
| `SystemUser_FormAssignments_User` | `SystemUser` | `FormAssignments` | `User` | No | Dataverse user where available |
| `FormVersions_Submissions_FormVersion` | `FormVersions` | `Submissions` | `FormVersion` | Yes | Submitted form version |
| `SystemUser_Submissions_AssignedUser` | `SystemUser` | `Submissions` | `AssignedUser` | No | Collector user where available |
| `Submissions_SubmissionAnswers_Submission` | `Submissions` | `SubmissionAnswers` | `Submission` | Yes | Parent submission |
| `Questions_SubmissionAnswers_Question` | `Questions` | `SubmissionAnswers` | `Question` | Yes | Question answered |
| `Submissions_SubmissionFiles_Submission` | `Submissions` | `SubmissionFiles` | `Submission` | Yes | Parent submission |
| `Questions_SubmissionFiles_Question` | `Questions` | `SubmissionFiles` | `Question` | Yes | Attachment question |

## Choice Values

- `Forms.Status`: `Draft`, `Active`, `Retired`
- `FormVersions.LifecycleStatus`: `Draft`, `Published`, `Retired`
- `Questions.Type`: `text`, `integer`, `decimal`, `date`, `select_one`, `select_many`, `file_photo_attachment`, `gps`
- `ValidationRules.RuleType`: `required`, `relevant`, `constraint`
- `FormAssignments.Status`: `Active`, `Inactive`
- `Submissions.Status`: `Draft`, `Submitted`, `Locked`

## Explicitly Deferred

- Full XLSForm parser/compiler.
- Repeat groups and nested repeats.
- Complex XPath expression evaluator.
- Offline-first sync and conflict resolution.
- Barcode capture.
- Admin publishing UI and version migration.
- Dashboards and production deployment.
