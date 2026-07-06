# Acceptance Criteria: July 7 Metadata-Driven MVP

## AC-01 Authentication

Given the user opens the app, when Power Apps loads, then the app uses the signed-in Entra/Power Apps identity and does not show a custom login flow.

## AC-02 Assigned forms

Given one published form version is assigned to the signed-in user, when the assigned forms screen loads, then only active assigned forms for that user are shown.

## AC-03 Metadata rendering

Given a published form has sections, questions, choices, and validation rules, when the user opens the form, then the app renders supported fields from metadata rather than from hard-coded TACATDP section screens.

## AC-04 Supported field types

Given the seeded form includes text, integer, decimal, date, select one, select many, and file/photo fields, when the form renders, then each supported type has an appropriate input and readable label/helper/error space.

## AC-05 Rule subset

Given a field is required, relevant based on one prior answer, or has a simple numeric/text constraint, when the user saves or submits invalid data, then the app shows visible errors and blocks successful save/submit as appropriate.

## AC-06 Drafts

Given the user saves a draft, when storage succeeds, then `Submissions`, `SubmissionAnswers`, and any `SubmissionFiles` are created or updated with status `Draft`.

## AC-07 Submit

Given the draft passes required visible validation, when Submit is selected, then the submission status changes to `Submitted`.

## AC-08 Edit until locked

Given a submission status is `Draft` or `Submitted`, when the user opens it from history, then fields are editable. Given status is `Locked`, when opened, then fields are read-only.

## AC-09 Attachment

Given the form includes one file/photo question, when the user attaches a file/photo and saves, then a `SubmissionFiles` row is linked to the submission and question.

## AC-10 History

Given the user has drafts or submissions for a selected form, when the history screen loads, then the user sees only their own submissions with status and timestamp.

## AC-11 Deferred scope protection

Given the July 7 slice is reviewed, when repeat groups, nested repeats, full XLSForm compiler, complex XPath, offline-first sync, barcode, dashboards, admin publishing UI, or version migration appear in implementation scope, then they are marked deferred unless explicitly re-approved.
