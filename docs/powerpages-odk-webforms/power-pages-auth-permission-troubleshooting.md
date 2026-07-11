# Power Pages Auth and Table Permission Troubleshooting

## Scope

This runbook captures the evidence-backed troubleshooting path for the TACATDP Power Pages `/_api` smoke test in the `PowerPagesDeveloper-070926-125720` environment.

Target site:

- Site: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`
- Dataverse URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Smoke route: `https://tacatdp.powerappsportals.com/api-smoke/`

Authoritative references:

- Power Pages Web API overview: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview`
- Power Pages Web API HTTP requests and errors: `https://learn.microsoft.com/en-us/power-pages/configure/web-api-http-requests-handle-errors`
- Power Pages table permissions: `https://learn.microsoft.com/en-us/power-pages/security/table-permissions`
- Power Pages Liquid objects: `https://learn.microsoft.com/en-us/power-pages/configure/liquid/liquid-objects`
- Power Pages OpenID Connect settings: `https://learn.microsoft.com/en-us/power-pages/security/authentication/openid-settings`

## Final Passing State

On 2026-07-10, the `/api-smoke` browser check passed:

```text
Power Pages /_api read smoke test passed.
```

Before the pass, the page diagnostics showed the correct portal session:

```text
Contact ID: f1e65863-d37b-f111-ab0e-7c1e523612eb
Email: john.mduda@mshirikacorp.onmicrosoft.com
Roles: Authenticated Users
```

The final blocker was not Dataverse schema, Web API site settings, contact identity, or browser token handling. The blocker was Power Pages runtime recognition of table permission to web-role associations. Direct Dataverse-created permission rows and relationship rows were visible to scripts, but the runtime still returned `EntityPermissionReadIsMissing` until the relevant table permissions were opened and saved through the Power Pages Security workspace with `Authenticated Users` selected.

## Failure Timeline and Diagnosis

### 1. Private-site banner was not portal contact auth

The top banner showed:

```text
This site is private: Only specific people can view this site.
Signed in as John Mduda
```

The smoke page still showed:

```text
Not signed in
Authentication required
```

Diagnosis:

- The private-site banner proves access to the private Power Pages site.
- It does not prove Liquid `user` has resolved to a portal `Contact`.
- Power Pages Liquid `user` is the current portal contact/user. If it is null, `/_api` table permissions cannot be evaluated for that contact.

### 2. Contact and external identity had to be proven

Evidence required before troubleshooting table permissions:

- A `Contact` exists for `john.mduda@mshirikacorp.onmicrosoft.com`.
- The contact has the `Authenticated Users` web role.
- The contact has a redeemed external identity.
- The page diagnostics show the same contact ID as Dataverse.

Run:

```bash
python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env
```

The hosted verifier checks contact existence, web-role membership, and external identity presence. This is necessary but not sufficient for runtime `/_api` success.

### 3. Custom OIDC was not needed for the final MVP path

A custom OpenID Connect provider named `TACATDP Entra ID` was tested. It authenticated but reached:

```text
Register your external account
The Email field is required.
```

When the existing email was entered, Power Pages reported it was already taken. That means the custom provider was trying to create or complete another external account flow instead of cleanly linking to the existing contact.

The final passing path used the default Microsoft Entra provider after the existing contact/external identity mapping was corrected. Do not use the custom provider as the MVP gate unless there is a specific client requirement to replace the default provider.

If custom OIDC is revisited later, keep these settings as the baseline:

```text
Authentication/OpenIdConnect/OpenId_1/Scope = openid email profile
Authentication/OpenIdConnect/OpenId_1/RegistrationClaimsMapping = firstname=given_name,lastname=family_name,emailaddress1=preferred_username
Authentication/OpenIdConnect/OpenId_1/LoginClaimsMapping = firstname=given_name,lastname=family_name,emailaddress1=preferred_username
```

### 4. `EntityPermissionReadIsMissing` meant runtime did not recognize the permission

With `Webapi/error/innererror=true`, Power Pages returned:

```json
{
  "error": {
    "code": "90040120",
    "message": "You don't have permission to read the mp_formassignment table.",
    "innererror": {
      "code": "90040120",
      "message": "You don't have permission to read the mp_formassignment table.",
      "type": "EntityPermissionReadIsMissing"
    }
  }
}
```

The same occurred for `mp_formversion` after `mp_formassignment` was fixed.

This means Power Pages found the Web API request and user session but did not find an effective read table permission for that table at runtime.

### 5. Direct Dataverse checks were necessary but not sufficient

The scripts verified all of these were present:

- `Webapi/mp_formassignment/enabled = true`
- `Webapi/mp_formassignment/fields = *`
- `mspp_entitypermission.mspp_entitylogicalname = mp_formassignment`
- `mspp_entitypermission.mspp_read = true`
- `mspp_entitypermission.mspp_scope = 756150000` (`Global`)
- `mspp_entitypermission_webroleset` linked the permission to `Authenticated Users`
- `powerpagecomponent_powerpagecomponent` linked the enhanced permission component to the enhanced web-role component
- `powerpagecomponent.powerpagesiteid` matched the TACATDP website ID

Even with these rows present, the runtime returned `EntityPermissionReadIsMissing`. The fix was to save the role association through the Power Pages Security workspace.

## Proven Fix

Use the Power Pages Security workspace for table permission role association.

Path:

1. Open `https://make.powerpages.microsoft.com/`.
2. Select environment `PowerPagesDeveloper-070926-125720`.
3. Open site `TACATDP Monitoring Tool`.
4. Select `Edit`.
5. Open `Security`.
6. Open `Table permissions`.
7. For each required table permission, confirm:
   - Access type: `Global`
   - `Read`: checked for metadata tables
   - Write flags only where intentionally needed for submission tables
   - Web role: `Authenticated Users`
8. Save.
9. Restart the site.
10. Test `/api-smoke` in browser.

Minimum tables for the read smoke:

- `mp_formassignment`
- `mp_formversion`
- `mp_form`

Recommended metadata tables for the first ODK Web Forms slice:

- `mp_project`
- `mp_form`
- `mp_formversion`
- `mp_formassignment`
- `mp_formattachment`

Submission tables will be needed for online submit:

- `mp_submission`
- `mp_submissionversion`
- `mp_submissionattachment`

## Browser Smoke Gate

The automated hosted verifier remains required, but it is no longer sufficient by itself. Browser runtime verification is required after any table permission or web-role change.

Open:

```text
https://tacatdp.powerappsportals.com/api-smoke/?v=<unique-cache-buster>
```

Passing result:

```text
Power Pages /_api read smoke test passed.
```

Diagnostic panel should show:

```text
Contact ID: <expected contact id>
Email: <expected email>
Roles: Authenticated Users
```

## Temporary Inner Error Diagnostic

`Webapi/error/innererror=true` was enabled temporarily to expose the `EntityPermissionReadIsMissing` type. It was removed after diagnosis on 2026-07-10.

Use it only while diagnosing Web API failures. Before sharing a client-facing POC, remove it or set it to `false`.

Check current value by querying `mspp_sitesettings` and `powerpagecomponents` for `Webapi/error/innererror`. Expected client-facing state is zero matching rows or a value of `false`.

Preferred cleanup is through the Power Pages site settings UI or an approved Dataverse update.

## Implementation Instructions for Agents

When Power Pages `/_api` returns `90040120`:

1. Inspect `docs/powerpages-odk-webforms/api-smoke-test.md`, this runbook, and Microsoft Power Pages Web API/table-permission docs.
2. Run `python3 scripts/verify-powerpages-api-smoke-hosted.py --env-file .env`.
3. Confirm the browser page diagnostic shows the expected contact ID, email, and `Authenticated Users` role.
4. If Liquid `user` is missing, fix contact/external identity before changing permissions.
5. If Liquid `user` and role are correct but `innererror.type = EntityPermissionReadIsMissing`, use the Power Pages Security workspace to open/save the table permission and role association for the failing table.
6. Retest the browser smoke route after each failing table moves forward.
7. Do not assume direct Dataverse relationship rows are enough for runtime authorization unless the browser smoke passes.
8. Remove temporary `Webapi/error/innererror` before client-facing sharing.
