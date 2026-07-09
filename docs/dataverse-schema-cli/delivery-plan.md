# Delivery Plan: Dataverse Schema CLI Setup

## Step 1: Validate local configuration

Run preflight against `.env.example` and `.env`. Keep `TACATDP_DRY_RUN=true` and `TACATDP_ALLOW_ENVIRONMENT_WRITE=false` until approval.

## Step 2: Generate operation plan

Review `docs/dataverse-schema-cli/schema-definition.md`, then run `scripts/dataverse-schema-plan.py` to produce a reviewable list of tables, columns, and lookup relationships that would be created. The output must include only the MVP schema.

## Step 3: Confirm PAC and solution

Use PAC to verify identity and solution state:

```bash
pac auth who
pac solution list --environment "$POWER_PLATFORM_ENVIRONMENT_URL"
```

If needed, initialize/export/check solution assets with PAC solution commands. Keep production out of scope.

## Step 4: Implement approved metadata write command

After review, implement or run a separate Web API deployment command that:

- obtains an access token without printing it;
- posts table definitions to `EntityDefinitions`;
- posts columns to each table's `Attributes` collection;
- creates required relationships through `RelationshipDefinitions`;
- sends `MSCRM.SolutionUniqueName` on metadata create calls;
- refuses production and destructive operations.

## Step 5: Seed one form

After schema exists, seed one form/version/assignment and representative questions. Keep seed data small enough for manual review.

## Step 6: Hand off to Canvas renderer

Only after schema and seed data exist should the Canvas renderer bind to Dataverse tables.

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
