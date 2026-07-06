# User Stories: July 7 Metadata-Driven MVP

## MVP-US-01: See assigned forms

As a data collector, I want to see forms assigned to me so that I know what data I am expected to capture.

Acceptance:

1. The app uses my Power Apps/Entra identity.
2. The assigned forms list is filtered to active published form versions assigned to me.
3. No custom login is shown.

## MVP-US-02: Fill a metadata-rendered form

As a data collector, I want the app to render a form from Dataverse metadata so that different forms can run in the same Canvas App.

Acceptance:

1. Sections and questions come from metadata.
2. Text, integer, decimal, date, select one, and select many fields render.
3. Labels, helper text, and errors are visible.

## MVP-US-03: Save and resume a draft

As a data collector, I want to save a draft and reopen it from history so that I can continue incomplete work.

Acceptance:

1. Save Draft stores a `Draft` submission and answer rows.
2. The draft appears in my history.
3. Reopening the draft restores saved answers.

## MVP-US-04: Submit and edit until locked

As a data collector, I want to submit a form and still edit it until it is locked so that corrections are possible before review closes the record.

Acceptance:

1. Submit changes status to `Submitted`.
2. Draft and Submitted records remain editable.
3. Locked records are read-only.

## MVP-US-05: Attach evidence

As a data collector, I want to attach a photo or document so that evidence can be stored with a submission.

Acceptance:

1. One file/photo question is available in the seeded form.
2. Saving links the file to the submission and question.
3. The attachment is visible when reopening the submission.

## MVP-US-06: Seed one form without a compiler

As a developer/maker, I want to seed one form manually or from a small JSON/YAML artifact so that the renderer can be proven before building the XLSForm compiler.

Acceptance:

1. One form, version, sections, questions, choices, rules, and assignment are seeded.
2. The seed is reviewable.
3. Full XLSForm compiler work is deferred.
