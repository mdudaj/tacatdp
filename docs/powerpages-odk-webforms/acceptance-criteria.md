# Acceptance Criteria

- Power Pages site source is downloaded under `powerpages/tacatdp-monitoring-tool/`.
- ODK Central-inspired schema artifacts exist and have a dry-run Dataverse plan.
- One assigned XForm-backed form can be read by an authenticated Power Pages user.
- Draft state can be saved locally and restored.
- Online submit creates a submission header and current submission version.
- One attachment can be uploaded and linked to the submission version.
- No raw Dataverse credentials or client secrets are present in the SPA.


## API Smoke Slice Acceptance

- `python3 scripts/validate-powerpages-api-smoke.py` passes locally.
- Power Pages source contains a hidden `/api-smoke` page.
- The page calls Power Pages `/_api`, not raw Dataverse Web API.
- Browser code contains no client secret, bearer token, or Dataverse OAuth endpoint.
- Hosted `/api-smoke` returns at least one assignment, one form version, and one form record for the signed-in session.
- Any hosted failure is captured with the visible status text and mapped to auth, table permission, entity-set, or seed-data causes before proceeding.
