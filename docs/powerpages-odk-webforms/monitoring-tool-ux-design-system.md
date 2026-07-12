# Monitoring Tool UX Design System

Date: 2026-07-11

## Product Name

Use **Monitoring Tool** in the user-facing shell. Avoid "Collector" because the product scope includes assigned forms, drafts, submissions, history, review status, and eventually monitoring operations.

## Design Goal

Deliver a CRDB-branded, mobile-first field monitoring experience that feels like a focused operational tool, not a prototype diagnostics page. The ODK Web Forms runtime remains the form engine; the host shell owns authentication state, navigation, project/form selection, loading, status, history, and submission feedback.

## Evidence Used

- Microsoft Power Pages authentication and `/_api` behavior govern login, contact/session state, table permissions, and CSRF-protected Dataverse access.
- ODK Collect organizes field work around projects/forms, drafts, ready-to-send/submitted states, form navigation, validation, and editing rules.
- ODK Web Forms should own the actual XForm rendering and validation surface.
- LIMS and STEMGEN show the reusable project pattern: semantic tokens, shared component recipes, explicit shell boundaries, task-focused pages, labeled back actions, and feature CSS only for narrow exceptions.
- TACATDP brand assets are available at `assets/images/CRDB_Bank_PLC.png` and `assets/images/CRDB_Bank_PLC.svg`.

## UX Principles

- Use Power Pages / Microsoft Entra authentication. Do not build custom login.
- If the user is unauthenticated, route to the Power Pages sign-in flow and return to the requested page after login.
- Keep one primary task per page state: choose work, fill form, review history, or inspect a submission.
- Show the signed-in user in the shell, but do not make the identity line the page headline.
- Use CRDB identity through tokens, logo placement, and restrained accent colors, not decorative backgrounds.
- Keep ODK runtime styling isolated. Do not target generic `button`, `input`, `label`, `select`, or `textarea` inside the ODK host.
- Move developer diagnostics behind a collapsible debug panel or development flag before sharing.
- Preserve clear status states: loading, empty, ready, saving draft, submitting, submitted, failed, offline/pending.

## Screen Model

### Unauthenticated

- Present a compact CRDB-branded sign-in panel only if automatic redirect is not possible.
- Primary action: "Sign in with Microsoft".
- Login must use the configured Power Pages / Microsoft Entra provider.

### Home / Work Queue

Show the user what they can do now:

- CRDB logo and product name: **Monitoring Tool**.
- Signed-in user name/email in the top shell area.
- Project list or current project summary.
- Assigned forms count.
- Local drafts count.
- Recent submitted count.
- Offline/sync status once offline sync is introduced.

For the current single-project MVP, use the same project-first pattern that will scale later: Home shows project cards only. Opening a project shows the project CRUD workspace.

### Project Detail

- Top action bar with icon+text Back, project name, online/offline state, and icon+text Add new.
- Sections:
  - Saved records.
  - Local drafts.
- Use peer tabs for Saved and Drafts because both represent record lists inside the same project workspace.
- Saved records are shared across authenticated users for this proof. Do not filter saved submitted records by the current user's email unless a future role/permission requirement explicitly changes the scope.
- Place search at the end of the Saved/Drafts toolbar. Search must filter as the user types across the loaded saved/draft records.
- Show data cards 10 per page. Cards must expose record identity, owner when known, status, updated time, and an icon+text Edit action for saved submitted records.
- The active card/list pattern should look like normal CRUD, not a survey launcher or diagnostics page.
- Cards and action areas use a restrained CRDB left accent strip. State text must be visible; do not communicate state by color alone.
- Use **Open** for existing work and **Add new** for new submissions. Avoid "Start" in the project/data list shell.
- Use **Edit** for submitted saved records. Edit must load the latest submitted instance into ODK Web Forms edit mode and save a new submission version for the same ODK instance id.
- Draft cards must represent restorable ODK instance state. Do not display runtime-load markers as drafts because opening them creates an empty form and teaches the wrong workflow.

### Form Loading

Use a reusable centered loading panel:

- CRDB logo.
- "Loading form".
- Form name and version when known.
- Loading dots or progress indicator.
- Optional secondary line: "Preparing the secure form session".

This same loading panel should be reused for page-level loading, assignment loading, form version loading, and submit transitions.

### Form Runner

- Top action bar with Back to project, form name, version, save/draft status, and submit state.
- ODK Web Forms gets the full main form area below the action bar.
- Host shell must provide spacing before and after the ODK runtime.
- Submit shows a blocking CRDB-branded progress panel with the CRDB logo, "Submitting record", "Saving to Dataverse", and animated dots. Do not leave users wondering whether a submit click was accepted.
- Successful submit returns to the project data-card list on the Saved tab and displays the submit result as a status banner. Failed submit stays on the form runner and keeps the error visible there.
- Attachment binary warnings should be visible but not framed as a total failure when submission and metadata persistence succeeded.

### History

- Show only the signed-in user's submissions unless an admin role is explicitly added later.
- List form name, version, submission time, lifecycle, review state, attachment count, and sync/file warning state.
- Submission detail can show canonical instance id and payload metadata for support, but not as the default first thing a field user sees.

## Component Inventory

- `AppShell`: CRDB brand header, user area, page container, status slot.
- `TopActionBar`: labeled Back, page title/subtitle, right-side actions.
- `LoadingPanel`: centered CRDB logo, loading message, animated dots/progress.
- `ProjectCard`: project name, active forms, drafts, recent submissions.
- `DataCard`: saved submission or local draft identity, status, updated time, Open action, and CRDB left accent.
- `RecordTabs`: Saved and Drafts tabs with counts.
- `PaginationBar`: Previous/Next controls for 10 records per page.
- `StatusBanner`: success/warning/error/offline states with `aria-live`.
- `DebugPanel`: collapsible diagnostics gated away from normal user flow.
- `OdkRuntimeBoundary`: the only host that contains ODK Web Forms; CSS must remain scoped.

## Token Direction

Create TACATDP tokens under the SPA CSS before further UI work:

- Typography: system UI/Segoe UI for shell; preserve ODK runtime typography inside the ODK boundary.
- Spacing: 4, 8, 12, 16, 20, 24, 32.
- Radius: 4 for compact controls, 8 for cards/panels.
- CRDB brand: derive primary/accent values from `CRDB_Bank_PLC.svg` and verify contrast.
- Neutrals: white surfaces over a muted off-white/green-tinted page background.
- Focus: visible focus rings on buttons, cards, form-list rows, and top-bar actions.

## Implementation Instructions

Before improving the UI:

1. Inspect this document, `requirements.md`, `delivery-plan.md`, `slice-checklist.md`, `powerpages/webforms-spa/src/views/AssignedFormsView.vue`, and `powerpages/webforms-spa/src/styles.css`.
2. Inspect CRDB assets in `assets/images/`.
3. Compare reusable patterns from LIMS `docs/UX_DESIGN_SYSTEM.md` and STEMGEN UI tokens/components before inventing a new component rule.
4. Before UI work, write down the expected behavior, data visibility scope, loaded-record limit/pagination, search fields, empty/error states, and what each primary action does. If any of these are unclear, stop and clarify before implementing.
5. Create or update shared shell components/tokens first; avoid page-local styling.
6. Keep ODK Web Forms in `OdkRuntimeBoundary` and verify host CSS does not style ODK controls except for explicitly documented host boundary spacing/footer adjustments.
7. Keep icon+text action controls for Back, Refresh, Add new, Open, and Edit.
8. Use the maintained `@lucide/vue` package for shell icons. Back uses `ArrowLeft`; Open uses `FolderOpen`; Edit uses `Pencil`; Add new uses `Plus`; Refresh uses `RefreshCw`; Saved uses `Database`; Drafts uses `FilePenLine`; Search uses `Search`. Do not use text glyphs such as `<`, `>`, `R`, `S`, `D`, or `+` as icons.
9. Build and visually check both mobile and desktop widths before upload.

## Acceptance Criteria

- User-facing text says **Monitoring Tool**.
- Unauthenticated users are sent to Microsoft/Power Pages login.
- Authenticated users land on a work queue, not a prototype diagnostic page.
- Authenticated users first see project cards.
- Project detail shows Saved and Drafts tabs, 10 cards per page, search at the end of the toolbar, Edit actions for saved records, and Add new in the top action bar.
- Saved records include all submitted records readable by the authenticated user, not only records owned by that user's email.
- Drafts tab does not show stale runtime-load markers as editable drafts.
- Loading uses the CRDB branded `LoadingPanel`.
- Submit uses the CRDB branded blocking progress panel and returns to the Saved data-card list after success.
- The form runner has a top action bar and a full-width ODK runtime area.
- Prototype diagnostics are hidden behind a debug panel.
- Mobile view is readable without forcing a tablet layout.
- Shell CSS is tokenized and does not broadly restyle ODK controls.

## References

- ODK Collect form management and drafts: https://docs.getodk.org/collect-forms/
- ODK Collect form navigation: https://docs.getodk.org/collect-filling-forms/
- ODK form logic: https://docs.getodk.org/form-logic/
- ODK Web Forms: https://docs.getodk.org/web-forms-intro/
- Power Pages Web API: https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview
