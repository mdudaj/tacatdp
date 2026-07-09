# Research: Dataverse Schema Setup Through CLI and Web API

## Sources checked

- Microsoft Power Platform CLI `pac auth`: `https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth`
- Microsoft Power Platform CLI `pac solution`: `https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution`
- Microsoft Power Platform CLI `pac data`: `https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/data`
- Dataverse Web API table definitions: `https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-entity-definitions-using-web-api`
- Dataverse Web API column definitions: `https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-column-definitions-using-web-api`
- Dataverse Web API relationships: `https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-entity-relationships-using-web-api`
- Dataverse Web API choices/option sets: `https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-optionsets`

## Findings

1. PAC is the right entry point for authentication and solution lifecycle. Microsoft documents `pac auth create`, `auth list`, `auth select`, and `auth who` for environment-targeted auth profiles, including service-principal auth.
2. PAC solution commands are for Dataverse solution projects and solution lifecycle. Microsoft documents `pac solution init`, `list`, `export`, `import`, `check`, `add-solution-component`, `pack`, `unpack`, and `publish`.
3. PAC data commands are for Dataverse configuration data import/export, not large data loads. Microsoft explicitly notes these commands are intended for configuration data and are not suitable for large volumes.
4. Deterministic custom table, column, and relationship creation should use Dataverse Web API metadata operations. Microsoft documents posting table definitions to `EntityDefinitions`, adding columns to `EntityDefinitions(LogicalName='<table>')/Attributes`, and posting relationships to `RelationshipDefinitions`.
5. Web API metadata create requests can include the `MSCRM.SolutionUniqueName` header to associate customizations with the intended solution.
6. Updating table definitions and relationships is replacement-style and riskier than creating new metadata. Microsoft documents `PUT` semantics for updates and warns that individual table definition properties cannot be patched. The MVP should be create-first and avoid destructive/update operations unless separately reviewed.
7. Choice metadata can be created through Web API global option set endpoints, but the MVP can avoid global choices by storing form choices as rows in the `Choices` table and using simple status choices where needed.

## Architecture implication

For the July 7 MVP, use a hybrid CLI delivery path:

- PAC: authenticate, verify org, create/list/export solution, run solution checker, import/export configuration data when appropriate.
- Local dry-run script: validate MVP schema artifacts and emit the planned metadata operations.
- Dataverse Web API: create tables, columns, and relationships with `MSCRM.SolutionUniqueName` after explicit approval.
- PAC data import or Web API row upsert: seed one small form and assignment after schema exists.

## MVP constraints

- Create only the 10 MVP tables in `schemas/dataverse/mvp-tables.json`.
- Use `schemas/dataverse/mvp-schema-definition.json` and `docs/dataverse-schema-cli/schema-definition.md` as the reviewed schema definition; keep `schemas/dataverse/mvp-columns.csv` as the script-friendly column contract.
- Avoid full platform tables, repeat groups, nested repeats, full XLSForm compiler, offline sync, barcode, dashboards, and admin publishing UI.
- Do not create a custom users table; reference Dataverse system users or store user email in `FormAssignments` and `Submissions`.
- Keep all writes dev-only and behind explicit approval.
