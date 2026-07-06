# Schema Import Guide Supersession Note

Status: fallback. The active July 7 MVP uses Dataverse MVP tables from `schemas/dataverse/mvp-tables.json` and `schemas/dataverse/mvp-columns.csv`; Microsoft Lists import guidance below is retained only as fallback.

# Microsoft Lists Schema Import Guide

## Generated artifacts

Run the generator from the repository root:

```bash
.venv/bin/python tools/generate_microsoft_lists_schema.py
```

It creates:

- `schemas/sharepoint-lists-schema.json` - canonical list and column definitions.
- `schemas/sharepoint-fields.csv` - reviewable field list with SharePoint types.
- `schemas/xlsform-to-list-mapping.csv` - mapping from each XLSForm input field to target list/column storage.
- `schemas/import-templates/*.csv` - empty CSV templates for importing data into each generated list.
- `schemas/reference-data/*.csv` - reference data CSVs generated from the XLSForm `choices` sheet.
- `scripts/create-microsoft-lists.ps1` - PnP PowerShell script to create lists and typed columns.
- `scripts/import-reference-data.ps1` - PnP PowerShell script to import generated reference data.
- `scripts/create-microsoft-lists.cmd` - Windows launcher that runs the PowerShell script with execution policy bypass for this process.
- `scripts/import-reference-data.cmd` - Windows launcher that imports reference data with execution policy bypass for this process.

## Schema shape

The generated schema uses the agreed hybrid design:

- Parent submission list: `TACATDP_Submissions`
- Section scalar lists: `TACATDP_Profile`, `TACATDP_Agriculture`, `TACATDP_ResourceEfficiency`, `TACATDP_SocialInclusion`, `TACATDP_Beneficiaries`, `TACATDP_SafeguardsClimate`, `TACATDP_InsuranceGuarantee`, `TACATDP_GHGWaterYield`, and `TACATDP_ProductionIncome`
- Child lists: `TACATDP_MultiSelectAnswers` and `TACATDP_ProductionCostLines`
- Reference lists: `TACATDP_RefRegions`, `TACATDP_RefDistricts`, `TACATDP_RefWards`, `TACATDP_RefVillages`, `TACATDP_RefBranches`, and `TACATDP_RefChoices`

`select_one` fields are stored as value/label text columns rather than SharePoint Choice columns. This preserves XLSForm stored values, keeps labels exportable, and avoids complex-column delegation issues in Power Apps. Primitive XLSForm fields keep typed SharePoint columns: `integer` to Number with zero decimals, `decimal` to Number or Currency, `date` to DateTime, and `geopoint` to raw/latitude/longitude/accuracy columns.

## Import steps

Use PowerShell 7+ (`pwsh`) on Windows. PnP.PowerShell is installed automatically in `CurrentUser` scope if it is missing from the current PowerShell profile.

PnP.PowerShell interactive authentication now requires a client ID from an approved Entra ID App Registration. Do not commit the client ID into scripts or documentation. Pass it on the command line for the current run, or set `ENTRAID_APP_ID`, `ENTRAID_CLIENT_ID`, or `PNP_CLIENT_ID` in the local Windows session.

Recommended Windows command prompt flow:

```bat
cd scripts
create-microsoft-lists.cmd -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>"
import-reference-data.cmd -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>"
```

If you prefer calling PowerShell directly:

```powershell
cd scripts
pwsh -NoProfile -ExecutionPolicy Bypass -File .\create-microsoft-lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>"
pwsh -NoProfile -ExecutionPolicy Bypass -File .\import-reference-data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>"
```

The `-ExecutionPolicy Bypass` flag applies only to that process, so it does not require changing the machine policy.

Create lists and typed fields:

```powershell
cd scripts
.\create-microsoft-lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>"
```

Import reference data:

```powershell
cd scripts
.\import-reference-data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>"
```

The reference import includes 66,297 village rows, so it can take time. Run it after confirming the target SharePoint site and list names.

If the browser popup flow fails with `Specified method is not supported`, use device-code authentication:

```bat
create-microsoft-lists.cmd -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>" -ClientId "<application-client-id>" -AuthMode DeviceLogin
```

The script checks the generated schema before connecting. By default, it fails if any generated list contains more than 300 generated columns. The current hybrid schema remains below that per-list limit; the largest generated list is `TACATDP_Beneficiaries`.

## Windows troubleshooting

If script execution is disabled, use the `.cmd` launchers or the direct `pwsh -NoProfile -ExecutionPolicy Bypass -File ...` commands above. Avoid relying on `Set-ExecutionPolicy -Scope Process` in a previous terminal because it only affects that running PowerShell process.

If PnP.PowerShell is reported as unavailable on the next run, confirm you are using PowerShell 7+ consistently:

```powershell
$PSVersionTable.PSEdition
$PSVersionTable.PSVersion
Get-Module -ListAvailable PnP.PowerShell
```

If `$PSVersionTable.PSEdition` is `Desktop`, you are in Windows PowerShell 5.1; open PowerShell 7 (`pwsh`) or use the `.cmd` launcher. The scripts install PnP.PowerShell with `Install-Module PnP.PowerShell -Scope CurrentUser -Force -AllowClobber` when the module is missing.

## Review before running

1. Confirm the target SharePoint site URL.
2. Review `schemas/sharepoint-fields.csv` for field names and types.
3. Review `schemas/xlsform-to-list-mapping.csv` for target-list assignments.
4. Confirm whether TZS decimal fields should remain Currency or be plain Number.
5. Confirm whether reference data should be imported by script or by Microsoft Lists CSV import.
