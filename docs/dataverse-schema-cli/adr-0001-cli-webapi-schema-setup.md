# ADR 0001: Use PAC plus Dataverse Web API for MVP schema setup

## Status

Accepted for July 7 MVP implementation planning.

## Context

The MVP needs ten Dataverse tables and a small seed form quickly. The Power Platform maker portal is useful for inspection, but manual clicks are hard to review and repeat. PAC CLI is already authenticated and verified for the target environment, but PAC does not provide a simple first-class command for creating arbitrary table/column metadata from our CSV/JSON artifacts.

Microsoft documents PAC for auth, solution lifecycle, and configuration data import/export. Microsoft documents Dataverse Web API metadata endpoints for creating tables, columns, and relationships.

## Decision

Use a dry-run-first delivery path:

1. Use PAC to authenticate and verify the target Dataverse environment.
2. Use PAC solution commands to create/select/export/check the unmanaged dev solution.
3. Use local scripts to validate schema artifacts and generate an operation plan.
4. Use Dataverse Web API metadata requests for table, column, and relationship creation after explicit approval.
5. Include `MSCRM.SolutionUniqueName` on metadata create requests.
6. Use small seed data import only after the schema is created.

## Consequences

- Schema delivery is reviewable and repeatable.
- We avoid hand-clicked maker portal drift.
- We need a small Web API deployment script or command wrapper rather than relying on PAC alone.
- Destructive operations, metadata updates, table deletes, column deletes, production writes, and publish/import to non-dev environments remain out of scope unless separately approved.

## Alternatives considered

- **Maker portal only**: fastest for one person, but not repeatable or reviewable enough.
- **Full solution source generation first**: better ALM later, too much for July 7 MVP.
- **Full platform schema first**: aligns with long-term vision, but delays the first runtime proof.
- **PAC data import only**: useful for seed/configuration data, but not sufficient for table/column metadata creation.
