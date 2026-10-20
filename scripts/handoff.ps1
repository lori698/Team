<#
.SYNOPSIS  Pass a task from one agent (or the owner) to another and put it on the board.
.EXAMPLE   .\handoff.ps1 -From chief-of-staff -To inbox-triage -Title "Clear overnight inbox" -Body "Sort and draft replies; see voice.md"
#>
param(
    [Parameter(Mandatory)][string]$From,
    [Parameter(Mandatory)][string]$To,
    [Parameter(Mandatory)][string]$Title,
    [string]$Body = ''
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$inbox = Join-Path $root "handoffs\$To"
if (-not (Test-Path (Join-Path $root "agents\$To")) -and $To -ne 'owner') { throw "Unknown agent '$To'. Check company/roster.md" }
New-Item -ItemType Directory -Force $inbox | Out-Null

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$id = "T$stamp"
$file = Join-Path $inbox "$stamp-from-$From.md"
@"
# $Title
- id: $id
- from: $From
- to: $To
- date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')

$Body
"@ | Set-Content $file -Encoding utf8

$board = Join-Path $root 'board\board.md'
$lines = Get-Content $board
$out = foreach ($l in $lines) {
    $l
    if ($l -eq '## To Do') { "- [$id] $Title — owner: $To — from: $From — $(Get-Date -Format 'yyyy-MM-dd')" }
}
$out | Set-Content $board -Encoding utf8
Write-Host "Handed off $id to $To -> $file"
