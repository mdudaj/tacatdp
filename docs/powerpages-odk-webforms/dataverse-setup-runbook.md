# Dataverse Setup Runbook for Power Pages ODK Web Forms

## Evidence to Inspect First

- `schemas/dataverse/odk-central-inspired-mvp-schema.json`
- `schemas/dataverse/odk-central-inspired-mvp-schema.md`
- `docs/powerpages-odk-webforms/adr-0002-power-pages-odk-webforms.md`
- `docs/powerpages-odk-webforms/requirements.md`
- `powerpages/tacatdp-monitoring-tool/.powerpages-site/`
- `pac auth list`, `pac env who`, and `pac pages list` output

## Dry Run

```bash
python3 scripts/dataverse-schema-plan.py \
  --schema-file schemas/dataverse/odk-central-inspired-mvp-schema.json \
  --solution "$POWER_PLATFORM_SOLUTION_UNIQUE_NAME"
```

## Approved Write Command

Only run after explicit approval and after `.env` points to the Power Pages developer environment.

```bash
python3 scripts/dataverse-schema-deploy.py \
  --schema-file schemas/dataverse/odk-central-inspired-mvp-schema.json \
  --execute
```

## Expected Tables

- Projects
- Forms
- FormVersions
- FormAttachments
- FormAssignments
- Submissions
- SubmissionVersions
- SubmissionAttachments

## Follow-Up After Schema

1. Seed one project/form/form version/assignment.
2. Configure Power Pages Web API site settings.
3. Configure table permissions/web roles.
4. Test authenticated `/_api` read from the site.


## Rich ODK MVP Seed

After the ODK Central-inspired schema exists, seed the richer XForm-backed MVP form:

```bash
python3 scripts/dataverse-seed-odk-mvp-form.py   --env-file .env   --execute
```

The seed stores the canonical XForm XML in `FormVersions.XFormXml` and creates/updates:

- one `Projects` row,
- one `Forms` row with `XmlFormId=tacatdp_impact_evaluation`,
- one published `FormVersions` row with about 43 fields, groups, relevance, constraints, GPS, select-one, select-many, and image upload,
- one active `FormAssignments` row for `TACATDP_SEED_USER_EMAIL` or the default maker account.


## Power Pages Web API and Table Permissions

After schema and seed data exist, configure authenticated Power Pages `/_api` access:

```bash
python3 scripts/powerpages-configure-webapi.py   --env-file .env   --execute
```

The script creates/updates `Webapi/<logical table>/enabled=true`, `Webapi/<logical table>/fields=*`, and Global table permissions for the Authenticated Users web role. This is acceptable for the dev POC; before production, replace broad Global submission permissions with contact/self/custom-scoped permissions.

Verified on 2026-07-09 against `PowerPagesDeveloper-070926-125720`:

- 16 named Web API site settings exist: enabled and fields settings for all 8 `mp_*` tables.
- 8 table permissions exist: metadata tables are read-only; submission tables allow read/create/write/append/append-to.
- All 8 table permissions are linked to the Power Pages `Authenticated Users` web role through `mspp_entitypermission_webroleset`.

Known dev-environment cleanup note: an earlier script run created 28 nameless `mspp_sitesetting` rows before `mspp_name` was added to the create payload. They are not usable Power Pages Web API settings and are not committed in source. Delete them only through a separately approved Dataverse cleanup.
