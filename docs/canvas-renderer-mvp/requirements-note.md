# Requirements Note: Canvas Metadata Renderer MVP

## Requirement source

This package translates the agreed July 7 MVP into a Canvas implementation contract after the Dataverse schema and seed were deployed.

The implementation must prove the dynamic runtime path, not a one-off static TACATDP form screen.

## Required first vertical slice

One assigned published form must be visible and runnable by the assigned user:

- Form: `TACATDP-MVP-001`.
- Version: `2026-07-07-v1`.
- Assignment: `john.mduda@mshirikacorp.onmicrosoft.com`.

The app must support:

- assigned forms;
- metadata-rendered fields;
- save draft;
- submit;
- edit until locked;
- one attachment path;
- user submission history.

## Requirement interpretation

- Authentication means Power Apps/Entra authentication only.
- Assigned forms means Dataverse-filtered assignment rows, not an in-app user picker.
- Metadata rendering means loading `Sections`, `Questions`, `Choices`, and `ValidationRules` from Dataverse.
- Save/submit means writing to the generic answer model, not creating a wide table.
- Attachment means proving a linked `SubmissionFiles` record, even if the UX uses a static Edit form subflow for the first slice.
- GPS is P1 and may be deferred if it threatens draft/submit/history.

## Design boundary

Do not add these during this slice:

- full XLSForm parser;
- repeat groups;
- offline-first sync;
- barcode;
- admin publishing UI;
- dashboards;
- production ALM.
