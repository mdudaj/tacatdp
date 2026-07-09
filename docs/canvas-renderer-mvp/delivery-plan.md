# Delivery Plan: Canvas Metadata Renderer MVP

## Step 1: Confirm seed and permissions

- Verify `tacatdp_prototype` solution exists.
- Verify the signed-in maker can read/write the ten MVP tables.
- Verify `john.mduda@mshirikacorp.onmicrosoft.com` can see the app and Dataverse rows required for the slice.

## Step 2: Create Canvas app shell

- Create one Canvas app in the dev environment.
- Add Dataverse tables as data sources.
- Add app to the `tacatdp_prototype` solution.
- First screen is assigned forms.

## Step 3: Assigned forms and history

- Build `AssignedFormsScreen`.
- Build `HistoryScreen` filtered to the selected form/version and current user/email.
- Validate with the seeded assignment.

## Step 4: Metadata load and renderer

- Load selected form metadata into local collections.
- Render seeded questions in order.
- Implement field controls for text, integer, decimal, date, select one, select many, attachment placeholder, and GPS placeholder/capture.

## Step 5: Save draft and submit

- Implement `Submissions` create/update.
- Implement `SubmissionAnswers` upsert.
- Implement required validation before submit.
- Implement status transition to `Submitted`.

## Step 6: Attachment path

- Add an Edit form for `SubmissionFiles` attachment upload.
- Link file row to current submission and attachment question.
- Keep one attachment field for MVP.

## Step 7: Edit until locked

- Open existing Draft/Submitted from history in edit mode.
- Render Locked as read-only.

## Step 8: Verification and packaging

- Run manual acceptance tests in Power Apps web/mobile.
- Export or save the app in the solution.
- Document any formulas or unresolved delegation warnings.
