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

For the ODK submit path, `mp_formversion` remains read-only for portal users but must grant `Append To`. Creating an `mp_submission` with `mp_FormVersion@odata.bind` associates the new submission to an existing form version; Power Pages Web API returns `90040106` if the referenced table lacks `Append To`.

Verified on 2026-07-09 against `PowerPagesDeveloper-070926-125720`:

- 16 named Web API site settings exist: enabled and fields settings for all 8 `mp_*` tables.
- 8 table permissions exist: metadata tables are read-only except `mp_formversion` grants `Append To` for submission lookup association; submission tables allow read/create/write/append/append-to.
- All 8 table permissions are linked to the Power Pages `Authenticated Users` web role through `mspp_entitypermission_webroleset`.
- In the enhanced data model, all 8 table permission `powerpagecomponent` rows are also linked to the `Authenticated Users` web-role `powerpagecomponent` through `powerpagecomponent_powerpagecomponent`.
- A portal `Contact` exists for `TACATDP_SEED_USER_EMAIL` or the default seeded test email, is assigned the `Authenticated Users` web role under the enhanced data model, and has a redeemed external identity. Power Pages table permissions are evaluated through web roles and portal contacts; a Dataverse maker/admin `systemuser` sign-in alone is not enough for browser `/_api` authorization.

If `/api-smoke/` shows `90040120` / "You don't have permission to read the <table> table":

1. Confirm the signed-in portal user has a `Contact` row in the Power Pages environment with `emailaddress1` matching the seeded assignment email.
2. Confirm the contact has a redeemed external identity. A manually created contact without invitation redemption or external identity linkage is not enough for the portal session to authorize `/_api`.
3. Confirm the browser `/api-smoke` diagnostic panel shows the expected contact ID, email, and `Roles: Authenticated Users`.
4. Confirm `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env` passes the hosted metadata checks.
5. If no contact or external identity exists, create/invite the contact from the Power Pages Portal Management app: `Security > Contacts`, then create/send an invitation and assign the needed web roles during invitation redemption.
6. If the browser user and role are correct but the Web API response includes `innererror.type = EntityPermissionReadIsMissing`, open the failing table permission in Power Pages `Edit site > Security > Table permissions`, confirm `Read` and `Authenticated Users`, and save it from the UI. Direct Dataverse-created `mspp_entitypermission_webroleset` / `powerpagecomponent_powerpagecomponent` rows were visible to scripts but were not sufficient for runtime authorization until the table permission was saved through the Security workspace on 2026-07-10.
7. Restart the Power Pages site, sign out/in, and retest `/api-smoke` with a cache-busting query string.
8. Rerun `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`.

See `docs/powerpages-odk-webforms/power-pages-auth-permission-troubleshooting.md` for the full evidence trail and final passing workflow.

Known dev-environment cleanup note: an earlier script run created 28 nameless `mspp_sitesetting` rows before `mspp_name` was added to the create payload. They are not usable Power Pages Web API settings and are not committed in source. Delete them only through a separately approved Dataverse cleanup.


## Cleanup Verification

After the approved 2026-07-09 cleanup, Dataverse verification showed:

- 0 nameless `mspp_sitesetting` rows.
- 16 named TACATDP `Webapi/mp_*` site settings.

The local Power Pages export was refreshed after cleanup.
