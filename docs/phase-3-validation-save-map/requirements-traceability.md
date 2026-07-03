# Requirements Traceability: Phase 3 Validation and Save Map

## Scope

Trace requirements for the TACATDP Phase 3 screen-by-screen validation and save-map slice. This is pre-implementation artifact work for the ordered native-control Canvas app source.

## Artifact links

- PRD: `docs/phase-3-validation-save-map/product-requirements-document.md`
- Requirements note: `docs/phase-3-validation-save-map/requirements-note.md`
- User stories: `docs/phase-3-validation-save-map/user-stories.md`
- Acceptance criteria: `docs/phase-3-validation-save-map/acceptance-criteria.md`
- Readiness: `docs/phase-3-validation-save-map/artifact-readiness.md`
- Definition of done: `docs/phase-3-validation-save-map/definition-of-done.md`
- Verification summary: `docs/phase-3-validation-save-map/verification-summary.md`
- UX source: `docs/design-system.md`
- Architecture source: `docs/phase-3-requirements.md`, `docs/phase-3-delivery-plan.md`
- Schema/data source: `schemas/xlsform-to-list-mapping.csv`, `schemas/sharepoint-lists-schema.json`

## Traceability matrix

| Requirement ID | Source evidence | User story | Acceptance criteria | UX / architecture / data artifact | Implementation surface | Test / eval | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VSM-RQ-01 | `summary.json`, `Screen_*.pa.yaml` | VSM-US-01 | AC-01, AC-02 | PRD screen map | 33 screen `OnSelect`/validation formulas | Manual screen validation checklist | Ready for implementation |
| VSM-RQ-02 | `docs/phase-3-requirements.md` | VSM-US-01 | AC-03 | Requirements note | Field visibility and required formulas | Hidden-required-field scenario | Ready for implementation |
| VSM-RQ-03 | `docs/design-system.md` | VSM-US-02 | AC-02 | Design system | Field row helper/error controls | UX review and accessibility checklist | Ready for implementation |
| VSM-RQ-04 | `docs/design-system.md`, runbook | VSM-US-01, VSM-US-06 | AC-02, AC-10 | Validation summary rule | Section validation summary collection/control | Blocked Continue and final review scenario | Ready for implementation |
| VSM-RQ-05 | `docs/milestone-1-placeholder-plan.md` | VSM-US-03 | AC-04, AC-05 | Placeholder strategy | `colPlaceholder*` collections | Save Draft success/failure scenario | Ready for placeholder implementation |
| VSM-RQ-06 | `schemas/sharepoint-lists-schema.json` | VSM-US-03, VSM-US-04 | AC-04, AC-07 | Data schema | Parent and child save payloads | Schema shape inspection | Ready for implementation |
| VSM-RQ-07 | `schemas/xlsform-to-list-mapping.csv` | VSM-US-04 | AC-06 | Save map | Multi-select save routine | Multi-select child-row scenario | Ready for implementation |
| VSM-RQ-08 | `schemas/xlsform-to-list-mapping.csv` | VSM-US-04 | AC-07 | Save map | Production cost line save routine | Add/edit production cost detail scenario | Ready for implementation |
| VSM-RQ-09 | Mapping and list schema files | VSM-US-04 | AC-01, AC-04 | Save map table | Section Patch/Collect payloads | Internal-name mapping review | Ready for implementation |
| VSM-RQ-10 | Power Platform skill, requirements | VSM-US-04 | AC-10 | Reference data strategy | ComboBox/reference filters | Delegation warning review | Needs Studio/App Checker evidence later |
| VSM-RQ-11 | `summary.json`, ordered source | VSM-US-02 | AC-08 | ODK metadata rule | Screen source and generated scaffolds | Search for visible metadata labels | Ready for implementation |
| VSM-RQ-12 | `docs/powerapps-import-recovery.md` | VSM-US-07 | AC-09 | Import recovery doc | Pack/open workflow | Windows Studio import/open test | Needs authorized environment later |

## Gaps

| Gap | Impact | Owner / next action |
| --- | --- | --- |
| Ordered screen branch is not merged into `main`. | Future implementation may accidentally start from old screen order. | Confirm PR/squash merge before source edits. |
| App Checker and Studio import cannot be run from this Linux session. | Import/open verification remains manual in authorized environment. | Maker runs Studio checks on authorized Windows laptop. |
| Final SharePoint site/list connection names are not approved. | Implementation must remain placeholder-first. | Confirm environment details before live connector wiring. |
| Offline behavior beyond draft state is not defined. | Offline sync should not be assumed. | Capture explicit offline requirements before implementing sync. |

## Review notes

The validation/save-map artifacts are sufficient to start a placeholder implementation slice after branch state is resolved. They are not sufficient to perform production SharePoint writes or publish/import an app without separate approval and Studio verification.

