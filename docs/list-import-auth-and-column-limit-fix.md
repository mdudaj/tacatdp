# Microsoft Lists Import Auth and Column Limit Fix

## Task classification

- Project: TACATDP
- Work category: implementation
- Risk: high, because the scripts create SharePoint/Microsoft Lists and use interactive authentication.
- Scope: fix script authentication parameters, add a generated-column preflight guard, and document the corrected Windows command.
- Out of scope: running the scripts against SharePoint, granting permissions, publishing apps, changing production lists, or committing any client ID.

## Requirements note

The Windows run failed at:

```text
Connect-PnPOnline -Url $SiteUrl -Interactive
Please specify a valid client id for an Entra ID App Registration.
Specified method is not supported.
```

PnP.PowerShell current authentication guidance requires `Connect-PnPOnline -Interactive -ClientId <client id of your Entra ID Application Registration>`. It also supports `-DeviceLogin -ClientId <client id>` for environments where the popup/browser flow is unsupported.

The generated Microsoft Lists design must also respect the project constraint that a list should not exceed 300 generated columns. The current hybrid schema is below that limit; the largest generated list is `TACATDP_Beneficiaries` with 112 generated columns.

## Product requirements

1. The create-list script must require or discover a PnP/Entra client ID without hard-coding it.
2. The reference import script must use the same authentication path as the create-list script.
3. The create-list script must fail before connecting if any generated list exceeds the configured per-list column limit.
4. The documentation must show the corrected command and a `DeviceLogin` fallback for the reported `Specified method is not supported` error.
5. The fix must not run live SharePoint writes or store secrets.

## User story

As a TACATDP maker on the authorized Windows laptop, I want the Microsoft Lists import scripts to accept an approved Entra app client ID and fail early on unsafe list widths, so that I can create the designed lists without ad-hoc script edits or SharePoint column-limit surprises.

## Acceptance criteria

1. `create-microsoft-lists.ps1` accepts `-ClientId` and passes it to `Connect-PnPOnline`.
2. `import-reference-data.ps1` accepts `-ClientId` and passes it to `Connect-PnPOnline`.
3. Both scripts can read `ENTRAID_APP_ID`, `ENTRAID_CLIENT_ID`, or `PNP_CLIENT_ID` from the local session.
4. Both scripts support `-AuthMode Interactive`, `-AuthMode DeviceLogin`, and `-AuthMode OSLogin`.
5. `create-microsoft-lists.ps1` defaults to a 300 generated-column limit and throws before connecting if a generated list exceeds it.
6. The import guide documents the corrected command and device-login fallback.
7. No client ID, tenant secret, token, or credential is committed.

## Requirements traceability

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Client ID support | `scripts/create-microsoft-lists.ps1`, `scripts/import-reference-data.ps1` | PowerShell parser validation |
| Device-login fallback | `-AuthMode DeviceLogin` switch in both scripts | PowerShell parser validation and docs review |
| Column-limit preflight | `Test-ListColumnLimits` in create script | Python schema count check |
| Current schema below 300/list | `schemas/sharepoint-lists-schema.json` | Max generated list: `TACATDP_Beneficiaries` with 112 fields |
| Operator guidance | `docs/schema-import-guide.md`, `docs/list-schema-design.md` | Diff review |

## Artifact readiness

- Ready for local script handoff: yes.
- Ready for live SharePoint execution: only after the user supplies an approved Entra app client ID and intentionally runs the script on the authorized Windows environment.
- Blocking gaps for live execution:
  - Approved Entra ID App Registration client ID is required.
  - The user must choose `Interactive`, `DeviceLogin`, or `OSLogin` based on the Windows environment.
  - Production SharePoint writes remain explicit-approval work.

## Safety review

- No secrets or client IDs are stored in the repository.
- The scripts now fail with a clear message if no client ID is supplied.
- The column-count guard runs before authentication, reducing the chance of partially-created unsafe lists.
- No live SharePoint command was executed during this fix.

## Threat or abuse case note

- Misuse risk: a user could run the script against the wrong SharePoint site and create lists there. Mitigation: the site URL remains an explicit required parameter and docs require confirming the target site.
- Credential risk: a client ID is not a secret, but it should still be treated as environment-specific configuration and not committed. The scripts use parameters or local environment variables.
- Data risk: reference import writes many rows, especially villages. It remains a separate command after schema creation.

## Approval record

No approval was requested or used to run live SharePoint writes, permission changes, app import/publish, or destructive operations. This task only changed scripts and documentation locally.

## Verification summary

- Parsed `scripts/create-microsoft-lists.ps1` with PowerShell parser.
- Parsed `scripts/import-reference-data.ps1` with PowerShell parser.
- Checked `schemas/sharepoint-lists-schema.json` for generated list column counts.
- Confirmed no generated list exceeds 300 columns; maximum is `TACATDP_Beneficiaries` with 112 generated columns.

## Definition of done

Done when the scripts and docs are committed on the task branch, the local parser/schema checks pass, and the TACATDP handoff is refreshed. Live SharePoint success is not part of this local fix because it requires the authorized Windows environment and approved client ID.

## Change summary

- Added `-ClientId`, environment-variable fallback, and `-AuthMode` to both PnP scripts.
- Added generated-column preflight to `create-microsoft-lists.ps1`.
- Updated import docs with the corrected command and device-login fallback.
- Updated schema design docs to record the 300 generated-column guardrail.

## Test or eval rationale

No live integration test was run because that would create SharePoint/Microsoft Lists objects in the target tenant. Static parser validation and schema-count checks are the appropriate local verification for this branch; live execution remains an explicit operator action.

