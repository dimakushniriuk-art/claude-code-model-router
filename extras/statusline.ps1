# Claude Code status line for Windows PowerShell: model | session cost | context used | cache hit ratio
# Installed by install.ps1. Reads the session JSON from stdin.
$ErrorActionPreference = "SilentlyContinue"
$raw = [Console]::In.ReadToEnd()
try { $d = $raw | ConvertFrom-Json } catch { Write-Output "statusline: bad input"; exit 0 }

$parts = @()
$name = $d.model.display_name
if (-not $name) { $name = "?" }
$parts += $name

$cost = 0
if ($d.cost.total_cost_usd) { $cost = [double]$d.cost.total_cost_usd }
$parts += ('$' + [math]::Round($cost, 2).ToString([Globalization.CultureInfo]::InvariantCulture))

$ctx = $d.context_window.used_percentage
if ($null -ne $ctx) { $parts += ("ctx " + [math]::Floor([double]$ctx) + "%") } else { $parts += "ctx -" }

$hit = $d.prompt_cache.hit_ratio
if ($null -ne $hit) { $parts += ("cache " + [math]::Floor([double]$hit * 100) + "%") }

if ($d.agent.name) { $parts += ("agent " + $d.agent.name) }

Write-Output ($parts -join " | ")
