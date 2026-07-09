# Formula Catalog: July 7 Canvas Renderer Slice

## Data sources

Add these Dataverse tables to the Canvas app: `Forms`, `FormVersions`, `Sections`, `Questions`, `Choices`, `ValidationRules`, `FormAssignments`, `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`.

Do not add a custom login screen. Authentication is the standard Power Apps / Entra user context.

## App.OnStart

```powerfx
Set(gblUserEmail, Lower(User().Email));
ClearCollect(colPendingAnswers, Table({Question: Blank(), ValueText: Blank(), ValueNumber: Blank(), ValueJson: Blank()}));
RemoveIf(colPendingAnswers, true);
ClearCollect(colValidationErrors, Table({Question: Blank()}));
RemoveIf(colValidationErrors, true);
Set(gblCurrentSection, Blank());
```


## App shell header

Every screen should display the signed-in user at the top, immediately below the title/action row:

```powerfx
"Signed in as " & gblUserEmail
```

Keep status copy user-neutral. Do not use messages such as `Assigned form found for <email>`; identity belongs in the header.

## Assigned forms gallery

The import-safe MVP formula uses normalized `UserEmail` only. It does not reference the custom `Status` choice column because Studio is not binding that column name consistently after import. Display each selectable assignment as `Form.Name - VersionCode`, with a seeded fallback for the current proof of concept.

```powerfx
SortByColumns(
    Filter(FormAssignments, UserEmail = gblUserEmail),
    "modifiedon",
    SortOrder.Descending
)
```

Assigned form display text:

```powerfx
Coalesce(
    LookUp(FormAssignments, UserEmail = gblUserEmail).FormVersion.Form.Name,
    "TACATDP MVP Field Visit"
) & " - " & Coalesce(
    LookUp(FormAssignments, UserEmail = gblUserEmail).FormVersion.'VersionCode',
    "2026-07-07-v1"
)
```

On select:

```powerfx
Set(gblAssignment, ThisItem);
Set(gblFormVersion, ThisItem.FormVersion);
Navigate(HistoryScreen, ScreenTransition.None);
```

## History screen

OnVisible:

```powerfx
Refresh(Submissions);
```

Gallery Items:

```powerfx
SortByColumns(
    Filter(Submissions, UserEmail = gblUserEmail && FormVersion.FormVersions = gblFormVersion.FormVersions),
    "modifiedon",
    SortOrder.Descending
)
```

New draft:

```powerfx
Set(
    gblSubmission,
    Patch(
        Submissions,
        Defaults(Submissions),
        {
            FormVersion: gblFormVersion,
            UserEmail: gblUserEmail,
            StartedAt: Now()
        }
    )
);
Navigate(RunnerScreen, ScreenTransition.None);
```

## Runner metadata load

The seeded MVP form has one section. To avoid Dataverse delegation warnings on lookup columns, the first slice loads small metadata tables into local collections, then filters locally by lookup primary id.

```powerfx
ClearCollect(colAllSections, Sections);
ClearCollect(colSections, SortByColumns(Filter(colAllSections, FormVersion.FormVersions = gblFormVersion.FormVersions), "mp_displayorder"));
Set(gblCurrentSection, First(colSections));
ClearCollect(colAllQuestions, Questions);
ClearCollect(colQuestions, SortByColumns(Filter(colAllQuestions, Section.Sections = gblCurrentSection.Sections), "mp_displayorder"));

ClearCollect(colRules, ValidationRules);
ClearCollect(colAllAnswers, SubmissionAnswers);
ClearCollect(colAnswers, Filter(colAllAnswers, Submission.Submissions = gblSubmission.Submissions));
RemoveIf(colPendingAnswers, true);
ClearCollect(colValidationErrors, FirstN(colQuestions, 0));
```

## Question renderer bindings

Use a vertical gallery bound directly to `SortByColumns(Filter(Questions, Section.Sections = gblCurrentSection.Sections), "mp_displayorder")`. Add visible controls by question type: text, integer, decimal, date, select one, select many, file/photo, and GPS. Save staged answers into `colPendingAnswers` as `{ Question: ThisItem, ValueText: ..., ValueNumber: ..., ValueJson: ... }`.

## Save draft

```powerfx
IfError(
    Set(gblSubmission, Patch(Submissions, gblSubmission, {UserEmail: gblUserEmail}));
    Patch(SubmissionAnswers, Coalesce(LookUp(SubmissionAnswers, Submission.Submissions = gblSubmission.Submissions && Question.Questions = LookUp(Questions, 'QuestionCode' = "farmer_name").Questions), Defaults(SubmissionAnswers)), {Submission: gblSubmission, Question: LookUp(Questions, 'QuestionCode' = "farmer_name"), ValueText: FarmerNameInput.Text});
    Patch(SubmissionAnswers, Coalesce(LookUp(SubmissionAnswers, Submission.Submissions = gblSubmission.Submissions && Question.Questions = LookUp(Questions, 'QuestionCode' = "farmer_age").Questions), Defaults(SubmissionAnswers)), {Submission: gblSubmission, Question: LookUp(Questions, 'QuestionCode' = "farmer_age"), ValueText: FarmerAgeInput.Text});
    Patch(SubmissionAnswers, Coalesce(LookUp(SubmissionAnswers, Submission.Submissions = gblSubmission.Submissions && Question.Questions = LookUp(Questions, 'QuestionCode' = "land_size_acres").Questions), Defaults(SubmissionAnswers)), {Submission: gblSubmission, Question: LookUp(Questions, 'QuestionCode' = "land_size_acres"), ValueText: LandSizeInput.Text});
    Patch(SubmissionAnswers, Coalesce(LookUp(SubmissionAnswers, Submission.Submissions = gblSubmission.Submissions && Question.Questions = LookUp(Questions, 'QuestionCode' = "visit_date").Questions), Defaults(SubmissionAnswers)), {Submission: gblSubmission, Question: LookUp(Questions, 'QuestionCode' = "visit_date"), ValueText: VisitDateInput.Text});
    Patch(SubmissionAnswers, Coalesce(LookUp(SubmissionAnswers, Submission.Submissions = gblSubmission.Submissions && Question.Questions = LookUp(Questions, 'QuestionCode' = "primary_crop").Questions), Defaults(SubmissionAnswers)), {Submission: gblSubmission, Question: LookUp(Questions, 'QuestionCode' = "primary_crop"), ValueText: PrimaryCropInput.Text});
    Patch(SubmissionAnswers, Coalesce(LookUp(SubmissionAnswers, Submission.Submissions = gblSubmission.Submissions && Question.Questions = LookUp(Questions, 'QuestionCode' = "support_needed").Questions), Defaults(SubmissionAnswers)), {Submission: gblSubmission, Question: LookUp(Questions, 'QuestionCode' = "support_needed"), ValueText: SupportNeededInput.Text});
    RemoveIf(colPendingAnswers, true);
    Notify("Draft saved.", NotificationType.Success),
    Notify("Draft could not be saved.", NotificationType.Error)
)
```

## Submit

```powerfx
// RunnerScreen.ReviewButton and RunnerScreen.RunnerNextButton
Set(gblReviewFarmerName, FarmerNameInput.Text);
Set(gblReviewFarmerAge, FarmerAgeInput.Text);
Set(gblReviewLandSize, LandSizeInput.Text);
Set(gblReviewVisitDate, VisitDateInput.Text);
Set(gblReviewPrimaryCrop, PrimaryCropInput.Text);
Set(gblReviewSupportNeeded, SupportNeededInput.Text);
Select(SaveDraftButton);
Navigate(ReviewScreen, ScreenTransition.None)

// ReviewScreen.ReviewSubmitButton
If(
    IsBlank(gblReviewFarmerName) || IsBlank(gblReviewVisitDate) || IsBlank(gblReviewPrimaryCrop),
    Notify("Complete farmer name, visit date, and primary crop before submitting.", NotificationType.Error);
    Navigate(RunnerScreen, ScreenTransition.None),
    IfError(
        Patch(Submissions, gblSubmission, {SubmittedAt: Now()});
        Notify("Submitted.", NotificationType.Success);
        Navigate(HistoryScreen, ScreenTransition.None),
        Notify("Submit failed.", NotificationType.Error)
    )
)
```

## Display mode

```powerfx
If(IsBlank(gblSubmission), DisplayMode.Disabled, DisplayMode.Edit)
```

Lock enforcement is deferred in the v3 package because the custom `Status` choice column is not binding consistently by display name after import.

## Attachment

Set `AttachmentScreen.OnVisible`:

```powerfx
Set(locAttachmentQuestion, LookUp(Questions, Section.Sections = gblCurrentSection.Sections && 'Type' = 'Type (Questions)'.file_photo_attachment));
```

The first slice uses a Dataverse edit form bound to `SubmissionFiles`. Keep the Attachments control inside that form. For the metadata stub, patch `Submission`, `Question`, `FileName`, and `MediaType`.

## GPS

```powerfx
Set(locGpsQuestion, LookUp(QuestionsGallery.AllItems, 'Type' = 'Type (Questions)'.gps));
If(
    !IsBlank(locGpsQuestion),
    Collect(
        colPendingAnswers,
        {
            Question: locGpsQuestion,
            ValueJson: JSON(
                {
                    latitude: Location.Latitude,
                    longitude: Location.Longitude,
                    altitude: Location.Altitude,
                    capturedAt: Text(Now(), DateTimeFormat.UTC)
                },
                JSONFormat.Compact
            )
        }
    );
    Notify("GPS captured.", NotificationType.Success),
    Notify("No GPS question on this form.", NotificationType.Information)
)
```

## MVP v3 status decision

The first two imports showed that the custom choice display name `Status` is not stable in Studio because Dataverse tables also have built-in state/status fields. For the July 7 MVP package, formulas no longer read or patch the custom `Status` columns. The runtime uses `StartedAt` and `SubmittedAt` for the demo path, and lock enforcement is deferred until the status column is renamed or Studio-normalized source reveals a stable column name.


## MVP v4 Runner fixes

The v4 package removes three remaining Runner blockers from the imported app:

- `Choices` table loading is removed because the downloaded app package did not contain a `Choices` data source binding. Reintroduce choice rendering after Studio adds that Dataverse table as a data source.
- GPS JSON uses only documented `Location` signal fields: `Latitude`, `Longitude`, and `Altitude`. Microsoft docs do not list `Location.Accuracy`.
- `SubmissionAnswers.ValueBoolean` is not patched in the MVP package because Studio imported the field as expecting an option-set-like value. Reintroduce boolean patching only after the imported data-source type is confirmed.
- Required validation checks whether an answer record exists instead of using `Coalesce` across mixed text, number, date, and JSON values.


## MVP v5 collection/date fixes

The v5 package removes the final reported Runner import errors:

- `Clear(...)` was removed from importable formulas. Microsoft documents that `Clear` operates only on collections. Generated imports can validate before a collection exists, so v5 initializes collections with `ClearCollect(...)` and empties staged rows with `RemoveIf(colPendingAnswers, true)`.
- `ValueDate` patching was removed until real date controls create a confirmed Date-typed staged answer field. The generated shell currently has no field renderer controls producing typed date values.


## MVP v6 literal-predicate warning fix

The v6 package replaces `Filter(colQuestions, false)` with `FirstN(colQuestions, 0)` in `RunnerScreen.OnVisible`. Microsoft documents `FirstN` as returning the first set of records from a table. Here it is applied only to an already-loaded local collection, so it creates an empty table without a literal `Filter` predicate and without adding a data-source delegation warning.


## v9 performance and data-source cleanup

The v9 package removes one-shot `ClearCollect` staging of whole Dataverse tables. History binds directly to a filtered `Submissions` query, runner selects the current section with a filtered `Sections` query, and the questions gallery binds directly to filtered `Questions`. This follows Microsoft delegation guidance: prefer delegable `Filter`/`LookUp` predicates and avoid nondelegable collection copies for tables that can grow.

Unused `Activities`, `Forms`, and `ValidationRules` package references are pruned from the generated `.msapp` because the MVP source formulas do not use those tables yet. `ValidationRules` remains in the Dataverse schema and roadmap, but the first renderer package validates required questions from the `Questions.Required` metadata field.


## MVP v13 wizard review slice

The v13 package adds a bottom `Next` button beside GPS and changes the shareable flow from direct runner submit to a wizard flow: Assigned Forms -> History/New Draft -> Runner -> Review -> Submit -> History. This matches the ODK/REDCap-style collector pattern for long forms: enter data, save draft, review, then submit.

Implementation constraints retained from prior imports:

- Use unversioned generated `Button` controls with minimal supported properties.
- Do not add `AccessibleLabel` or `TabIndex` to `Label@2.5.1`.
- Do not style generated buttons with rejected `Fill`, `Color`, hover, pressed, border, or align properties.
- Do not use `ForAll`, `Clear`, `ValueDate`, `ValueBoolean`, `Location.Accuracy`, or ambiguous `Status` formulas in the import package.
- Keep saved seeded answers as `SubmissionAnswers.ValueText` for the share candidate; typed storage is a post-share hardening task.

The visible seeded controls are still a pragmatic share candidate, not the final generic renderer. The next compound iteration should replace the hard-coded visible fields with a Studio-normalized reusable field row/component after this vertical slice is demoed.


## MVP v14 entry-screen design revision

The v14 package reorganizes the entry screen and app shell:

- every screen shows `Signed in as <gblUserEmail>` near the top;
- assignment status copy is user-neutral;
- the assigned-form open control shows both form display name and version code; and
- the package validator fails if the old `Assigned form found for <email>` pattern returns.
