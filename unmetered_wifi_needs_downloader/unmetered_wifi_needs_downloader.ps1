# --- CONFIGURATION ---
$LinkFile = "C:\Users\YourName\Documents\downloads.txt"
$DownloadFolder = "C:\Users\israelolawuyi.OVERWATCH886\Downloads\Autodownloads"

# 1. Load Windows Networking Framework
[void][Windows.Networking.Connectivity.NetworkInformation, Windows, ContentType = WindowsRuntime]

# 2. Check Network Cost
$Connection = [Windows.Networking.Connectivity.NetworkInformation]::GetInternetConnectionProfile()

if ($Connection -eq $null) {
    Write-Host "No Internet. Exiting."
    exit
}

$Cost = $Connection.GetConnectionCost()

# ONLY run if Unrestricted (Unmetered)
if ($Cost.NetworkCostType -ne 'Unrestricted') {
    Write-Host "Connection is METERED. Aborting to save data."
    exit
}

# 3. Check if file exists and has links
if (-not (Test-Path $LinkFile)) {
    Write-Host "Download file not found."
    exit
}

$Links = Get-Content $LinkFile
if ($Links.Count -eq 0) {
    Write-Host "No links to download."
    exit
}

# Create folder if missing
if (-not (Test-Path $DownloadFolder)) {
    New-Item -ItemType Directory -Force -Path $DownloadFolder | Out-Null
}

$FailedLinks = @()

# 4. Loop through links
foreach ($Link in $Links) {
    if ([string]::IsNullOrWhiteSpace($Link)) { continue }

    try {
        $FileName = Split-Path $Link -Leaf
        $DestPath = Join-Path $DownloadFolder $FileName
        
        Write-Host "Downloading: $FileName"
        
        # BITS TRANSFER: The magic command that handles resumes/interruptions
        Start-BitsTransfer -Source $Link -Destination $DestPath -ErrorAction Stop
        
        Write-Host "Success."
    }
    catch {
        Write-Warning "Failed to download $Link. Error: $_"
        $FailedLinks += $Link
    }
}

# 5. Rewrite the file
# We overwrite the file with ONLY the links that failed.
# If all succeeded, the file becomes empty.
$FailedLinks | Set-Content $LinkFile