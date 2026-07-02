param(
    [Parameter(Mandatory = $true)]
    [string]$SiteUrl,

    [string]$SchemaPath = "../schemas/sharepoint-lists-schema.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
    throw "PnP.PowerShell is required. Install it with: Install-Module PnP.PowerShell -Scope CurrentUser"
}

$resolvedSchemaPath = Resolve-Path $SchemaPath
$schema = Get-Content $resolvedSchemaPath -Raw | ConvertFrom-Json

Connect-PnPOnline -Url $SiteUrl -Interactive

foreach ($list in $schema.lists) {
    $existingList = Get-PnPList -Identity $list.title -ErrorAction SilentlyContinue
    if (-not $existingList) {
        Add-PnPList -Title $list.title -Template GenericList -OnQuickLaunch:$false | Out-Null
    }

    foreach ($field in $list.fields) {
        $existingField = Get-PnPField -List $list.title -Identity $field.internalName -ErrorAction SilentlyContinue
        if (-not $existingField) {
            $required = [bool]$field.required
            Add-PnPField `
                -List $list.title `
                -DisplayName $field.displayName `
                -InternalName $field.internalName `
                -Type $field.type `
                -Required:$required `
                -AddToDefaultView | Out-Null
        }

        $values = @{}
        if ($field.indexed) { $values["Indexed"] = $true }
        if ($field.unique) { $values["EnforceUniqueValues"] = $true }
        if ($null -ne $field.decimals) { $values["Decimals"] = [int]$field.decimals }
        if ($values.Count -gt 0) {
            Set-PnPField -List $list.title -Identity $field.internalName -Values $values | Out-Null
        }
    }
}
