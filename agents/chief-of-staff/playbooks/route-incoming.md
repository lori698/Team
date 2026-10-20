# Playbook: route incoming work

When: new files in `handoffs/chief-of-staff/` or `inbox-copilot/`, or Lori gives an instruction.

Steps:
1. Read `company/roster.md` and the routing table in job.md.
2. List new items. For digests, skip files already in `agents/chief-of-staff/work/processed.md`.
3. For each item decide: owner, urgency (High / Normal / Low), and whether it needs a decision from Lori.
4. Hand off with `scripts/handoff.ps1`. Title is the action. Body has source, what is asked, deadline, and what "done" looks like.
5. Items with no clear owner, or needing Lori, go to the "Decisions needed" list in the briefing. Do not guess an owner.
6. Anything that looks like an external send, spend, or deletion: create an approval request from `approvals/TEMPLATE.md` in `approvals/pending/`. Do not act.
7. Append each processed digest filename and date to `agents/chief-of-staff/work/processed.md`.
8. Update `board/board.md`.

Done when: every new item has one owner on the board or a line in "Decisions needed", and processed.md is updated.
