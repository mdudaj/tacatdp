# Power Pages ODK Web Forms MVP Requirements

## Goal

Deliver a Microsoft-managed ODK-style proof that runs inside Power Pages, renders one XForm-backed form, supports authenticated assigned users, saves local drafts, submits to Dataverse, and handles attachment metadata while binary persistence is resolved through a Microsoft-managed path.

## Functional Requirements

- Authenticate through Power Pages. Do not build custom login.
- Use **Monitoring Tool** as the user-facing product name.
- Route unauthenticated users through the Power Pages / Microsoft Entra sign-in flow.
- Show assigned published forms for the signed-in user.
- Present assigned work through a mobile-first work queue with project/form cards, not a prototype diagnostics-first page.
- Load the selected `FormVersions.XFormXml`.
- Render the form through ODK Web Forms / XForms engine.
- Save local draft state in IndexedDB.
- Restore local draft state after browser refresh or reconnect.
- Submit online to Dataverse through Power Pages `/_api`.
- Create one `Submissions` header and one current `SubmissionVersions` payload.
- Persist at least one file/photo as a `SubmissionAttachments` metadata row linked to the submitted version.
- Attempt browser binary upload to the Dataverse file column only through Power Pages `/_api`; do not add raw Dataverse credentials, direct OAuth, or external storage. If the hosted browser route fails, keep metadata persistence and report binary storage as a pending managed-Microsoft slice.
- Show user's submission history for the selected form.

## Non-Functional Requirements

- The SPA must not store secrets or Dataverse credentials.
- All Dataverse browser writes must go through Power Pages auth, table permissions, and CSRF token handling.
- The app must be mobile-first and usable on phone width.
- The shell must use CRDB-branded tokens and reusable components documented in `monitoring-tool-ux-design-system.md`.
- The ODK runtime must remain isolated from broad host CSS. Host styling may provide spacing and documented footer/label adjustments only.
- Prototype diagnostics must be hidden behind a developer/debug panel before sharing the MVP.
- Offline support for MVP means local draft save/restore; offline submit sync can be introduced after the first online submit path works.
- Attachment binary persistence must be verified against the hosted Power Pages origin because Microsoft documents Power Pages Web API as a CRUD subset with JSON requests, while Dataverse file-column binary uploads are documented on the Dataverse Web API file-column route.
