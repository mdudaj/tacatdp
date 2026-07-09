# Power Pages ODK Web Forms User Stories

## Scope

These stories govern the Power Pages ODK Web Forms MVP. They map to the accepted architecture in `adr-0002-power-pages-odk-webforms.md` and the requirements in `requirements.md`.

## Personas

- Field user: signs in through Power Pages and fills assigned monitoring forms on a phone.
- Project monitor: reviews submitted records and attachment presence.
- Platform maintainer: publishes form versions, configures assignments, and verifies Power Pages/Dataverse access.

## Stories

### PP-ODK-001 Authentication

As a field user, I want to use Power Pages authentication so that I do not manage a separate TACATDP login.

Acceptance:

- The SPA does not implement custom credentials.
- Browser code does not contain secrets, OAuth client secrets, bearer tokens, or raw Dataverse OAuth endpoints.
- Dataverse access goes through Power Pages `/_api` and table permissions.

### PP-ODK-002 Assigned Forms

As a field user, I want to see forms assigned to me so that I only fill relevant instruments.

Acceptance:

- The app reads `FormAssignments` through `/_api/mp_formassignments`.
- Each listed item shows form name, form version, and assignment key.
- Empty state is explicit when no assignments are returned.

### PP-ODK-003 Load Published XForm

As a field user, I want the selected form version to load its XForm XML so that the runtime can render the current published instrument.

Acceptance:

- The app reads `FormVersions.XFormXml` through `/_api/mp_formversions`.
- The app resolves parent `Forms` metadata through `/_api/mp_forms`.
- The XForm XML remains source-of-truth; decomposed answer rows are not required for the runtime.

### PP-ODK-004 Local Draft

As a field user, I want my partially completed form to survive refresh or connection loss so that I can continue data capture.

Acceptance:

- Draft state is stored in IndexedDB or equivalent browser-local storage.
- Draft keys include assignment/form version and user context.
- Draft restore is explicit and does not submit data automatically.

### PP-ODK-005 Online Submit

As a field user, I want to submit a finalized form online so that Dataverse receives the submission.

Acceptance:

- Submit uses Power Pages `/_api`, not raw Dataverse Web API.
- Mutating requests include the Power Pages anti-forgery token.
- Submit creates one `Submissions` header and one current `SubmissionVersions` payload.

### PP-ODK-006 Attachment

As a field user, I want to attach one photo or file so that supporting evidence is linked to my submission.

Acceptance:

- The attachment is linked to the submission version.
- Metadata includes filename and media type.
- Attachment upload does not store credentials in browser code.

### PP-ODK-007 History

As a field user, I want to see my prior submissions for the selected form so that I can confirm what I sent.

Acceptance:

- History uses `Submissions` and `SubmissionVersions`.
- Locked/submitted state is visible when available.
- The list is scoped by the current user or assignment model.

## Traceability

| Story | Requirement | First verification gate |
| --- | --- | --- |
| PP-ODK-001 | Authenticate through Power Pages | `validate-webforms-spa-foundation.py`, hosted smoke verifier |
| PP-ODK-002 | Show assigned published forms | SPA foundation API client and hosted seed checks |
| PP-ODK-003 | Load selected XForm XML | API client and next ODK shell slice |
| PP-ODK-004 | Save/restore local draft | IndexedDB adapter tests in draft slice |
| PP-ODK-005 | Submit online to Dataverse | Submission slice with CSRF token handling |
| PP-ODK-006 | Upload one attachment | Attachment slice |
| PP-ODK-007 | Show submission history | History slice |
