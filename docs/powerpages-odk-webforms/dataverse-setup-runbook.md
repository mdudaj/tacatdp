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
