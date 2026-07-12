# Power Pages ODK Web Forms MVP Requirements

## Goal

Deliver a Microsoft-managed ODK-style proof that runs inside Power Pages, renders one XForm-backed form, supports authenticated assigned users, submits to Dataverse, and handles attachment metadata while binary persistence and editable local draft restore are resolved through later managed-Microsoft slices.

## Functional Requirements

- Authenticate through Power Pages. Do not build custom login.
- Use **Monitoring Tool** as the user-facing product name.
- Route unauthenticated users through the Power Pages / Microsoft Entra sign-in flow.
- Show assigned published forms for the signed-in user when creating a new record.
- Present assigned work through a mobile-first CRUD workspace: project cards first, then project-level saved/draft data cards.
- Project detail must show Saved and Drafts tabs, 10 data cards per page, Open actions for existing records, and an Add new action for new submissions.
- Saved records are a shared authenticated-user worklist. Any logged-in user with the Power Pages authenticated role can see all submitted `Submissions` returned by table permissions; the saved list must not filter by the signed-in user's email.
- The Saved/Drafts toolbar must include a search input at the end. Search runs as the user types across the loaded records by instance id, owner email, form metadata, status, version, and timestamp.
- Load the selected `FormVersions.XFormXml`.
- Render the form through ODK Web Forms / XForms engine.
- Editing a saved submitted record must use ODK Web Forms `editInstance` with the latest `SubmissionVersions.XFormSubmissionXml`, then submit a new version for the same ODK `instanceID`.
- Do not create a local draft just because the ODK runtime loaded. Draft cards must represent restorable instance state, not runtime markers.
- Save and restore editable local draft state in IndexedDB only after the implementation captures ODK instance XML/state and can restore it into the runtime.
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
- Primary shell actions must use Lucide Vue icon+text buttons and the user-facing shell must use "Open" for projects and "Edit" for saved submitted records. Back uses a left-arrow icon, not a text `<` glyph; Open/Edit actions use semantic icons, not text `>` glyphs.
- The ODK runtime must remain isolated from broad host CSS. Host styling may provide spacing and documented footer/label adjustments only.
- Prototype diagnostics must be hidden behind a developer/debug panel before sharing the MVP.
- Offline support remains a staged requirement. The current shareable proof must not misrepresent runtime-load markers as drafts; editable local draft save/restore and offline submit sync can be introduced after the online submit path is stable.
- Attachment binary persistence must be verified against the hosted Power Pages origin because Microsoft documents Power Pages Web API as a CRUD subset with JSON requests, while Dataverse file-column binary uploads are documented on the Dataverse Web API file-column route.
- Before future UX-impacting work, document the expected behavior, data visibility scope, loaded-record limit/pagination, empty states, and edit/save semantics before implementation. Do not infer per-user versus shared data scope from the current screen.
