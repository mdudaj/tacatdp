# Delivery Plan: July 7 Metadata-Driven MVP Slice

## Step 1: Confirm access

Already validated enough to proceed:

- service-principal auth works;
- `pac solution list` works;
- `pac org who` works.

## Step 2: Prepare MVP Dataverse solution

After explicit dev-write approval, create only the MVP tables:

- `Forms`;
- `FormVersions`;
- `Sections`;
- `Questions`;
- `Choices`;
- `ValidationRules`;
- `FormAssignments`;
- `Submissions`;
- `SubmissionAnswers`;
- `SubmissionFiles`.

## Step 3: Seed one published form

Seed a small TACATDP form definition manually or from JSON/YAML:

1. one form;
2. one published form version;
3. two or three sections;
4. representative supported field types;
5. choices for one select-one and one select-many question;
6. one file/photo question;
7. simple required/relevance/constraint rules;
8. one assignment for the test user.

## Step 4: Build assigned forms and history

Canvas screens:

1. assigned forms list filtered by current user/email and active published version;
2. selected form history showing the user's own `Draft`, `Submitted`, and `Locked` submissions.

## Step 5: Build form runner

Render sections/questions from metadata. Support:

- text;
- integer;
- decimal;
- date;
- select one;
- select many;
- file/photo attachment;
- GPS only if quick after the core controls work.

## Step 6: Build save/submit/edit behavior

1. Save Draft creates/updates `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`.
2. Submit changes status to `Submitted`.
3. Draft and Submitted remain editable.
4. Locked is read-only.

## Step 7: Verify vertical slice

Verify one user can:

1. authenticate through Power Apps/Entra;
2. see one assigned form;
3. open the form;
4. capture supported fields;
5. attach one file/photo;
6. save draft;
7. reopen from history;
8. submit;
9. edit until locked;
10. see locked read-only behavior.

## Deferred implementation

Do not implement these in the July 7 slice unless explicitly re-approved:

- full XLSForm compiler;
- repeat groups;
- nested repeats;
- complex XPath;
- offline-first sync;
- barcode;
- admin publishing UI;
- dashboards;
- version migration.
