# Verification Summary: Dataverse Schema CLI Delivery

## Current status

Executed against the configured dev Dataverse environment on 2026-07-06.

## Live write result

- Publisher exists/created with prefix `mp`.
- Unmanaged solution exists: `tacatdp_prototype` / `TACATDP Impact Tracking Prototype`, version `0.1.0.0`.
- Created/present tables:
  - `mp_form`
  - `mp_formversion`
  - `mp_section`
  - `mp_question`
  - `mp_choice`
  - `mp_validationrule`
  - `mp_formassignment`
  - `mp_submission`
  - `mp_submissionanswer`
  - `mp_submissionfile`
- Created/present lookup relationships: 13.
- Published customizations: yes.

## Schema adjustment made during deployment

Dataverse requires the primary name attribute for a custom table to be a text attribute. `ValidationRules` originally used `RuleType` as the primary name, but `RuleType` is a Choice. The deployed schema now uses `ValidationRules.Name` as the required text primary name column and keeps `ValidationRules.RuleType` as the rule-type choice.

## Commands verified

```bash
python3 scripts/dataverse-deploy-preflight.py --env-file .env
python3 scripts/dataverse-schema-plan.py --schema-dir schemas/dataverse
python3 scripts/dataverse-schema-deploy.py --env-file .env --execute
python3 scripts/dataverse-schema-deploy.py --env-file .env --execute --no-publish
pac solution list --environment "$POWER_PLATFORM_ENVIRONMENT_URL"
```

## Verified output

- Preflight passed with no issues.
- Dry-run plan now reports 73 operations: 10 tables, 50 columns, 13 relationships.
- Idempotent verification reported all tables, direct columns, and relationships as existing.
- PAC solution list shows `tacatdp_prototype` as unmanaged.


## Seed data result

Executed against the configured dev Dataverse environment on 2026-07-06.

- Seed form: `TACATDP-MVP-001` / `TACATDP MVP Field Visit`.
- Published version: `2026-07-07-v1`.
- Section: `core` / `Core Visit`.
- Questions seeded for the Canvas renderer:
  - `farmer_name` (`text`, required)
  - `farmer_age` (`integer`)
  - `land_size_acres` (`decimal`)
  - `visit_date` (`date`, required)
  - `primary_crop` (`select_one`, required; choices `maize`, `rice`, `sunflower`, `other`)
  - `support_needed` (`select_many`; choices `finance`, `inputs`, `training`, `market`)
  - `farm_photo` (`file_photo_attachment`)
  - `gps_point` (`gps`)
- Validation rules seeded for required questions: `farmer_name`, `visit_date`, `primary_crop`.
- Active assignment seeded for `john.mduda@mshirikacorp.onmicrosoft.com`; Dataverse `systemuser` lookup resolved successfully.
- Idempotent verification passed: rerunning the seed command reports all rows as existing.

Seed command:

```bash
python3 scripts/dataverse-seed-mvp-form.py --env-file .env --execute
```

## Not yet done

- Build Canvas renderer against the created Dataverse tables and seeded form metadata.
- Add export/import solution packaging once the schema stabilizes.

## Canvas renderer handoff

The next delivery package is `docs/canvas-renderer-mvp/`, using the seeded form `TACATDP-MVP-001` and assignment for `john.mduda@mshirikacorp.onmicrosoft.com`.
