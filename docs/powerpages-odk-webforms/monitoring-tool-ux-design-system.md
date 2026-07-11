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

For the current single-project MVP, it is acceptable to show one project card and the assigned forms below it, but keep the project concept in the component model.

### Project Detail

- Top action bar with labeled Back action, project name, user/session status, and Refresh.
- Sections:
  - Assigned forms.
  - Drafts.
  - Recent submissions/history.
- Form cards must show form name, version, assignment status, and last local/server activity.

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
- Submit result should be a concise status region near the top or bottom of the host shell, not mixed into the assignment selector.
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
- `FormCard`: form name, version, assignment status, draft/submission summary, Start/Continue action.
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
4. Create or update shared shell components/tokens first; avoid page-local styling.
5. Keep ODK Web Forms in `OdkRuntimeBoundary` and verify host CSS does not style ODK controls except for explicitly documented host boundary spacing/footer adjustments.
6. Build and visually check both mobile and desktop widths before upload.

## Acceptance Criteria

- User-facing text says **Monitoring Tool**.
- Unauthenticated users are sent to Microsoft/Power Pages login.
- Authenticated users land on a work queue, not a prototype diagnostic page.
- Form cards show form name and version.
- Loading uses the CRDB branded `LoadingPanel`.
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
