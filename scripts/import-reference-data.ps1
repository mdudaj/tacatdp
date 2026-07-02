param(
    [Parameter(Mandatory = $true)]
    [string]$SiteUrl,

    [string]$ReferenceDataPath = "../schemas/reference-data"
)

$ErrorActionPreference = "Stop"

function Ensure-PnPPowerShell {
    if ($PSVersionTable.PSEdition -eq "Desktop") {
        throw "PnP.PowerShell requires PowerShell 7+. Run this script with pwsh, or use import-reference-data.cmd."
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

$resolvedReferencePath = Resolve-Path $ReferenceDataPath
Connect-PnPOnline -Url $SiteUrl -Interactive

Get-ChildItem -Path $resolvedReferencePath -Filter "*.csv" | ForEach-Object {
    $listTitle = $_.BaseName
    $rows = Import-Csv $_.FullName
    Write-Host "Importing $($rows.Count) rows into $listTitle"

    foreach ($row in $rows) {
        $values = @{}
        foreach ($property in $row.PSObject.Properties) {
            if ($property.Value -ne $null -and $property.Value -ne "") {
                $values[$property.Name] = $property.Value
            }
        }
        if ($values.ContainsKey("ChoiceListName")) {
            $values["Title"] = "{0}-{1}" -f $values["ChoiceListName"], $values["ChoiceValue"]
        } elseif ($values.ContainsKey("ChoiceValue")) {
            $values["Title"] = $values["ChoiceValue"]
        }
        Add-PnPListItem -List $listTitle -Values $values | Out-Null
    }
}
