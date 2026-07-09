# ADR 0002: Power Pages Hosted ODK Web Forms Runtime

Status: accepted for next MVP slice.
Date: 2026-07-09

## Context

The Canvas metadata renderer proved Dataverse authentication, assignment, draft, submit, and basic dynamic rendering, but repeated Canvas source/import and formula constraints make it a poor long-term fit for ODK Collect/Web Forms parity. The client wants Microsoft-managed services for security reasons and does not want external hosted integrations.

## Decision

Use a Power Pages hosted Vue SPA as the field user runtime. The SPA will integrate ODK Web Forms / `@getodk/xforms-engine`, authenticate through Power Pages, and read/write Dataverse through the Power Pages Web API `/_api`.

Use an ODK Central-inspired Dataverse schema: `Projects`, `Forms`, `FormVersions`, `FormAttachments`, `FormAssignments`, `Submissions`, `SubmissionVersions`, and `SubmissionAttachments`. Store canonical XForm XML and submitted instance XML/JSON as source-of-truth payloads.

## Consequences

- Power Pages site and Dataverse schema must live in the same environment.
- Browser code must use Power Pages Web API settings, table permissions, web roles, and CSRF tokens.
- Offline drafts require explicit IndexedDB/sync-queue implementation; Power Pages PWA alone is insufficient.
- Canvas becomes proof/admin/monitoring surface, not the primary ODK-style field renderer.
- `SubmissionAnswers` can be added later as an analytics projection.
