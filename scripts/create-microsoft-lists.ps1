param(
    [Parameter(Mandatory = $true)]
    [string]$SiteUrl,

    [string]$SchemaPath = "../schemas/sharepoint-lists-schema.json",

    [string]$ClientId = $env:ENTRAID_APP_ID,

    [ValidateSet("Interactive", "DeviceLogin", "OSLogin")]
    [string]$AuthMode = "Interactive",

    [int]$MaxColumnsPerList = 300
)

$ErrorActionPreference = "Stop"

function Ensure-PnPPowerShell {
    if ($PSVersionTable.PSEdition -eq "Desktop") {
        throw "PnP.PowerShell requires PowerShell 7+. Run this script with pwsh, or use create-microsoft-lists.cmd."
    }

    try {
        Import-Module PnP.PowerShell -ErrorAction Stop
        return
    } catch {
        Write-Host "PnP.PowerShell is not available in this PowerShell profile. Installing for CurrentUser..."
    }

    $gallery = Get-PSRepository -Name PSGallery -ErrorAction SilentlyContinue
    if ($gallery -and $gallery.InstallationPolicy -ne "Trusted") {
        Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
    }

    Install-Module PnP.PowerShell -Scope CurrentUser -Force -AllowClobber
    Import-Module PnP.PowerShell -ErrorAction Stop
}

Ensure-PnPPowerShell

$resolvedSchemaPath = Resolve-Path $SchemaPath
$schema = Get-Content $resolvedSchemaPath -Raw | ConvertFrom-Json

function Resolve-PnPClientId {
    if (-not [string]::IsNullOrWhiteSpace($ClientId)) {
        return $ClientId
    }

    $fallbackNames = @("ENTRAID_CLIENT_ID", "PNP_CLIENT_ID")
    foreach ($name in $fallbackNames) {
        $value = [Environment]::GetEnvironmentVariable($name)
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }
    }

    throw @"
PnP.PowerShell now requires a ClientId for interactive authentication.

Create or use an approved Entra ID App Registration, then rerun with:
  .\create-microsoft-lists.cmd -SiteUrl "$SiteUrl" -ClientId "<application-client-id>"

You can also set ENTRAID_APP_ID, ENTRAID_CLIENT_ID, or PNP_CLIENT_ID.
If the popup login is unsupported on this machine, add -AuthMode DeviceLogin.
"@
}

function Test-ListColumnLimits {
    param(
        [Parameter(Mandatory = $true)]
        $Schema,

        [Parameter(Mandatory = $true)]
        [int]$Limit
    )

    foreach ($list in $Schema.lists) {
        $fieldCount = @($list.fields).Count
        if ($fieldCount -gt $Limit) {
            throw "List '$($list.title)' defines $fieldCount generated columns, which exceeds the configured limit of $Limit. Split this list before importing."
        }
        if ($fieldCount -gt ($Limit - 25)) {
            Write-Warning "List '$($list.title)' defines $fieldCount generated columns and is close to the configured limit of $Limit."
        }
    }
}

function Connect-TacatdpPnPOnline {
    $resolvedClientId = Resolve-PnPClientId

    switch ($AuthMode) {
        "Interactive" {
            Connect-PnPOnline -Url $SiteUrl -Interactive -ClientId $resolvedClientId
        }
        "DeviceLogin" {
            Connect-PnPOnline -Url $SiteUrl -DeviceLogin -ClientId $resolvedClientId
        }
        "OSLogin" {
            Connect-PnPOnline -Url $SiteUrl -OSLogin -ClientId $resolvedClientId
        }
    }
}

Test-ListColumnLimits -Schema $schema -Limit $MaxColumnsPerList
Connect-TacatdpPnPOnline

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
