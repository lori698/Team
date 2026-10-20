<#
.SYNOPSIS  Run one employee headlessly on a task (used by schedules, or manually).
.EXAMPLE   .\run-agent.ps1 -Agent chief-of-staff -Prompt "Process my handoffs inbox"
#>
param(
    [Parameter(Mandatory)][string]$Agent,
    [string]$Prompt = 'Check your handoffs inbox and the board, then do any work assigned to you.'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not (Test-Path "$root\.claude\agents\$Agent.md")) { throw "Unknown agent '$Agent'" }
$logDir = Join-Path $root "agents\$Agent\work\logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir ("{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))

Push-Location $root
try {
    # Headless run as the named subagent; permissions come from the agent's tools list.
    claude --agent $Agent -p $Prompt 2>&1 | Tee-Object -FilePath $log
} finally { Pop-Location }
