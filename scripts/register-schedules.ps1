<#
.SYNOPSIS  Register enabled jobs from schedules/schedules.json as Windows Scheduled Tasks (daily, current user).
           Use -Remove to delete them. Use -WhatIf to preview.
#>
param([switch]$Remove, [switch]$WhatIf)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$cfg = Get-Content "$root\schedules\schedules.json" -Raw | ConvertFrom-Json

foreach ($j in $cfg.jobs) {
    $taskName = "AITeam-$($j.name)"
    if ($Remove -or -not $j.enabled) {
        if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
            if ($WhatIf) { Write-Host "Would remove $taskName" } else { Unregister-ScheduledTask -TaskName $taskName -Confirm:$false; Write-Host "Removed $taskName" }
        }
        continue
    }
    $arg = "-NoProfile -File `"$PSScriptRoot\run-agent.ps1`" -Agent $($j.agent) -Prompt `"$($j.prompt -replace '"','\"')`""
    if ($WhatIf) { Write-Host "Would register $taskName daily $($j.time): pwsh $arg"; continue }
    $action = New-ScheduledTaskAction -Execute 'pwsh.exe' -Argument $arg -WorkingDirectory $root
    $trigger = New-ScheduledTaskTrigger -Daily -At $j.time
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Force | Out-Null
    Write-Host "Registered $taskName daily at $($j.time)"
}
