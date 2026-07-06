# Dynamic Data Collection Data Model

## July 7 MVP model

The MVP uses a deliberately small Dataverse model to prove runtime collection before the full platform schema is built.

| Table | Key columns | Purpose |
| --- | --- | --- |
| `Forms` | `FormCode`, `Name`, `Status` | Form/instrument container. |
| `FormVersions` | `Form`, `VersionCode`, `LifecycleStatus`, `PublishedAt` | Published version metadata. |
| `Sections` | `FormVersion`, `SectionCode`, `Name`, `DisplayOrder` | Ordered form sections/pages. |
| `Questions` | `Section`, `QuestionCode`, `Type`, `Label`, `Required`, `DisplayOrder` | Renderer metadata for a question. |
| `Choices` | `Question`, `ChoiceCode`, `Label`, `DisplayOrder` | Select one / select many options. |
| `ValidationRules` | `Question`, `RuleType`, `Expression`, `Message` | Required, simple relevance, and simple constraints. |
| `FormAssignments` | `FormVersion`, `User`, `UserEmail`, `Status` | Assigns a published form version to a user. |
| `Submissions` | `FormVersion`, `AssignedUser`, `Status`, timestamps | One filled form instance. |
| `SubmissionAnswers` | `Submission`, `Question`, typed value columns | Generic answer row. |
| `SubmissionFiles` | `Submission`, `Question`, `File`, `FileName`, `MediaType` | Photo/document evidence. |

Do not create a custom `Users` table for the MVP unless profile metadata becomes necessary. Use Dataverse system users and `FormAssignments`.

## Generic answer typed columns

`SubmissionAnswers` should store typed nullable values:

- `ValueText`;
- `ValueNumber`;
- `ValueDecimal`;
- `ValueDate`;
- `ValueBoolean`;
- `ValueJson`.

For MVP, select-many and GPS can use `ValueJson` if that keeps the renderer simple. Later analytics can use projection/export tables.

## Submission statuses

Use a simple status field:

- `Draft`;
- `Submitted`;
- `Locked`.

The Canvas App may edit `Draft` and `Submitted` submissions. `Locked` submissions are read-only.

## July 7 supported rules

Support only:

- required true/false;
- relevance depending on one prior answer;
- simple numeric/text comparisons.

Defer complex XPath expressions and repeat-aware calculations.

## Long-term platform model

After the MVP works, evolve toward the richer platform model:

| Long-term concept | Purpose |
| --- | --- |
| `Project` | Top-level project/program boundary. |
| `ProjectRoleAssignment` | Project-specific user/role mapping. |
| `Instrument` / `InstrumentVersion` | Versioned form definitions. |
| `GroupDefinition` / `FieldDefinition` | Rich sections, repeats, and question metadata. |
| `FieldRule` | Required, relevance, constraint, calculation, default, and choice filters. |
| `VocabularyScheme` / `VocabularyTerm` | Reusable controlled vocabularies and reference data. |
| `TrackedEntity` / `Encounter` | Longitudinal subjects and visits. |
| `GroupInstance` | Repeat group occurrences. |
| `MultiSelectAnswer` | Normalized selected terms for analytics. |
| `SubmissionReview` / `AuditEvent` | Review, locking, and audit workflow. |
| Export/projection tables | Wide/long reporting outputs derived from normalized source data. |

These long-term concepts remain valid, but they are deferred until after the first metadata-rendered MVP slice proves the runtime path.
