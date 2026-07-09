# TACATDP Canvas MVP Design System

## Evidence

- Microsoft Power Apps accessibility guidance requires clear labels, logical top-to-bottom flow, keyboard-accessible interactive controls, and accessibility checking in Studio.
- Microsoft Power Apps responsive design guidance recommends planning supported form factors and using responsive layout principles so the app works across phones, tablets, laptops, and desktops.
- The current Source Code import path has rejected several otherwise valid accessibility/style properties on generated YAML controls, so this MVP design system uses only properties proven by the package validator and Studio import history.

## App shell

Every MVP screen uses the same top structure:

1. Command/title row at `Y = 20`.
2. Signed-in user row at `Y = 68` with text `Signed in as <gblUserEmail>`.
3. Screen content begins below the identity row.

Do not put the user email inside state messages such as `Assigned form found for <email>`. State messages must describe the screen state, while the header owns identity.

## Assigned forms

Assigned form rows/cards must show both:

- form display name from `Forms.Name` through the selected `FormVersion.Form` lookup where Studio resolves it; and
- `FormVersions.VersionCode`.

For the share candidate, keep a seeded fallback of `TACATDP MVP Field Visit - 2026-07-07-v1` so the POC remains readable if lookup expansion is limited in imported source.

## Generated YAML constraints

Keep generated buttons minimal: `AccessibleLabel`, `Text`, `OnSelect`, `DisplayMode`, `X`, `Y`, `Width`, and `Height`. Do not add generated button style properties that Studio has already rejected.

Do not add `AccessibleLabel`, `TabIndex`, or `Role` to `Label@2.5.1` in generated source. Apply richer heading semantics in Studio after import if Studio-normalized source supports them.

## Verification

Run:

```bash
python3 scripts/validate-canvas-renderer-slice.py
```

Then import/open the package in Power Apps Studio, run App Checker, and smoke-test: assigned form -> new draft -> save -> next -> review -> submit -> history.


## Phone layout

Microsoft responsive canvas app guidance says responsive apps should disable Scale to fit, Lock aspect ratio, and Lock orientation in Settings > Display. The generated MVP package must keep `DocumentLayoutScaleToFit = false`, `DocumentLayoutMaintainAspectRatio = false`, and `DocumentLayoutLockOrientation = false` so phones use their available screen width instead of forcing the tablet canvas shape.
