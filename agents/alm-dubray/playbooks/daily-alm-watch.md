# Playbook: daily ALM watch

When: asked for the ALM position, or on the morning schedule.

Steps:
1. Try the dashboard URL in agents/alm-dubray/job.md. If it needs a login, use the newest export in `C:\claude\Project\gtm` and state its date.
2. Build the list: blocked, no owner, no movement 7+ days, waiting on Lori to verify in production, release-tagged but off track, waiting on FTT.
3. Write `agents/alm-dubray/work/ALM_Watch_<date>.md`:
   - Risks and blockers first, each as issue, impact, dependency, action, owner, risk.
   - Then decisions needed from Lori.
   - Then what changed since the previous watch file.
4. Draft any ticket comments or FTT messages into the same file. Do not post.
5. Hand GTM-related tickets to gtm-signoff with `scripts/handoff.ps1`.

Done when: the file is saved, every item shows its source and date, nothing was posted to ADO.

