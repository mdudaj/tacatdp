# ODK Central-Inspired Dataverse MVP Schema

Status: review-ready, no environment write.

This schema is the preferred Dataverse shape for the Power Pages hosted ODK Web Forms MVP. It stores canonical XForm XML and submitted instance payloads as source-of-truth records, while leaving decomposed answer rows as a later analytics projection.

## Tables

### Projects

Top-level project container, equivalent to ODK Central project scope.

Primary name column: `Name`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `ProjectCode` | `Text` | Yes | Stable project code. |
| `Name` | `Text` | Yes | Project display name. |
| `Description` | `MultilineText` | No | Project description. |
| `LifecycleStatus` | `Choice` | Yes | Active/Archived. Choices: Active, Archived. |

### Forms

ODK form identity within a project. XmlFormId should match the XForm form id.

Primary name column: `Name`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `Project` | `Lookup:Projects` | Yes | Parent project. |
| `XmlFormId` | `Text` | Yes | ODK XML form id. |
| `Name` | `Text` | Yes | Form display name. |
| `Description` | `MultilineText` | No | Form description. |
| `LifecycleStatus` | `Choice` | Yes | Draft/Open/Closed. Choices: Draft, Open, Closed. |

### FormVersions

Versioned canonical XForm XML and publish state.

Primary name column: `Version`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `Form` | `Lookup:Forms` | Yes | Parent form. |
| `Version` | `Text` | Yes | ODK form version string. |
| `Hash` | `Text` | No | Form definition hash when available. |
| `XFormXml` | `MultilineText` | Yes | Canonical XForm XML used by ODK Web Forms. |
| `WebFormsEnabled` | `Boolean` | No | Whether this version is fillable in the Power Pages Web Forms runtime. |
| `LifecycleStatus` | `Choice` | Yes | Draft/Published/Retired. Choices: Draft, Published, Retired. |
| `PublishedAt` | `DateTime` | No | Publish timestamp. |

### FormAttachments

Media/data files referenced by a form version.

Primary name column: `FileName`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `FormVersion` | `Lookup:FormVersions` | Yes | Parent form version. |
| `FileName` | `Text` | Yes | Attachment filename as referenced by the XForm. |
| `MediaType` | `Text` | No | MIME/media type. |
| `File` | `File` | No | Dataverse file column for binary attachment. |

### FormAssignments

Assign published form versions to Dataverse/Power Pages users or email fallback keys.

Primary name column: `AssignmentKey`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `FormVersion` | `Lookup:FormVersions` | Yes | Assigned published form version. |
| `User` | `Lookup:SystemUser` | No | Dataverse system user where available. |
| `UserEmail` | `Text` | No | Normalized email fallback/filter key. |
| `AssignmentKey` | `Text` | Yes | Stable key, for example xmlFormId:version:userEmail. |
| `LifecycleStatus` | `Choice` | Yes | Active/Inactive. Choices: Active, Inactive. |

### Submissions

Submission header keyed by ODK instanceId.

Primary name column: `InstanceId`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `FormVersion` | `Lookup:FormVersions` | Yes | Submitted form version. |
| `InstanceId` | `Text` | Yes | ODK instanceId. |
| `Submitter` | `Lookup:SystemUser` | No | Dataverse user where available. |
| `UserEmail` | `Text` | No | Submitter email snapshot. |
| `LifecycleStatus` | `Choice` | Yes | Draft/Submitted/Locked. Choices: Draft, Submitted, Locked. |
| `ReviewState` | `Choice` | No | ODK Central-inspired review state. Choices: Received, Edited, HasIssues, Rejected, Approved. |
| `StartedAt` | `DateTime` | No | Draft start timestamp. |
| `SubmittedAt` | `DateTime` | No | Submit timestamp. |
| `UpdatedAt` | `DateTime` | No | Latest local/server update timestamp. |

### SubmissionVersions

Versioned immutable/current submission payloads.

Primary name column: `VersionKey`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `Submission` | `Lookup:Submissions` | Yes | Parent submission. |
| `VersionKey` | `Text` | Yes | Stable key such as instanceId:versionNumber. |
| `VersionNumber` | `WholeNumber` | Yes | Sequential submission payload version. |
| `InstanceId` | `Text` | Yes | ODK instanceId snapshot. |
| `XFormSubmissionXml` | `MultilineText` | Yes | Canonical submitted instance XML. |
| `SubmissionJson` | `MultilineText` | No | JSON projection for app convenience and diagnostics. |
| `Current` | `Boolean` | No | True when this is the current payload version. |
| `UserAgent` | `Text` | No | Browser user agent snapshot. |
| `DeviceId` | `Text` | No | Optional field device/client id. |
| `CreatedAt` | `DateTime` | No | Payload version creation timestamp. |

### SubmissionAttachments

Media/files attached to a submission version.

Primary name column: `FileName`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| `SubmissionVersion` | `Lookup:SubmissionVersions` | Yes | Parent submission version. |
| `FileName` | `Text` | Yes | Original filename or XForm media reference. |
| `MediaType` | `Text` | No | MIME/media type. |
| `File` | `File` | No | Dataverse file column. |
| `CapturedAt` | `DateTime` | No | Capture timestamp when known. |
| `UploadedAt` | `DateTime` | No | Upload timestamp. |

## Relationships

| Referenced | Referencing | Lookup | Required | Notes |
| --- | --- | --- | --- | --- |
| `Projects` | `Forms` | `Project` | Yes | Project forms. |
| `Forms` | `FormVersions` | `Form` | Yes | Form versions. |
| `FormVersions` | `FormAttachments` | `FormVersion` | Yes | Form media attachments. |
| `FormVersions` | `FormAssignments` | `FormVersion` | Yes | Assigned form version. |
| `SystemUser` | `FormAssignments` | `User` | No | Assigned user. |
| `FormVersions` | `Submissions` | `FormVersion` | Yes | Submitted form version. |
| `SystemUser` | `Submissions` | `Submitter` | No | Submitter user. |
| `Submissions` | `SubmissionVersions` | `Submission` | Yes | Submission payload versions. |
| `SubmissionVersions` | `SubmissionAttachments` | `SubmissionVersion` | Yes | Submission media/files. |

## Deferred

- Datasets, Entities, and EntityVersions for longitudinal workflows.
- SubmissionAnswers analytics projection.
- OpenRosa-compatible API surface.
- Full XLSForm compiler and publishing UI.
