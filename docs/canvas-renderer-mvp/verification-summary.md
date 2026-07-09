# Verification Summary: Canvas Metadata Renderer MVP

## Current status

Planning artifacts are ready. Canvas app implementation has not started in this artifact pack.

## Inputs verified

- Dataverse schema exists in dev.
- Seeded form exists: `TACATDP-MVP-001` / `2026-07-07-v1`.
- Active assignment exists for `john.mduda@mshirikacorp.onmicrosoft.com`.
- The app should target the seeded metadata first.

## Verification to perform during implementation

- Assigned user opens app and sees the seeded form.
- User saves a partial draft and sees it in history.
- User reopens draft and answers persist.
- User submits after required fields are complete.
- User attaches one file/photo.
- User captures GPS or GPS is explicitly deferred.
- Submitted row remains editable until status is manually set to `Locked` for test.
- Locked row renders read-only.

## Open risks

- Attachment control constraints may require a static edit-form subflow rather than a fully dynamic field control.
- `User().Email` returns UPN, so assignment matching must preserve the seeded UPN/email fallback.
- Delegation warnings must be reviewed before calling the renderer scalable.

## July 6, 2026 Slice Scaffold Verification

Commands run:

```bash
python3 scripts/validate-canvas-renderer-slice.py
python3 -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted(Path('app-src-metadata-renderer/Src').glob('*.pa.yaml'))]; print('OK: YAML parses')"
```

Results:

- `OK: Canvas renderer slice artifacts are present and aligned with the July 7 MVP.`
- `OK: YAML parses`

Notes:

- The installed PAC CLI reports `pac canvas validate` as unsupported, so local validation is limited to artifact checks and YAML parsing until the app is built/saved in Power Apps Studio.
- The existing generated fixed-screen `app-src/` was not overwritten. The metadata renderer slice is isolated under `app-src-metadata-renderer/`.
- The next verification gate is Studio App Checker plus a live test against the seeded form assignment.

## July 6, 2026 Studio Artifact Packaging Verification

Input artifact:

- `artifacts/TACATDP Metadata Renderer.msapp`

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP.msapp`

Commands run:

```bash
pac canvas unpack --msapp artifacts/'TACATDP Metadata Renderer.msapp' --sources app-src-studio --layout SourceCode --overwrite
pac canvas pack --sources app-src-studio --msapp artifacts/'TACATDP Metadata Renderer - MVP.msapp' --layout SourceCode --overwrite
pac canvas unpack --msapp artifacts/'TACATDP Metadata Renderer - MVP.msapp' --sources /tmp/tacatdp-mvp-roundtrip --layout SourceCode --overwrite
python3 scripts/validate-canvas-renderer-slice.py
python3 -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted(Path('app-src-studio/Src').glob('*.pa.yaml'))]; print('OK: studio YAML parses')"
```

Results:

- Studio-created `.msapp` unpacked successfully.
- Renderer formulas were applied to `app-src-studio/Src`.
- MVP `.msapp` packed successfully.
- MVP `.msapp` round-trip unpacked successfully.
- Packed artifact includes references for all ten MVP Dataverse tables.
- Embedded App Checker SARIF exists and has no results in the packed package.

Remaining live gate:

- Open `artifacts/TACATDP Metadata Renderer - MVP.msapp` in Power Apps Studio, run App Checker against the live environment, publish, and test the seeded assignment flow.

## July 7, 2026 App Checker Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v2.msapp`

Fix scope:

- Removed `Lower(UserEmail)` from Dataverse filters.
- Quoted ambiguous Dataverse choice field references such as `'Status'`.
- Used `Text(gblSubmission.'Status') = "Locked"` for locked display-mode checks.
- Replaced nested lookup-id chains with direct lookup record comparisons for the seeded MVP section.
- Removed the undefined `gblAttachmentQuestion` dependency.
- Used `[@Choices]` for the metadata Choices table.

Verification:

- `pac canvas pack` succeeded for the v2 artifact.
- `pac canvas unpack` round-trip succeeded for the v2 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` now targets the v2 artifact.

## July 7, 2026 MVP v3 App Checker Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v3.msapp`

Reason for v3:

- The v2 import still failed on the custom choice display name `Status` and produced delegation warnings on Dataverse lookup-column comparisons.
- Microsoft documents that display names are not unique and can be disambiguated by Studio, while Dataverse tables also have built-in state/status fields.
- Microsoft delegation docs list `Lower` as nondelegable on columns and warn that nondelegable query parts are processed locally.

Fix scope:

- Removed all formula references to custom `Status` choice columns.
- Removed assigned-form status/lifecycle choice filters from the package; seeded assignment data is the MVP filter boundary.
- Used `StartedAt` and `SubmittedAt` timestamps for the demo lifecycle.
- Moved lookup filtering that caused warnings to local collections for the small seeded metadata/user-submission slice.
- Compared lookup primary ids in local collections, for example `FormVersion.FormVersions = gblFormVersion.FormVersions` and `Submission.Submissions = gblSubmission.Submissions`.

Verification:

- `pac canvas pack` succeeded for the v3 artifact.
- `pac canvas unpack` round-trip succeeded for the v3 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v3 artifact.
- Studio YAML parses locally.

Remaining product gap:

- `Edit until locked` is not enforced in v3 because the custom `Status` choice column is intentionally removed from formulas. Durable fix: rename Dataverse status columns to domain-specific names such as `SubmissionStatus` and `AssignmentStatus`, update seed data, then reintroduce lock checks from Studio-normalized source.

## July 7, 2026 MVP v4 Runner Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v4.msapp`

Reason for v4:

- The third Studio import reported remaining `RunnerScreen` errors only: missing `Choices`, unsupported `Location.Accuracy`, `ValueBoolean` type mismatch, and invalid mixed-type `Coalesce` validation.

Fix scope:

- Removed `Choices` table loading because the downloaded app package does not include a bound `Choices` data source.
- Removed `Location.Accuracy`; Microsoft documents `Location.Latitude`, `Location.Longitude`, and `Location.Altitude` only.
- Removed `ValueBoolean` patching until Studio confirms the imported Dataverse field type.
- Replaced mixed-type `Coalesce` required validation with an answer-record existence check.

Verification:

- `pac canvas pack` succeeded for the v4 artifact.
- `pac canvas unpack` round-trip succeeded for the v4 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v4 artifact.
- Studio YAML parses locally.
- Embedded package `AppCheckerResult.sarif` has zero results, noting this is package metadata and not a substitute for Studio App Checker after import.

## July 7, 2026 MVP v5 Collection and Date Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v5.msapp`

Reason for v5:

- The fourth Studio import reported two remaining `RunnerScreen` issues: `Clear` invalid argument in `OnVisible`, and `ValueDate` patch type mismatch in `SaveDraftButton.OnSelect`.

Fix scope:

- Removed all `Clear(...)` calls from importable formulas.
- Initialized local collections with `ClearCollect(...)` and data-source schema filters.
- Used `RemoveIf(colPendingAnswers, true)` after initializing the staged answer collection.
- Removed `ValueDate` patching until a real date renderer control creates a confirmed Date-typed staged value.

Verification:

- `pac canvas pack` succeeded for the v5 artifact.
- `pac canvas unpack` round-trip succeeded for the v5 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v5 artifact.
- Studio YAML parses locally.
- The packed `RunnerScreen.pa.yaml` contains no `Clear(`, `ValueDate`, `ValueBoolean`, `Location.Accuracy`, or `[@Choices]` formula references.
- Embedded package `AppCheckerResult.sarif` has zero results, noting this is package metadata and not a substitute for Studio App Checker after import.

## July 7, 2026 MVP v6 Literal Predicate Warning Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v6.msapp`

Reason for v6:

- Studio App Checker reported one warning in `RunnerScreen.OnVisible`: `This predicate is a literal value and doesn't reference input table`.

Fix scope:

- Replaced `Filter(colQuestions, false)` with `FirstN(colQuestions, 0)` after `colQuestions` is populated as a local collection.
- Removed remaining `Filter(DataSource, false)` initializers from `App.OnStart` to avoid the same warning pattern reappearing elsewhere.
- Kept staged collection initialization with `ClearCollect(... Table(...)); RemoveIf(..., true)`.

Verification:

- `pac canvas pack` succeeded for the v6 artifact.
- `pac canvas unpack` round-trip succeeded for the v6 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v6 artifact.
- Studio YAML parses locally.
- The packed `App.pa.yaml` and `RunnerScreen.pa.yaml` contain no `Filter(..., false)`, `Clear(`, `ValueDate`, `ValueBoolean`, `Location.Accuracy`, or `[@Choices]` formula references.
- Embedded package `AppCheckerResult.sarif` has zero results, noting this is package metadata and not a substitute for Studio App Checker after import.

## July 7, 2026 MVP v7 Accessibility and Performance Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v7.msapp`

Fix scope:

- Added accessible labels and tab order metadata.
- Marked non-interactive headings/instructions with `TabIndex = -1`.
- Removed unused app variables/collections from source formulas.
- Removed `ForAll(... Patch(...))` from `SaveDraftButton`.

Verification:

- `pac canvas pack` succeeded for the v7 artifact.
- `pac canvas unpack` round-trip succeeded for the v7 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v7 artifact.
- Studio YAML parses locally.
- The source contains `AccessibleLabel` and `TabIndex`, and no `ForAll(` formula references.

Remaining Studio-only cleanup:

- Remove unused `Activities` and `Forms` data sources in Studio after import. These are package reference entries, not source formulas.

## July 7, 2026 MVP v8 Source Code Import Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v8.msapp`

Fix scope:

- Corrected the v7 import failure by removing source-schema-rejected accessibility properties from Label and Button controls.
- Preserved supported accessibility metadata on buttons and galleries.
- Updated `scripts/validate-canvas-renderer-slice.py` to guard against reintroducing the rejected property combinations.

Verification:

- `pac canvas pack` succeeded for the v8 artifact.
- `pac canvas unpack` round-trip succeeded for the v8 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v8 artifact.
- Studio YAML parses locally.

Remaining Studio-only cleanup:

- Run Studio import/open and App Checker against v8. If focus/heading warnings remain, resolve them through Studio-supported properties or Studio-normalized source, not by hand-adding rejected properties to `*.pa.yaml`.
- Remove unused `Activities` and `Forms` data sources in Studio after import.

## July 7, 2026 MVP v9 Accessibility, Performance, and Data-Source Cleanup Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v9.msapp`

Fix scope:

- Converted remaining warning-producing title/instruction labels to focusable text-styled buttons with accessible labels.
- Removed whole-table collection staging from History and Runner formulas.
- Removed stale package data-source references for `Activities`, `Forms`, and `ValidationRules`; the package now carries only `FormVersions`, `Sections`, `Questions`, `FormAssignments`, `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`.
- Updated validator coverage for v9 package metadata and stale collection patterns.

Verification:

- `pac canvas pack` succeeded for the v9 artifact.
- `pac canvas unpack` round-trip succeeded for the v9 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v9 artifact.
- Studio source YAML parses locally.
- Parsed package metadata confirms only the seven used Dataverse data sources remain.

Remaining Studio gate:

- Import/open v9 in Studio and run App Checker. If Studio still reports accessibility semantics on text-styled heading buttons, resolve in Studio with supported heading/text properties or normalized source-control output.

## July 7, 2026 MVP v10 Button Source Schema Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v10.msapp`

Fix scope:

- Removed explicit `Button@2.2.0` versions from generated source.
- Removed Button styling properties that Studio rejected during v9 import.
- Updated validator coverage for the rejected Button properties.

Verification:

- `pac canvas pack` succeeded for the v10 artifact.
- `pac canvas unpack` round-trip succeeded for the v10 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for the v10 artifact.
- Studio source YAML parses locally.
- Packed source scan confirms no explicit `Button@2.2.0` controls and no rejected Button styling properties.

## July 7, 2026 MVP v11 Assigned Form Visibility Fix Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v11.msapp`

Evidence checked:

- Live Dataverse query confirms one `FormAssignments` row exists for `john.mduda@mshirikacorp.onmicrosoft.com`.
- v10 `AssignedFormsGallery.Items` was correct but the generated gallery had no visible template child controls, so the assigned row could appear as an empty area during Play.

Fix scope:

- Added `AssignedFormsStatus` to show whether the current `User().Email` filter matches a seeded assignment.
- Added `OpenAssignedFormButton` to open the first matching assignment directly for the one-assignment MVP smoke test.
- Kept the original gallery for later Studio-normalized template work.
- Updated validator markers so this visible assigned-form path is required.

Verification:

- `pac canvas pack` succeeded for v11.
- `pac canvas unpack` round-trip succeeded for v11.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for v11.
- Packed source scan confirms the status and direct-open controls exist, and no rejected Button version/style properties reappeared.

Smoke-test instruction:

- Import/open v11. If the screen says `Assigned form found for ...`, click `Open assigned form`. If it says `No assigned forms for ...`, seed or update a `FormAssignments.UserEmail` row to match the displayed email before continuing the smoke test.

## July 7, 2026 MVP v12 Seeded Field Visibility Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v12.msapp`

Evidence checked:

- Runtime smoke test reached `RunnerScreen` but no data-entry fields were visible; the generated `QuestionsGallery` had metadata items but no visible template controls.
- Existing fixed-screen source uses `Classic/TextInput@2.3.2`, so v12 uses that proven input-control shape for the seeded MVP fields.

Fix scope:

- Added visible labels and `Classic/TextInput@2.3.2` controls for seeded fields: farmer name, farmer age, land size acres, visit date, primary crop, and support needed.
- Updated Save Draft to patch `SubmissionAnswers` for the seeded question codes.
- Updated Submit validation to require farmer name, visit date, and primary crop.
- Kept GPS capture through `ValueJson`.
- Stored visible input answers in `ValueText` for the share candidate to avoid reintroducing previous date/number binding errors; typed answer storage remains a post-share hardening task.

Verification:

- `pac canvas pack` succeeded for v12.
- `pac canvas unpack` round-trip succeeded for v12.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for v12.
- Packed source scan confirms visible seeded input controls exist and rejected Button/typed-field patterns did not reappear.

Smoke-test instruction:

- Import/open v12, select the assigned form, click `New`, enter values in the visible fields, click `Save`, then click `Submit`.


## July 7, 2026 MVP v13 Wizard Review Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v13.msapp`

Reason for v13:

- Live smoke testing showed fields rendered and draft save worked, but the runner had no next/review step.
- The MVP needs a shareable collector flow closer to ODK Collect and REDCap Mobile: enter answers, save draft, review, submit, and return to history.

Fix scope:

- Added `ReviewScreen` to the Canvas source and editor screen order.
- Replaced direct runner submit with top `ReviewButton` plus bottom `RunnerNextButton`, which capture current visible values, save the draft, and navigate to review.
- Added `ReviewSubmitButton`, which validates farmer name, visit date, and primary crop before patching `SubmittedAt`.
- Added `HistoryStatus` and `OpenLatestSubmissionButton` so history is not blank if gallery template rendering remains weak after import.
- Updated visible seeded inputs to default from existing `SubmissionAnswers.ValueText` rows when reopening a saved draft/submission.
- Updated the validator to require the review screen and v13 package while retaining guards against known import failures.

Verification:

```bash
pac canvas pack --sources app-src-studio --msapp 'artifacts/TACATDP Metadata Renderer - MVP v13.msapp' --layout SourceCode --overwrite
pac canvas unpack --msapp 'artifacts/TACATDP Metadata Renderer - MVP v13.msapp' --sources /tmp/tacatdp-mvp-v13-roundtrip --layout SourceCode --overwrite
python3 scripts/validate-canvas-renderer-slice.py
python3 -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted(Path('app-src-studio/Src').glob('*.pa.yaml'))]; print('OK: studio YAML parses')"
```

Results:

- `pac canvas pack` succeeded for the v13 artifact.
- `pac canvas unpack` round-trip succeeded for the v13 artifact.
- `python3 scripts/validate-canvas-renderer-slice.py` passes for v13.
- Studio YAML parses locally.
- Packed source scan found none of the banned import-regression patterns: versioned generated buttons, rejected button style props, `Location.Accuracy`, `ValueDate`, `ValueBoolean`, `ForAll`, or `Clear`.

Remaining live gate:

- Import/open `artifacts/TACATDP Metadata Renderer - MVP v13.msapp` in Power Apps Studio, run App Checker, and smoke-test assigned form -> new draft -> save -> review -> submit -> history.


## July 7, 2026 MVP v14 Shell and Entry Revision Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v14.msapp`

Reason for v14:

- Smoke-test review showed the entry screen was using identity as status copy: `Assigned form found for john.mduda@mshirikacorp.onmicrosoft.com`.
- The assigned form action showed only the version code, which is not enough when multiple forms or versions exist.
- The MVP needs a repeatable design-system rule for later agents: app shell identity belongs in the header, and assignment rows show form name plus version.

Fix scope:

- Added a signed-in-user header row to Assigned Forms, History, Runner, Review, and Attachment screens.
- Reorganized the assigned-forms screen into app title, identity, state message, selectable assigned form, and hidden/gallery fallback.
- Changed assigned form display to `Form.Name - VersionCode` with seeded POC fallback.
- Added `docs/canvas-renderer-mvp/design-system.md`.
- Updated the validator to require signed-in-user headers, form name plus version display, and to block the old identity-in-status pattern.

Verification:

```bash
pac canvas pack --sources app-src-studio --msapp 'artifacts/TACATDP Metadata Renderer - MVP v14.msapp' --layout SourceCode --overwrite
pac canvas unpack --msapp 'artifacts/TACATDP Metadata Renderer - MVP v14.msapp' --sources /tmp/tacatdp-mvp-v14-roundtrip --layout SourceCode --overwrite
python3 scripts/validate-canvas-renderer-slice.py
python3 -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted(Path('app-src-studio/Src').glob('*.pa.yaml'))]; print('OK: studio YAML parses')"
```

Remaining live gate:

- Import/open `artifacts/TACATDP Metadata Renderer - MVP v14.msapp` in Power Apps Studio and confirm App Checker plus entry-screen visual behavior.


## July 7, 2026 MVP v15 Phone Layout and Draft Status Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v15.msapp`

Reason for v15:

- Phone smoke testing showed the app still behaved like a tablet canvas. Package properties had `DocumentLayoutScaleToFit=true`, `DocumentLayoutMaintainAspectRatio=true`, landscape `1366x768`. Microsoft responsive canvas app guidance says to disable Scale to fit, Lock aspect ratio, and Lock orientation for responsive apps.
- Creating a new submission showed `mp_status is required`. `Submissions.Status` is application-required in the Dataverse schema.

Fix scope:

- Updated package display properties to disable scale-to-fit and aspect-ratio lock.
- Removed the Canvas `Status` patch again after Studio reported that the column does not exist in formulas. The required-level fix belongs in Dataverse metadata, not Canvas source.
- Updated validator to require responsive package properties and the Draft status patch.

Remaining live gate:

- Import/open `artifacts/TACATDP Metadata Renderer - MVP v15.msapp`, play on phone, and confirm New no longer reports `mp_status is required`.


## July 7, 2026 MVP v16 Status-Free Canvas Package

Generated artifact:

- `artifacts/TACATDP Metadata Renderer - MVP v16.msapp`

Reason for v16:

- Studio reported formula errors after v15: the `Status` column did not exist in the Canvas formula binding, and the `Patch` call had invalid arguments. This repeats the earlier finding that generic custom Dataverse `Status` columns are fragile in imported Canvas source because built-in state/status columns also exist.

Fix scope:

- Removed all `Status (Submissions)` usage from Canvas source.
- Kept phone-responsive package display settings from v15.
- Updated the validator to fail any Canvas source dependency on `Status (Submissions)`.
- Added a separate guarded Dataverse metadata fix path to relax `Submissions.Status` required level in dev.

Remaining live gate:

- Run the guarded Dataverse metadata fix in dev, import/open `artifacts/TACATDP Metadata Renderer - MVP v16.msapp`, then confirm `New` no longer reports `mp_status is required`.
