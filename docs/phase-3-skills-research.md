# Phase 3 Skills Research

## Task focus

Phase 3 moves from schema design to Power Apps canvas app architecture. The work needs skills for Power Platform architecture, Microsoft Lists integration, Power Fx validation/skip logic, UX design, and delivery governance.

## Useful existing Karakana skills

| Skill | Use in Phase 3 |
| --- | --- |
| `requirements-elicitation` | Keep Phase 3 requirements grounded in the XLSForm inventory, schema mapping, and user decisions. |
| `design-system-governance` | Ensure the app has a reusable UI contract instead of page-local styling or inconsistent screens. |
| `delivery-artifact-gate` | Check that requirements, design, schema, verification, and handoff artifacts exist before implementation. |
| `karakana-handoff` | Preserve current context between bounded work sessions. |
| `github-pr-review` | Review generated app/source/schema changes before integration. |

## Skill gap found

Karakana did not have a focused skill for Microsoft Power Apps canvas app architecture, Microsoft Lists/SharePoint connector constraints, Power Fx formulas, or XLSForm-to-Power Apps conversion.

## Skillset update

Added `skills/power-platform-canvas-apps/SKILL.md` in the Karakana repository and registered it in `skillpacks/karakana.yml` as an optional skill.

The new skill covers:

- Microsoft Lists/SharePoint connector delegation.
- Typed schema and reference-list design.
- XLSForm `required`, `relevant`, `constraint`, choice, and calculation semantics.
- Power Fx validation and save orchestration.
- Power Apps modern controls, Fluent UI, and Material-inspired form UX principles.
- Safety rules for SharePoint writes, app import/publish, permissions, and secrets.

## Recommended Phase 3 skill stack

Use these together for TACATDP Phase 3:

1. `power-platform-canvas-apps` for platform architecture and Power Fx/Microsoft Lists decisions.
2. `design-system-governance` for app shell, reusable components, form surfaces, validation, spacing, and accessibility.
3. `requirements-elicitation` for acceptance criteria and decision tracking.
4. `delivery-artifact-gate` before implementation starts.
5. `karakana-handoff` at task boundaries.

## Milestone 1 skill use

Milestone 1 will use placeholders while the controlled Windows environment is prepared for Microsoft Lists creation. This makes `design-system-governance` especially important because placeholder screens must not become throwaway layouts. The app shell, section progress, field wrapper, validation summary, and command bar should be defined as reusable design-system components from the start.

The `power-platform-canvas-apps` skill remains necessary even without live Lists because placeholder collections must be shaped to swap cleanly to Microsoft Lists later.
