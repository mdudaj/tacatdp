# Delivery Checklist: Canvas Metadata Renderer MVP

## Before build

- [x] Confirm schema deployment verified.
- [x] Confirm seed form verified.
- [x] Confirm service principal can read/write Dataverse metadata and solution data.
- [ ] Confirm maker account can create/update Canvas apps in the target environment.
- [ ] Confirm target assignment user can access the published app and Dataverse tables.

## Canvas app setup

- [x] Implementation-ready slice scaffold created under `app-src-metadata-renderer/`.
- [x] Formula catalog created at `docs/canvas-renderer-mvp/formula-catalog.md`.
- [x] App start, assigned forms, history, runner, attachment, submit, lock, and GPS formulas defined.
- [ ] App created or updated in dev environment through Power Apps Studio.
- [ ] App added to `tacatdp_prototype` solution.
- [ ] Data sources added for all ten MVP tables.
- [ ] App starts at assigned forms screen.

## Runtime

- [x] Live Dataverse assignment row verified for the seeded user.
- [ ] Assigned forms list works for seeded user.
- [x] Assigned-forms screen has visible status/direct-open controls in v11 package.
- [x] History screen has visible status and direct latest-submission reopen controls in v13 package.
- [ ] History gallery works for selected form/version after Studio import.
- [ ] Metadata loads from Dataverse.
- [ ] Seeded questions render in order.
- [x] Runner screen has visible seeded input controls in v12 package.
- [ ] Choices load from `Choices` table.
- [x] Required validation exists on review submit for farmer name, visit date, and primary crop.
- [ ] Required validation confirmed in Studio after v13 import.
- [ ] Save Draft creates/updates submission and answers.
- [x] Submit patches `SubmittedAt` in v13 package.
- [ ] Durable `Submitted` status field naming restored after status-column hardening.
- [x] Visible seeded input defaults read saved `SubmissionAnswers.ValueText` when reopening a submission in v13 package.
- [ ] Draft/submitted reopen confirmed in Studio after v13 import.
- [ ] Locked records render read-only.
- [ ] Attachment writes to `SubmissionFiles`.
- [ ] GPS writes to `SubmissionAnswers.ValueJson` if device/browser permission is available.

## Quality gates

- [x] Local artifact readiness validator passes.
- [x] Canvas YAML scaffold parses as YAML.
- [ ] App Checker run completed in Studio.
- [ ] No delegation warnings on assigned form and history queries, or warnings are documented with rationale.
- [ ] Error handling exists around write paths.
- [ ] Mobile viewport checked.
- [x] Accessibility labels exist for interactive controls in the packaged MVP source.
- [ ] Verification summary updated after Studio test.

## Studio cleanup

- [x] Remove unused `Activities`, `Forms`, and `ValidationRules` data-source references from the v9 package metadata; confirm in Studio after import.

## v13 wizard slice

- [x] Review step exists between data entry and submit.
- [x] Review submit validates required seeded fields before patching `SubmittedAt`.
- [x] v13 `.msapp` package created and round-trip unpacked locally.
- [ ] v13 imported/opened in Studio and App Checker run completed.

## v14 shell and entry revision

- [x] Every MVP screen source includes a signed-in user header.
- [x] Assigned form action shows form name plus version.
- [x] Assignment state message no longer embeds the user email.
- [ ] v14 imported/opened in Studio and App Checker run completed.

## v15 phone layout and draft status

- [x] Package display settings disable scale-to-fit and aspect ratio lock.
- [x] New draft formula sets required `Submissions.Status` to Draft.
- [ ] v15 imported/opened in Studio and phone smoke test completed.

## v16 status-free Canvas package

- [x] Canvas source no longer references `Status (Submissions)`.
- [x] Package remains phone-responsive.
- [ ] Dev Dataverse `Submissions.Status` required level relaxed or status column renamed.
- [ ] v16 imported/opened in Studio and New draft smoke test completed.
