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
- `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env` passes against the hosted environment.
- Manual browser navigation to `/api-smoke` is optional observation, not the delivery gate.

## SPA Foundation Slice Acceptance

- `docs/powerpages-odk-webforms/user-stories.md` exists and maps stories to requirements.
- `docs/powerpages-odk-webforms/slice-checklist.md` identifies completed, current, next, and deferred work.
- `docs/powerpages-odk-webforms/package-review.md` exists and blocks dependency installation until accepted.
- `powerpages/webforms-spa/` contains a private Vite/Vue package skeleton.
- SPA source uses Power Pages `/_api` paths and includes anti-forgery token handling for future writes.
- SPA source contains no raw Dataverse OAuth endpoint, client secret, bearer token, or custom login.
- `python3 scripts/validate-webforms-spa-foundation.py` passes.
- Hosted state remains verified by `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`.
