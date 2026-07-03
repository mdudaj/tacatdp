# Dataverse Import Order: Multi-Project Monitoring Platform

Generated review artifact for TACATDP. This document does not authorize or perform environment writes.

## Scope

- Source model: `docs/multi-project-monitoring/data-model.md`
- Field source: `docs/xlsform-field-inventory.csv` and `schemas/xlsform-to-list-mapping.csv`
- Vocabulary source: `schemas/reference-data/*.csv`
- High-volume village source: `schemas/reference-data/TACATDP_RefVillages.csv`
- Platform publisher prefix placeholder: `mp`
- TACATDP project code: `tacatdp`

## Recommended create/import sequence

1. Create the Power Platform solution and publisher after approval; replace the placeholder `mp` prefix only if the approved publisher prefix differs.
2. Create project/governance tables from `platform-tables.json` and `platform-columns.csv`.
3. Create instrument metadata tables and relationships: `mp_Instrument`, `mp_InstrumentVersion`, `mp_EventDefinition`, `mp_InstrumentEventBinding`, `mp_GroupDefinition`, `mp_FieldDefinition`, `mp_FieldRule`.
4. Create controlled vocabulary tables and relationships: `mp_VocabularyScheme`, `mp_VocabularyTerm`, `mp_VocabularyTermLabel`, `mp_VocabularyTermRelation`, `mp_ProjectVocabularyBinding`, `mp_FieldVocabularyBinding`, `mp_ExternalAuthorityIdentifier`.
5. Create high-volume reference data table `mp_VillageReference` with indexed `RegionCode`, `DistrictCode`, and `WardCode` columns for delegated cascading lookup filters.
6. Create runtime tables and relationships: `mp_TrackedEntity`, `mp_EntityIdentifier`, `mp_Encounter`, `mp_Submission`, `mp_GroupInstance`, `mp_AnswerValue`, `mp_MultiSelectAnswer`, `mp_Attachment`, `mp_SubmissionReview`, `mp_AuditEvent`.
7. Create projection/export tables: `mp_ExportProfile`, `mp_ExportColumn`.
8. Add alternate keys from `platform-alternate-keys.csv` after referenced columns exist.
9. Import seed records in this order: `mp_Project`, `mp_Instrument`, `mp_InstrumentVersion`, `mp_EventDefinition`, `mp_GroupDefinition`, `mp_VocabularyScheme`, non-village `mp_VocabularyTerm`, `mp_VocabularyTermLabel`, `mp_VillageReference`, `mp_FieldDefinition`, `mp_FieldRule`, vocabulary/reference bindings, and project bindings.
10. Import TACATDP metadata from `tacatdp-field-definitions.csv`, `tacatdp-vocabulary-terms.csv`, and `tacatdp-village-reference.csv` only after the generated rows are reviewed.
11. Bind the Canvas app only after the reviewed dev Dataverse schema exists.

## Reference-data decision

Villages are intentionally not stored as generic `mp_VocabularyTerm` rows in this revision. The source contains 66297 villages, so a dedicated `mp_VillageReference` table is more efficient for Canvas cascading lookups because the app can delegate filters directly against indexed `RegionCode`, `DistrictCode`, and `WardCode` columns. Smaller choice lists remain governed vocabulary terms.

## Review checks before environment writes

- Confirm publisher prefix and solution name.
- Confirm whether the 72 fields without a `source_screen` match should stay grouped by old save-target projection or be assigned to explicit metadata groups. These are not missing XLSForm fields; they are fields whose labels did not map cleanly to the current Canvas screen YAML, mostly production-cost line-item fields.
- Confirm `mp_VillageReference` naming and key columns before creating tables.
- Confirm field-level requiredness remains app-visible-only; `required_in_dataverse` is intentionally `no` for imported TACATDP fields.
- Confirm alternate keys do not exceed Dataverse key constraints in the target environment.

## Generated artifact inventory

- `platform-tables.json`: 30 platform/reference tables.
- `platform-columns.csv`: 170 platform/reference columns.
- `platform-relationships.csv`: 46 relationships.
- `platform-alternate-keys.csv`: 22 alternate keys.
- `tacatdp-field-definitions.csv`: 292 TACATDP field definitions.
- `tacatdp-vocabulary-terms.csv`: 5190 TACATDP non-village vocabulary terms.
- `tacatdp-village-reference.csv`: 66297 TACATDP village reference rows.
