# Acceptance Criteria: Canvas Metadata Renderer MVP

## AC-01 Authentication

Given the user opens the app, when the app loads, then no custom login screen is shown and the app uses the signed-in Power Apps user.

## AC-02 Assigned form list

Given `john.mduda@mshirikacorp.onmicrosoft.com` has an active assignment, when that user opens the app, then `TACATDP MVP Field Visit` is visible in the assigned forms list.

## AC-03 Metadata load

Given the user selects the assigned form, when the runner opens, then the app loads the published version, section, questions, choices, and validation rules from Dataverse.

## AC-04 Field rendering

Given the seeded form is loaded, when the questions render, then the app displays controls for text, integer, decimal, date, select one, select many, attachment, and GPS placeholder/capture.

## AC-05 Required validation

Given required answers are blank, when the user selects Submit, then submit is blocked and the required fields show clear errors.

## AC-06 Save draft

Given the user enters any subset of answers, when Save Draft succeeds, then one `Submissions` row exists with status `Draft` and answer rows exist in `SubmissionAnswers`.

## AC-07 Submit

Given required answers are complete, when Submit succeeds, then the submission status changes to `Submitted` and history shows the submitted record.

## AC-08 Edit until locked

Given a submission has status `Draft` or `Submitted`, when the user opens it from history, then controls are editable. Given the status is `Locked`, controls are read-only.

## AC-09 Attachment

Given the user attaches one file/photo, when the submission is saved, then `SubmissionFiles` has a row linked to the submission and attachment question.

## AC-10 GPS

Given GPS capture is implemented and the user grants location permission, when the user captures location, then `SubmissionAnswers.ValueJson` stores latitude, longitude, altitude/accuracy when available, and captured timestamp.

## AC-11 Delegation hygiene

Given the app formulas are reviewed, when assignment/history queries are inspected, then they avoid known nondelegable patterns for Dataverse filtering.

## AC-12 Idempotent user path

Given the user saves, leaves, and reopens the app, when they select the draft from history, then previous answers are loaded and can be edited.
