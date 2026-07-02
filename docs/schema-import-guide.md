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

## Schema shape

The generated schema uses the agreed hybrid design:

- Parent submission list: `TACATDP_Submissions`
- Section scalar lists: `TACATDP_Profile`, `TACATDP_Agriculture`, `TACATDP_ResourceEfficiency`, `TACATDP_SocialInclusion`, `TACATDP_Beneficiaries`, `TACATDP_SafeguardsClimate`, `TACATDP_InsuranceGuarantee`, `TACATDP_GHGWaterYield`, and `TACATDP_ProductionIncome`
- Child lists: `TACATDP_MultiSelectAnswers` and `TACATDP_ProductionCostLines`
- Reference lists: `TACATDP_RefRegions`, `TACATDP_RefDistricts`, `TACATDP_RefWards`, `TACATDP_RefVillages`, `TACATDP_RefBranches`, and `TACATDP_RefChoices`

`select_one` fields are stored as value/label text columns rather than SharePoint Choice columns. This preserves XLSForm stored values, keeps labels exportable, and avoids complex-column delegation issues in Power Apps. Primitive XLSForm fields keep typed SharePoint columns: `integer` to Number with zero decimals, `decimal` to Number or Currency, `date` to DateTime, and `geopoint` to raw/latitude/longitude/accuracy columns.

## Import steps

Install PnP PowerShell if needed:

```powershell
Install-Module PnP.PowerShell -Scope CurrentUser
```

Create lists and typed fields:

```powershell
cd scripts
.\create-microsoft-lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>"
```

Import reference data:

```powershell
cd scripts
.\import-reference-data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<site>"
```

The reference import includes 66,297 village rows, so it can take time. Run it after confirming the target SharePoint site and list names.

## Review before running

1. Confirm the target SharePoint site URL.
2. Review `schemas/sharepoint-fields.csv` for field names and types.
3. Review `schemas/xlsform-to-list-mapping.csv` for target-list assignments.
4. Confirm whether TZS decimal fields should remain Currency or be plain Number.
5. Confirm whether reference data should be imported by script or by Microsoft Lists CSV import.
