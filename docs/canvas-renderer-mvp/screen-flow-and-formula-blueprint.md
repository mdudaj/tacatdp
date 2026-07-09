# Screen Flow and Formula Blueprint: Canvas Metadata Renderer MVP

## Data sources

Add these Dataverse tables to the Canvas app:

- `Forms`
- `FormVersions`
- `Sections`
- `Questions`
- `Choices`
- `ValidationRules`
- `FormAssignments`
- `Submissions`
- `SubmissionAnswers`
- `SubmissionFiles`

## App start

Set lightweight globals:

```powerfx
Set(gblUserEmail, Lower(User().Email));
Set(gblNow, Now());
```

Do not load all submission data at app start.

## AssignedFormsScreen

Purpose: first screen. No marketing or landing page.

Data pattern:

```powerfx
Filter(
    FormAssignments,
    Status = 'Status (FormAssignments)'.Active &&
    (Lower(UserEmail) = gblUserEmail || User.'Primary Email' = gblUserEmail) &&
    FormVersion.LifecycleStatus = 'LifecycleStatus (FormVersions)'.Published
)
```

Implementation note: if `Lower(UserEmail)` creates a delegation warning, store normalized email in the seed and compare exact text without `Lower()`.

Select action:

```powerfx
Set(gblAssignment, ThisItem);
Set(gblFormVersion, ThisItem.FormVersion);
Navigate(HistoryScreen);
```

## HistoryScreen

Purpose: show user's own submissions for the selected form/version and allow new/resume.

Items pattern:

```powerfx
SortByColumns(
    Filter(
        Submissions,
        FormVersion.FormVersion = gblFormVersion.FormVersion &&
        (Lower(UserEmail) = gblUserEmail || AssignedUser.'Primary Email' = gblUserEmail)
    ),
    "modifiedon",
    SortOrder.Descending
)
```

Actions:

- New: create or initialize a `Draft` submission and navigate to runner.
- Existing: set `gblSubmission` and load answers, then navigate to runner.

## RunnerScreen metadata load

On visible or after selecting a submission:

```powerfx
ClearCollect(colSections, SortByColumns(Filter(Sections, FormVersion.FormVersion = gblFormVersion.FormVersion), "mp_displayorder"));
ClearCollect(colQuestions, SortByColumns(Filter(Questions, Section.FormVersion.FormVersion = gblFormVersion.FormVersion), "mp_displayorder"));
ClearCollect(colChoices, SortByColumns(Filter(Choices, Question.Section.FormVersion.FormVersion = gblFormVersion.FormVersion), "mp_displayorder"));
ClearCollect(colRules, Filter(ValidationRules, Question.Section.FormVersion.FormVersion = gblFormVersion.FormVersion));
ClearCollect(colAnswers, Filter(SubmissionAnswers, Submission.Submission = gblSubmission.Submission));
```

Use collections only for the selected form's small metadata and active submission answers.

## Field renderer strategy

A gallery can render question labels and use conditional controls based on `ThisItem.Type`:

- text: text input writes to local answer state.
- integer: number input with integer validation.
- decimal: number input with decimal validation.
- date: date picker.
- select one: radio or combo box using `Filter(colChoices, Question.Question = ThisItem.Question)`.
- select many: combo box with multi-select; save selected choice codes as JSON in `ValueJson`.
- file/photo: navigate/open attachment card bound to `SubmissionFiles`.
- GPS: button captures `Location` and stores JSON.

## Save draft

Use `Patch` for `Submissions`, then upsert one answer row per answered question. Wrap in `IfError` and do not clear local state until writes succeed.

Pseudo-flow:

```powerfx
IfError(
    Set(
        gblSubmission,
        Patch(
            Submissions,
            Coalesce(gblSubmission, Defaults(Submissions)),
            {
                FormVersion: gblFormVersion,
                UserEmail: gblUserEmail,
                Status: 'Status (Submissions)'.Draft,
                StartedAt: Coalesce(gblSubmission.StartedAt, Now())
            }
        )
    ),
    Notify("Draft could not be saved.", NotificationType.Error),
    Notify("Draft saved.", NotificationType.Success)
)
```

## Submit

Submit should:

1. Validate required questions in `colRules`.
2. Save current answers.
3. Patch `Submissions.Status` to `Submitted` and `SubmittedAt` to `Now()`.
4. Navigate to history.

## Attachment capture

Use an Edit form bound to `SubmissionFiles` for the current submission/question because Microsoft documents that the Attachments control only supports upload/delete inside a form and does not support transformed table expressions.

## GPS capture

Capture only on button press:

```powerfx
Set(
    locGpsPoint,
    {
        latitude: Location.Latitude,
        longitude: Location.Longitude,
        altitude: Location.Altitude,
        accuracy: Location.Accuracy,
        capturedAt: Text(Now(), DateTimeFormat.UTC)
    }
)
```

Store as JSON in `SubmissionAnswers.ValueJson`.

## Lock behavior

Controls use:

```powerfx
If(gblSubmission.Status = 'Status (Submissions)'.Locked, DisplayMode.View, DisplayMode.Edit)
```
