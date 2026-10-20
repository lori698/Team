<#
.SYNOPSIS  Create a new AI employee: workspace, subagent definition, roster entry, handoff inbox.
.EXAMPLE   .\new-agent.ps1 -Name inbox-triage -Title "Inbox Triage" -Mission "Sort the inbox and draft replies" -Tools "Read,Write,Edit,Glob,Grep"
#>
param(
    [Parameter(Mandatory)][ValidatePattern('^[a-z0-9-]+$')][string]$Name,
    [Parameter(Mandatory)][string]$Title,
    [Parameter(Mandatory)][string]$Mission,
    [string]$Tools = 'Read,Write,Edit,Glob,Grep',
    [string]$Model = 'sonnet'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$dir = Join-Path $root "agents\$Name"
if (Test-Path $dir) { throw "Agent '$Name' already exists at $dir" }

foreach ($d in @("$dir\playbooks", "$dir\work", "$root\handoffs\$Name", "$root\.claude\agents")) {
    New-Item -ItemType Directory -Force $d | Out-Null
}

@"
# Job Description — $Title

**Agent name:** $Name
**Mission:** $Mission

## Responsibilities
-

## Not my job (hand off instead)
-

## Allowed tools
$Tools

## Boundaries
- Write only inside agents/$Name/, handoffs/, board/, approvals/pending/.
- Follow the hard safeguards in CLAUDE.md. Draft external messages; never send them.
"@ | Set-Content "$dir\job.md" -Encoding utf8

@"
# Notebook — $Title

Lessons learned. One entry per lesson: date, what happened, what to do next time.
"@ | Set-Content "$dir\notebook.md" -Encoding utf8

@"
# Playbook: example

When: <trigger>
Steps:
1.
Done when:
"@ | Set-Content "$dir\playbooks\example.md" -Encoding utf8

@"
---
name: $Name
description: $Title. $Mission
tools: $Tools
model: $Model
---
You are $Title, an employee on the owner's AI team. Your workspace is agents/$Name/ under the team root.

Before any task, read in order: company/owner.md, company/voice.md, company/roster.md, company/rules.md, agents/$Name/job.md, agents/$Name/notebook.md. Then check handoffs/$Name/ and board/board.md. Follow the safeguards in CLAUDE.md. If a task belongs to another role, hand it off with scripts/handoff.ps1 instead of doing it.
"@ | Set-Content "$root\.claude\agents\$Name.md" -Encoding utf8

Add-Content "$root\company\roster.md" "| $Name | $Title | $Mission | agents/$Name/ |" -Encoding utf8
Write-Host "Created agent '$Name'. Edit agents\$Name\job.md to refine the role."
