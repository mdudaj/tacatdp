# Dataverse Dev Deployment Harness

This harness prepares TACATDP for reviewed dev Dataverse schema setup. It is dry-run first and does not write to Dataverse by itself.

The active schema setup artifact pack is `docs/dataverse-schema-cli/`.

## Local configuration

Copy `.env.example` to `.env` and fill local values. Do not commit `.env`.

Required local values:

- `PAC_AUTH_NAME`
- `POWER_PLATFORM_CLOUD`
- `POWER_PLATFORM_AUTH_MODE`
- `POWER_PLATFORM_TENANT_ID`
- `POWER_PLATFORM_CLIENT_ID`
- `POWER_PLATFORM_CLIENT_SECRET` when using service-principal deployment
- `POWER_PLATFORM_ENVIRONMENT_ID` or `POWER_PLATFORM_ENVIRONMENT_URL`
- `POWER_PLATFORM_SOLUTION_UNIQUE_NAME`
- `POWER_PLATFORM_PUBLISHER_PREFIX`
- `TACATDP_DATAVERSE_SCHEMA_DIR`

Keep `TACATDP_DRY_RUN=true` and `TACATDP_ALLOW_ENVIRONMENT_WRITE=false` until the exact dev schema write command is reviewed and approved.

## Preflight

Validate the example file shape without secrets:

```bash
python3 scripts/dataverse-deploy-preflight.py --env-file .env.example --allow-placeholders
```

Validate local configuration without printing secret values:

```bash
python3 scripts/dataverse-deploy-preflight.py --env-file .env
```

Machine-readable output:

```bash
python3 scripts/dataverse-deploy-preflight.py --env-file .env --json
```

## Schema operation plan

Generate a reviewable dry-run operation plan:

```bash
python3 scripts/dataverse-schema-plan.py --schema-dir schemas/dataverse
```

The plan must list only the ten MVP tables from `mvp-tables.json`, columns from `mvp-columns.csv`, and relationships from `mvp-schema-definition.json` / `schema-definition.md`.

## Microsoft-backed delivery path

- PAC handles auth and solution lifecycle: `pac auth who`, `pac solution list`, `pac solution export`, `pac solution import`, `pac solution check`.
- Dataverse Web API metadata operations create tables, columns, and relationships after approval.
- Metadata create calls should include `MSCRM.SolutionUniqueName` so components land in the intended unmanaged dev solution.
- PAC data import is for small configuration/seed data and is not the large-data import path.

## Deployment boundary

This harness validates and plans:

- local configuration presence;
- MVP schema artifact presence;
- required MVP table set;
- required generic answer/file/status columns;
- whether `pac` is available on PATH.

It does not authenticate, create tables, import data, publish apps, change permissions, or deploy solutions.

## Next reviewed command

After preflight and plan pass, create a separate reviewed deployment command that uses the MVP schema set only, targets dev only, and refuses destructive operations by default.

## Live schema command

After review and explicit approval, execute dev schema setup with:

```bash
python3 scripts/dataverse-schema-deploy.py --env-file .env --execute
```

Verify idempotently without republishing:

```bash
python3 scripts/dataverse-schema-deploy.py --env-file .env --execute --no-publish
```

## MVP seed command

After schema setup succeeds, seed the first renderer form with:

```bash
python3 scripts/dataverse-seed-mvp-form.py --env-file .env --execute
```

Set `TACATDP_SEED_USER_EMAIL` in `.env` to override the default assignment user.
