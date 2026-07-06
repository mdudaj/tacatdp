# App Vision and MVP Strategy

## Current decision

The long-term vision is a reusable dynamic data collection platform powered by Dataverse. It should mirror the useful architecture of ODK Central and ODK Collect while using Power Apps, Dataverse, Entra authentication, and Power Platform ALM.

The near-term deliverable is the July 7, 2026 MVP described in `docs/mvp-july-7.md`:

> One published form assigned to one user, rendered dynamically in Canvas from Dataverse metadata, with draft/save/submit/history and one attachment field.

## Product shape

- **ODK Central equivalent**: Dataverse plus future admin surfaces for forms, versions, assignments, submissions, exports, monitoring, and publishing.
- **ODK Collect equivalent**: one Canvas App runtime that authenticates with Entra, shows assigned forms, renders form metadata, saves drafts, submits data, and shows history.
- **Compiler/import path**: seed one form manually or from a small JSON/YAML artifact for MVP; build XLSForm-to-Dataverse metadata compilation after the runtime path is proven.

## Why a metadata renderer now

Generating one Power App per form is not the platform architecture. It would create duplicated screens, formulas, permissions, and ALM work for every instrument.

The app should instead render metadata:

- `Forms`;
- `FormVersions`;
- `Sections`;
- `Questions`;
- `Choices`;
- `ValidationRules`;
- `FormAssignments`.

Runtime data should be generic:

- `Submissions`;
- `SubmissionAnswers`;
- `SubmissionFiles`.

## MVP boundary

The July 7 MVP is intentionally narrow:

1. Use Power Apps / Entra authentication; no custom login.
2. Show assigned published forms for the current user.
3. Render text, integer, decimal, date, select one, select many, file/photo attachment, and GPS if quick enough.
4. Save drafts and submit using `Draft`, `Submitted`, and `Locked` statuses.
5. Allow edits until locked.
6. Show the user's own submission history for a selected form.
7. Seed one form; do not build the full XLSForm compiler yet.

## Deferred platform capabilities

After the first working vertical slice, add:

- XLSForm parser/compiler;
- repeat groups and nested repeats;
- richer XPath expression support;
- offline-first sync and conflict handling;
- barcode;
- admin publishing UI;
- version migration;
- dashboards and export projections;
- richer locking/review workflows.

## Relationship to older artifacts

Older TACATDP generated screen artifacts and section-specific plans remain useful as source material and reference, but they are not the default implementation path for the platform. The active implementation path is the metadata-driven MVP documented in `docs/mvp-july-7.md` and the updated `docs/tacatdp-prototype-slice-1/` artifacts.
