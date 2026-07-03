# Dataverse Import Order: Multi-Project Monitoring Platform

Generated review artifact for TACATDP. This document does not authorize or perform environment writes.

## Scope

- Source model: `docs/multi-project-monitoring/data-model.md`
- Field source: `docs/xlsform-field-inventory.csv` and `schemas/xlsform-to-list-mapping.csv`
- Vocabulary source: `schemas/reference-data/*.csv`
- Platform publisher prefix placeholder: `mp`
- TACATDP project code: `tacatdp`

## Recommended create/import sequence

1. Create the Power Platform solution and publisher after approval; replace the placeholder `mp` prefix only if the approved publisher prefix differs.
2. Create project/governance tables from `platform-tables.json` and `platform-columns.csv`.
3. Create instrument metadata tables and relationships: `mp_Instrument`, `mp_InstrumentVersion`, `mp_EventDefinition`, `mp_InstrumentEventBinding`, `mp_GroupDefinition`, `mp_FieldDefinition`, `mp_FieldRule`.
4. Create controlled vocabulary tables and relationships: `mp_VocabularyScheme`, `mp_VocabularyTerm`, `mp_VocabularyTermLabel`, `mp_VocabularyTermRelation`, `mp_ProjectVocabularyBinding`, `mp_FieldVocabularyBinding`, `mp_ExternalAuthorityIdentifier`.
5. Create runtime tables and relationships: `mp_TrackedEntity`, `mp_EntityIdentifier`, `mp_Encounter`, `mp_Submission`, `mp_GroupInstance`, `mp_AnswerValue`, `mp_MultiSelectAnswer`, `mp_Attachment`, `mp_SubmissionReview`, `mp_AuditEvent`.
6. Create projection/export tables: `mp_ExportProfile`, `mp_ExportColumn`.
7. Add alternate keys from `platform-alternate-keys.csv` after referenced columns exist.
8. Import seed records in this order: `mp_Project`, `mp_Instrument`, `mp_InstrumentVersion`, `mp_EventDefinition`, `mp_GroupDefinition`, `mp_VocabularyScheme`, `mp_VocabularyTerm`, `mp_VocabularyTermLabel`, `mp_FieldDefinition`, `mp_FieldRule`, vocabulary bindings, and project bindings.
9. Import TACATDP metadata from `tacatdp-field-definitions.csv` and `tacatdp-vocabulary-terms.csv` only after the generated rows are reviewed.
10. Bind the Canvas app only after the reviewed dev Dataverse schema exists.

## Review checks before environment writes

- Confirm publisher prefix and solution name.
- Confirm whether TACATDP screen groups should be generated from `source_screen` or from old save-target projections for fields with no screen match.
- Confirm large reference vocabularies, especially villages (66297 rows), should live in Dataverse as terms or in a dedicated reference table with the same vocabulary API contract.
- Confirm field-level requiredness remains app-visible-only; `required_in_dataverse` is intentionally `no` for imported TACATDP fields.
- Confirm alternate keys do not exceed Dataverse key constraints in the target environment.

## Generated artifact inventory

- `platform-tables.json`: 29 platform tables.
- `platform-columns.csv`: 160 platform columns.
- `platform-relationships.csv`: 45 relationships.
- `platform-alternate-keys.csv`: 21 alternate keys.
- `tacatdp-field-definitions.csv`: 292 TACATDP field definitions.
- `tacatdp-vocabulary-terms.csv`: 71487 TACATDP vocabulary terms.
