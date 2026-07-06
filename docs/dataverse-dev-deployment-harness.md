# Dataverse Dev Deployment Harness

This harness prepares TACATDP for a reviewed dev Dataverse deployment. It is dry-run first and does not write to Dataverse by itself.

## Local Configuration

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

Keep `TACATDP_DRY_RUN=true` and `TACATDP_ALLOW_ENVIRONMENT_WRITE=false` until the exact deployment command is reviewed and approved.

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

## Service Principal Requirements

Before any service-principal deployment, the app registration must be added as an application user in the target Power Platform environment and assigned the required security roles. The local client secret remains only in `.env` or the operator's secret manager.

## Deployment Boundary

This harness only validates:

- local configuration presence;
- review-only schema artifact presence and row counts;
- required prototype tables;
- `mp_AnswerValue` lookup columns for vocabulary terms and village references;
- required relationships for those lookups;
- whether `pac` is available on PATH.

It does not authenticate, create tables, import data, publish apps, change permissions, or deploy solutions.

## Next Reviewed Command

After preflight passes and the dev target is approved, create a separate reviewed deployment command that uses the reduced prototype schema set only. Keep production deployment out of scope.
