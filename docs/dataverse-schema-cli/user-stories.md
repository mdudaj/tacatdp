# User Stories: Dataverse Schema CLI Delivery

## DVCLI-US-01: Validate environment before schema setup

As a developer, I want the deployment preflight to validate my local PAC/env configuration so that I do not accidentally target the wrong Dataverse environment.

Acceptance:

1. Missing environment URL/ID is reported.
2. Secrets are not printed.
3. Dry-run mode is the default.

## DVCLI-US-02: Review the schema operation plan

As a reviewer, I want to see a table/column operation plan before any Dataverse writes so that I can confirm the MVP scope is limited to the ten approved tables.

Acceptance:

1. The plan lists each MVP table.
2. The plan lists columns grouped by table.
3. Deferred platform tables are not included.

## DVCLI-US-03: Create schema in dev after approval

As a maker/developer, I want an approved command path to create the MVP schema in the dev solution so that the Canvas renderer can bind to real Dataverse metadata.

Acceptance:

1. The command uses the reviewed solution unique name.
2. The command targets the approved dev environment.
3. The command refuses production by default.

## DVCLI-US-04: Seed one form after schema setup

As a project manager, I want one form seeded after schema creation so that the assigned-forms and renderer screens can be tested end to end.

Acceptance:

1. One form version is published.
2. One user assignment exists.
3. The seed includes supported MVP question types.
