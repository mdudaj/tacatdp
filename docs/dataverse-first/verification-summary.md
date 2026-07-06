# Verification Summary: July 7 Metadata-Driven MVP

## Planned verification

1. `pac auth who` confirms the intended service principal or maker identity.
2. `pac solution list --environment "$POWER_PLATFORM_ENVIRONMENT_URL"` confirms Dataverse connectivity.
3. The MVP solution contains only the approved MVP tables unless extra tables are explicitly justified.
4. Seed data creates one form, one published version, sections, questions, choices, rules, and one assignment.
5. Canvas assigned forms list shows only the assigned published form.
6. Form runner renders fields from metadata.
7. Save Draft creates/updates submission, answer, and file rows.
8. Submit changes status to `Submitted`.
9. History shows only the current user's submissions.
10. Locked state blocks editing.

## Current verification state

- PAC/Dataverse connection: validated by user-provided `pac solution list` and `pac org who` output.
- Documentation alignment: updated to make `docs/mvp-july-7.md` the canonical MVP scope.
- Dataverse environment writes: not performed by this documentation update.
