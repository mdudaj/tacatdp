# Requirements Traceability: Dataverse-First Pivot

## Scope

Trace Dataverse-first requirements for TACATDP backend planning.

## Artifact links

- Research: `docs/dataverse-first/research.md`
- Requirements note: `docs/dataverse-first/requirements-note.md`
- PRD: `docs/dataverse-first/product-requirements-document.md`
- User stories: `docs/dataverse-first/user-stories.md`
- Acceptance criteria: `docs/dataverse-first/acceptance-criteria.md`
- Readiness: `docs/dataverse-first/artifact-readiness.md`
- Definition of done: `docs/dataverse-first/definition-of-done.md`
- Delivery plan: `docs/dataverse-first/delivery-plan.md`
- Verification: `docs/dataverse-first/verification-summary.md`

## Matrix

| Requirement | Story | Acceptance criteria | Implementation surface | Verification |
| --- | --- | --- | --- | --- |
| DV-RQ-01 Dataverse primary backend | DV-US-01 | AC-01 | Docs, schema generator, app data sources | Docs review |
| DV-RQ-02 Solution packaging | DV-US-07 | AC-08 | Power Platform solution | Maker/admin review |
| DV-RQ-03 Submission parent | DV-US-02 | AC-03, AC-04 | Generic `Submission` table with project/instrument/entity/encounter context | Schema review |
| DV-RQ-04 Generic group/answer model | DV-US-03 | AC-02, AC-03 | `GroupDefinition`, `GroupInstance`, `FieldDefinition`, `AnswerValue` | Mapping coverage check |
| DV-RQ-05 Multi-select rows | DV-US-04 | AC-05 | Generic `MultiSelectAnswer` linked to field and vocabulary term | Mapping coverage check |
| DV-RQ-06 Production cost repeat/line model | DV-US-05 | AC-06 | Repeat group instances and answer rows; optional projection | Mapping coverage check |
| DV-RQ-07 Controlled/reference vocabularies | DV-US-06 | AC-07 | `VocabularyScheme`, `VocabularyTerm`, bindings, labels | Delegation review |
| DV-RQ-08 Alternate keys | DV-US-02, DV-US-07 | AC-04 | Dataverse alternate keys | Schema review |
| DV-RQ-09 Delegable filters | DV-US-06 | AC-07 | ComboBox/filter formulas | App Checker |
| DV-RQ-10 Update validation/save-map | DV-US-01, DV-US-03 | AC-02, AC-09 | Existing validation/save docs | Docs diff review |

## Gaps

| Gap | Impact | Next action |
| --- | --- | --- |
| No generated multi-project Dataverse schema artifact yet. | Implementation cannot safely create tables. | Add schema generator or manual table design artifact next. |
| No confirmed publisher prefix. | Solution/table naming could change. | Choose publisher/prefix before generation. |
| No confirmed production licensing. | Production deployment path may differ. | Record license/admin constraints before production plan. |
| No Dataverse App Checker evidence. | Delegation risks remain untested. | Validate in Power Apps Studio after data sources are connected. |
