param(
    [Parameter(Mandatory = $true)]
    [string]$SiteUrl,

    [string]$ReferenceDataPath = "../schemas/reference-data"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
    throw "PnP.PowerShell is required. Install it with: Install-Module PnP.PowerShell -Scope CurrentUser"
}

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
