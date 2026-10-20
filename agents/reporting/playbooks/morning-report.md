# Playbook: morning report draft

When: asked for the morning report or a position update on the BYOD 243 programme.

Steps:
1. Read `PROGRAMME_STATE.md`, `orchestration\programme\SUMMARY.json`, `runner\STATUS_BY_PROCEDURE.csv`, `DECISIONS_NEEDED.csv` in `C:\claude\Project\REPORTING`.
2. Check the file dates. If the snapshot is older than the latest decision files, say so at the top.
3. Open the latest `reports\BYOD_243_Morning_Report_*.md` and copy its layout.
4. Write the draft to `agents/reporting/work/Morning_Report_<date>_DRAFT.md`.
   - Order: risks and blockers, decisions needed (with owner), position table, what changed since last report, next actions.
   - Counts must come from the files. Mark anything you could not refresh.
   - "Verified on real D365 data" stays at what the files say; do not round up.
5. Report to Lori in short bullets: top three risks, decisions needed, path to the draft.

Done when: draft saved, counts traceable to files, contradictions between files listed.
