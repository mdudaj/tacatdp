# MVP: Dynamic Dataverse Data Collection Platform by July 7, 2026

## Decision

The first deliverable is a narrow metadata-driven data collection MVP, not a full TACATDP screen build, full XLSForm compiler, or complete ODK parity platform.

The MVP must prove one vertical slice:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

This proves the core architecture without overbuilding. After this works, add XLSForm import, repeat groups, offline behavior, barcode, dashboards, and advanced ODK parity incrementally.

## Product framing

Long-term vision: a dynamic data collection platform powered by Dataverse that mirrors the useful architecture of ODK Central and ODK Collect while using the Microsoft Power Platform ecosystem.

Near-term MVP:

- Power Apps Canvas is the data collection runtime.
- Dataverse stores form metadata, assignments, submissions, answers, and files.
- The app renders metadata instead of generating one app per form.
- TACATDP is the first seeded form and project context.

## MVP scope

### 1. Authentication

Use Power Apps / Entra authentication. Do not build custom login.

### 2. Assigned forms

Use `FormAssignments` to show only forms assigned to the current Dataverse user/email and active published form version.

### 3. Metadata renderer

Support only these field/control types for the July 7 slice:

- text;
- integer;
- decimal;
- date;
- select one;
- select many;
- photo/file attachment;
- GPS point if quick enough.

Defer repeat groups, barcode, advanced calculations, and complex XPath-style expressions.

### 4. Drafts and submit

Use:

- `Submissions`;
- `SubmissionAnswers`;
- `SubmissionFiles`.

Submission status values:

- `Draft`;
- `Submitted`;
- `Locked`.

### 5. Edit until locked

Allow edit when status is `Draft` or `Submitted`. Block edit when status is `Locked`.

### 6. History

Show the current user's own submissions for the selected form.

### 7. Admin seed

Do not build a full XLSForm compiler yet. For MVP, seed one form into Dataverse metadata from a small JSON/YAML artifact or manual import. Build the compiler after the runtime path is proven.

## MVP Dataverse tables

Use these tables for the July 7 MVP:

| Table | Purpose |
| --- | --- |
| `Forms` | Form/instrument container. |
| `FormVersions` | Published version metadata and lifecycle status. |
| `Sections` | Ordered form sections/pages. |
| `Questions` | Question metadata and renderer hints. |
| `Choices` | Select-one/select-many options. |
| `ValidationRules` | Required, relevance, and simple constraints. |
| `FormAssignments` | User/form-version assignment. |
| `Submissions` | One form instance with status and timestamps. |
| `SubmissionAnswers` | Generic typed answer rows. |
| `SubmissionFiles` | Photos/documents linked to submission/question. |

Do not create a custom `Users` table unless profile metadata becomes necessary. Use Dataverse system users and a lightweight assignment table referencing users or user email.

## Generic answer storage

Store answers in `SubmissionAnswers`:

| Column | Purpose |
| --- | --- |
| `Submission` | Parent submission. |
| `Question` | Question metadata row. |
| `ValueText` | Text and select code/label snapshots where appropriate. |
| `ValueNumber` | Integer/whole-number value. |
| `ValueDecimal` | Decimal value. |
| `ValueDate` | Date value. |
| `ValueBoolean` | Boolean value. |
| `ValueJson` | Select-many arrays, GPS object, or rare complex MVP values. |

This keeps the runtime generic and fast. Later analytics can use export views, projections, or compiled wide tables.

## July 7 rule-expression subset

ODK/XLSForm logic is intentionally richer than the MVP. For July 7, support only:

- `required = true/false`;
- `relevant` depending on one prior answer;
- simple numeric/text constraints such as equality and comparison.

Reference: ODK form logic is richer and continuously re-evaluates calculations, relevance, constraints, and repeats: `https://docs.getodk.org/form-logic/`.

## Deferred until after first vertical slice

- full XLSForm parser/compiler;
- repeat groups;
- nested repeats;
- complex XPath expressions;
- offline-first sync;
- barcode;
- admin publishing UI;
- version migration;
- dashboards;
- locking workflow beyond a simple status field.

## Implementation priority

1. Confirm PAC/Dataverse dev access works.
2. Create or prepare the MVP Dataverse tables in a dev solution after explicit approval.
3. Seed one published TACATDP form version, sections, questions, choices, validation rules, and one assignment.
4. Build the Canvas assigned-forms screen.
5. Build the metadata-driven form runner for the supported MVP field types.
6. Implement Save Draft, Submit, edit-until-locked, attachment upload, and history.
7. Verify with one assigned user and one published form.
