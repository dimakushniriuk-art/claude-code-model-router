# model-router installer for Windows PowerShell (5.1+) and PowerShell 7.
#
# One line, in PowerShell:
#   irm https://raw.githubusercontent.com/dimakushniriuk-art/claude-code-model-router/main/install.ps1 | iex
#
# What it does (each step is skipped safely if already done):
#   1. adds the marketplace and installs the model-router plugin
#   2. sets Sonnet as the default main model in %USERPROFILE%\.claude\settings.json
#   3. installs a PowerShell status line (model | cost | context | cache)
# A backup of settings.json is written next to it before any change.
# Opt out of steps 2 or 3 by setting $env:MR_SKIP_MODEL = "1" or $env:MR_SKIP_STATUSLINE = "1" first.

$ErrorActionPreference = "Stop"
$repo = "dimakushniriuk-art/claude-code-model-router"
$raw  = "https://raw.githubusercontent.com/$repo/main"

function Say($msg, $color = "Cyan") { Write-Host $msg -ForegroundColor $color }

# --- 0. Claude Code must be installed -----------------------------------------
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Say "Claude Code (the 'claude' command) was not found." "Red"
    Say "Install it first: https://code.claude.com/docs/en/setup  then run this script again." "Yellow"
    return
}

# --- 1. Plugin ----------------------------------------------------------------
Say "1/3  Installing the model-router plugin..."
& claude plugin marketplace add $repo
if ($LASTEXITCODE -ne 0) { Say "     Marketplace may already be added, continuing." "Yellow" }
& claude plugin install "model-router@model-router"
if ($LASTEXITCODE -ne 0) {
    & claude plugin update "model-router@model-router"
    if ($LASTEXITCODE -ne 0) { Say "     Plugin install failed. Run: claude plugin install model-router@model-router" "Red"; return }
}
Say "     Plugin ready." "Green"

# --- settings.json helpers ----------------------------------------------------
$claudeDir    = Join-Path $env:USERPROFILE ".claude"
$settingsPath = Join-Path $claudeDir "settings.json"
if (-not (Test-Path $claudeDir)) { New-Item -ItemType Directory -Path $claudeDir | Out-Null }

function Read-Settings {
    if (Test-Path $settingsPath) {
        $text = [IO.File]::ReadAllText($settingsPath)
        if ($text.Trim().Length -gt 0) { return ($text | ConvertFrom-Json) }
    }
    return (New-Object PSObject)
}

function Write-Settings($obj) {
    if (Test-Path $settingsPath) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        Copy-Item $settingsPath "$settingsPath.bak-$stamp"
    }
    $json = $obj | ConvertTo-Json -Depth 32
    # UTF-8 without BOM
    [IO.File]::WriteAllText($settingsPath, $json, (New-Object System.Text.UTF8Encoding $false))
}

$settings = Read-Settings
$changed = $false

# --- 2. Sonnet as main model --------------------------------------------------
if ($env:MR_SKIP_MODEL -ne "1") {
    Say "2/3  Setting Sonnet as the main model..."
    $settings | Add-Member -NotePropertyName "model" -NotePropertyValue "sonnet" -Force
    $changed = $true
} else { Say "2/3  Skipped (MR_SKIP_MODEL=1)." "Yellow" }

# --- 3. Status line -----------------------------------------------------------
if ($env:MR_SKIP_STATUSLINE -ne "1") {
    Say "3/3  Installing the status line..."
    $slPath = Join-Path $claudeDir "statusline.ps1"
    Invoke-WebRequest -UseBasicParsing -Uri "$raw/extras/statusline.ps1" -OutFile $slPath
    # Forward slashes: Claude Code may run this through Git Bash, where backslashes are escapes.
    $slPathFwd = $slPath -replace '\\', '/'
    $cmd = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$slPathFwd`""
    $statusLine = [PSCustomObject]@{ type = "command"; command = $cmd }
    $settings | Add-Member -NotePropertyName "statusLine" -NotePropertyValue $statusLine -Force
    $changed = $true
} else { Say "3/3  Skipped (MR_SKIP_STATUSLINE=1)." "Yellow" }

if ($changed) { Write-Settings $settings; Say "     Saved $settingsPath (backup kept next to it)." "Green" }

Say ""
Say "Done. Restart Claude Code, then type /agents to see model-router:reader, coder and architect." "Green"
