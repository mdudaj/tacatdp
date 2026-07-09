# Artifact Readiness: Dataverse Schema CLI Delivery

## Ready

- Dev Dataverse schema has been executed and verified in `tacatdp_prototype`.

- PAC service-principal auth has been validated by prior `pac solution list` and `pac org who` output.
- MVP schema artifacts exist: `mvp-tables.json`, `mvp-columns.csv`, `mvp-schema-definition.json`, and `docs/dataverse-schema-cli/schema-definition.md`.
- `.env.example` exists and keeps secrets blank.
- Preflight script exists and is dry-run only.

## Must be ready before dev write approval

- Confirm solution unique name and publisher prefix.
- Confirm target environment URL/ID.
- Confirm table logical names and publisher prefix strategy.
- Confirm seed form fields and assignment user.
- Confirm no production target.
- Review dry-run schema operation plan.

## Not ready / explicitly deferred

- Full XLSForm compiler.
- Full multi-project schema.
- Repeat groups and nested repeats.
- Large reference data import.
- Production deployment.
