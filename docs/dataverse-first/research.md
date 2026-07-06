# MVP Supersession Note

Status: updated by `docs/mvp-july-7.md`. The Dataverse-first conclusion remains valid, but the July 7 implementation uses the smaller MVP tables and defers multi-select child tables, production-cost line rows, repeat groups, and full platform schema until after the first vertical slice.

# TACATDP Dataverse-First Research Note

## Decision

Use Microsoft Dataverse as the primary development data platform for TACATDP now that the development environment has Dataverse enabled. Keep Microsoft Lists/SharePoint as a fallback or export/interoperability path, not the primary app architecture.

## Repository evidence

- `docs/xlsform-summary.md`, `docs/xlsform-field-inventory.csv`, and `schemas/xlsform-to-list-mapping.csv` describe 292 XLSForm input mappings.
- Input profile from `docs/list-schema-design.md`: 122 integer, 54 decimal, 75 `select_one`, 20 `select_multiple`, 19 text, 1 geopoint, and 1 date input.
- Logic/reference profile: 288 required rules, 48 relevance rules, 16 constraints, 9 choice filters, 47 input-used choice lists, and 71,487 source choice rows.
- Largest reference lists: village 66,297 rows, ward 3,966 rows, branch 239 rows, district 184 rows.
- Current hybrid Microsoft Lists design already separates parent submission, section data, child multi-select answers, production cost line rows, and reference data.
- Current generated schema has 18 lists; largest generated list is `TACATDP_Beneficiaries` with 112 generated columns.

## Microsoft evidence

- Microsoft describes Dataverse as a secure cloud data store for business applications where data is stored in typed tables, with custom tables, relationships, security, server-side logic, and Power Apps integration.
- Microsoft notes Dataverse benefits include role-based security, rich metadata, data types and relationships used directly in Power Apps, calculated columns, business rules, workflows, and business process flows.
- Microsoft documents that Dataverse databases are created in Power Platform environments and require environment admin rights and appropriate licensing.
- Microsoft Power Platform ALM guidance centers on solutions, environments, and deployment practices across Power Apps, Power Automate, and Dataverse.
- Microsoft documents alternate keys as a way to integrate external systems when the external system does not store Dataverse GUIDs; this fits TACATDP's `SubmissionKey`, XLSForm names, and reference values.
- Microsoft Power Apps delegation guidance warns that nondelegable queries only process the first 500 records by default, configurable to 2,000; this is unsafe for TACATDP village/reference data unless filters are delegable.

References:

- `https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-intro`
- `https://learn.microsoft.com/en-us/power-platform/admin/create-database`
- `https://learn.microsoft.com/en-us/power-platform/alm/`
- `https://learn.microsoft.com/en-us/power-apps/maker/data-platform/define-alternate-keys-portal`
- `https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview`

## Dataverse vs Microsoft Lists conclusion

| Capability | Dataverse fit | Microsoft Lists fit | TACATDP implication |
| --- | --- | --- | --- |
| Parent/child relationships | Native relationships and lookup columns | Manual `SubmissionKey` joins across lists | Dataverse reduces save/reporting complexity. |
| Large reference data | Better table model and delegation support | Possible but more fragile with SharePoint connector limitations | Dataverse is safer for 66k villages and cascades. |
| Validation/business rules | App rules plus Dataverse metadata/business rules | Mostly app-layer rules | Dataverse can enforce more durable constraints. |
| ALM | Solutions and environment strategy | Scripts/lists/source docs | Dataverse aligns better with dev/test/prod. |
| Security | Table/row/role model | Site/list/item permissions | Dataverse is more robust if role-based access matters. |
| Licensing/admin dependency | Higher | Lower if SharePoint is already licensed | Trial/dev is now available; production licensing remains a decision. |

## Recommended platform stance

1. Use Dataverse-first for schema, app data sources, validation/save-map planning, and trial development.
2. Preserve Microsoft Lists artifacts as fallback and as evidence for the existing hybrid data decomposition.
3. Keep `SubmissionKey` as an alternate key / integration key even when Dataverse primary GUIDs exist.
4. Use Dataverse relationships for parent submission to section rows, multi-select answers, production cost lines, and reference records.
5. Use Power Platform solutions from the start for tables, choices, relationships, canvas app, flows, environment variables, and future managed deployment.

