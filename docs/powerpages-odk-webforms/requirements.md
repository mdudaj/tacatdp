# Power Pages ODK Web Forms MVP Requirements

## Goal

Deliver a Microsoft-managed ODK-style proof that runs inside Power Pages, renders one XForm-backed form, supports authenticated assigned users, saves local drafts, submits to Dataverse, and uploads one attachment.

## Functional Requirements

- Authenticate through Power Pages. Do not build custom login.
- Show assigned published forms for the signed-in user.
- Load the selected `FormVersions.XFormXml`.
- Render the form through ODK Web Forms / XForms engine.
- Save local draft state in IndexedDB.
- Restore local draft state after browser refresh or reconnect.
- Submit online to Dataverse through Power Pages `/_api`.
- Create one `Submissions` header and one current `SubmissionVersions` payload.
- Upload at least one file/photo as `SubmissionAttachments`.
- Show user's submission history for the selected form.

## Non-Functional Requirements

- The SPA must not store secrets or Dataverse credentials.
- All Dataverse browser writes must go through Power Pages auth, table permissions, and CSRF token handling.
- The app must be mobile-first and usable on phone width.
- Offline support for MVP means local draft save/restore; offline submit sync can be introduced after the first online submit path works.
