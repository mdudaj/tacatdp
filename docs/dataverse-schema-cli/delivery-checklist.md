# Delivery Checklist: Dataverse Schema CLI Setup

## Before writes

- [ ] Confirm current branch and clean worktree.
- [ ] Confirm `.env` points to dev only.
- [ ] Run `python3 scripts/dataverse-deploy-preflight.py --env-file .env.example --allow-placeholders`.
- [ ] Run `python3 scripts/dataverse-deploy-preflight.py --env-file .env`.
- [ ] Run `python3 scripts/dataverse-schema-plan.py --schema-dir schemas/dataverse`.
- [ ] Review operation plan for only ten MVP tables.
- [ ] Confirm solution unique name and publisher prefix.
- [ ] Confirm exact target environment URL/ID.
- [ ] Get explicit approval for dev Dataverse writes.

## Dev schema setup

- [ ] `pac auth who` confirms expected service principal or maker identity.
- [ ] `pac solution list --environment "$POWER_PLATFORM_ENVIRONMENT_URL"` succeeds.
- [ ] Dev solution exists or is created.
- [ ] Tables are created through reviewed metadata operations.
- [ ] Columns are created through reviewed metadata operations.
- [ ] Relationships/lookups are created only after referenced tables exist.
- [ ] Customizations are published only after schema review.

## Seed data

- [ ] One form row exists.
- [ ] One published form version exists.
- [ ] Sections/questions/choices/rules cover MVP field types.
- [ ] One assignment exists for the test user.
- [ ] Canvas renderer can read assigned form metadata.
