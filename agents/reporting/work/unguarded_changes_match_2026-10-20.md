# Match of 10 unlogged MDW02 changes (19 Oct) to the deploy record

Handoff T20261020-080428. Files only. No database access, no project file edited. Compared against PROGRAMME_STATE.md, QUEUE.csv, STATUS_BY_PROCEDURE.csv, `ledger\` (results.csv, compare_results.csv), `validation\run_2026-10-19\OVERNIGHT_LEDGER.csv` and `MORNING_REPORT.md`, the deploy folder, and `scripts\guard\guard_log.txt`.

## Risks first
1. **The record for these 10 is one file, written by the AI session itself.** PROGRAMME_STATE.md (last edited 19 Oct 14:25), QUEUE.csv (16:40) and the `ledger\` folder (last write 16:40) all pre-date every change in the list. Nothing independent (no guard line, no VERIFY_RESULT file, no bundle) covers them. CONFIRMED.
2. **Two creates have no record of the event at all**: table Book_Sales_Stock_Top500_Franchise_BYOD (15:25) and table Lookback_Days_Prior_BYOD (23:47). See below.
3. **Nothing exists after 22:13 in the overnight ledger.** The 23:47 change is 94 minutes after its last line. CONFIRMED.
4. **Guard coverage.** The last guard decision line is 19 Oct 21:2x (lines 6651 to 6654). The next is 20 Oct 06:46 (the guard self-test). So every change from 21:37 on has no guard line. CONFIRMED from the log. The ledger itself says the hook was `{}` before 19:52 and Lori later changed the permission mode (21:40 line). Why settings.json was emptied at 21:36 is UNKNOWN; I found nothing in the files that explains it.
5. Several of these were deployed or run by Lori in SSMS (22:04 line says so for Mins). SSMS does not go through the guard at all, so a missing guard line is not evidence either way. INFERRED.

## Result per object

| # | Object | Change (time) | Verdict | Record (file, time) | Tag |
|---|---|---|---|---|---|
| 1 | Book_Sales_Stock_Top500_Franchise_BYOD (table) | created 15:25 | **No record of the create.** Possible side effect of a run of the Franchise proc | Ledger line 8 and MORNING_REPORT row 2 say the Franchise proc ran and produced 0 rows, but give no run time. The proc already existed live from 14 Oct, so an earlier-version run could have created the table. 15:25 is also the start of the Ecomm_Books_Fulfilment run (ledger line 15, 15:25 to 15:47) | INFERRED at best; cause UNKNOWN |
| 2 | Book_8wk_Wh_Fra_Sales_BYOD (table) | created 15:55 | **Matches a recorded run** (execution, not a deploy) | OVERNIGHT_LEDGER.csv line 14: SP_Book_8wk_Wh_Fra_Sales_BYOD "execute, DONE (data gap), ran 15:47 to 15:56, table has 1 row" | CONFIRMED that the run is recorded; INFERRED that the run created the table |
| 3 | SP_Book_SalesStock_Top500_Franchise_BYOD (proc) | altered 16:54 | **Matches a recorded deploy** | OVERNIGHT_LEDGER.csv line 8: "direct-source rewrite deployed, modify_date 2026-10-19 16:54:34, backup row present, 23141 chars". Source file `validation\run_2026-10-18\packs\TILL_02_SP_Book_SalesStock_Top500_Franchise_BYOD\02_DEPLOY_ARMED_...sql` last written 19 Oct 16:54. Not in PROGRAMME_STATE.md or QUEUE.csv (QUEUE.csv still says NOT DEPLOYED, STATUS_BY_PROCEDURE.csv says "Not deployed: implementation open") | CONFIRMED (time and pack agree). Register is stale |
| 4 | SP_Book_Sales_Nday_BYOD (proc) | created 21:37 | **Matches a recorded deploy** | OVERNIGHT_LEDGER.csv line 35: "redeploy with Lookback column fix, modify_date 21:37:29". First create at 21:05:06 is line 26 and a guard ALLOW "approved script (fingerprint)" at 21:05:05. The 21:37 redeploy has no guard line | CONFIRMED in ledger; guard line absent |
| 5 | SP_PO_Lines_Books_BYOD (proc) | created 21:37 | **Matches a recorded deploy** | OVERNIGHT_LEDGER.csv line 36: "create, modify_date 21:37:35 (not run)". Draft hash line 32 (E116C5FF...). Pack `packs\BOOKS_LINK_05_SP_PO_Lines_Books_BYOD` | CONFIRMED in ledger; guard line absent |
| 6 | SP_Book_Mins_Report_BYOD (proc) | created 22:05 | **Matches a recorded deploy** | OVERNIGHT_LEDGER.csv line 39: "collation fix deployed (local-read version), modify_date 22:05:27". Pack `BOOKS_LINK_01b_..._LOCAL`. Earlier version created 18:22:45 (line 9) | CONFIRMED in ledger |
| 7 | Book_Mins_Rpt_BYOD (table) | created 22:05 | **Matches a recorded run, with a 1 minute difference** | OVERNIGHT_LEDGER.csv line 40: Mins executed by Lori in SSMS, ended 22:06:18, "Book_Mins_Rpt_BYOD 131486 rows 47 columns". Line 38: the 22:04 run failed (collation), so a table creation at 22:05 fits the proc being re-created and run | INFERRED (table creation time vs run times not tied by a log line) |
| 8 | SP_Book_SalesStock_BYOD (proc) | altered 22:09 | **Matches a recorded deploy** | OVERNIGHT_LEDGER.csv line 43: "local-read version deployed, modify_date 22:09:26". Pack `BOOKS_LINK_07_SP_Book_SalesStock_BYOD_LOCAL` (dir written 22:09). First create 21:05:20 is line 27 | CONFIRMED in ledger; guard line absent |
| 9 | SP_Book_SalesStock_Top500_BYOD (proc) | altered 22:13 | **Matches a recorded deploy** | OVERNIGHT_LEDGER.csv line 44: "local-read version deployed (ALTER), modify_date 22:13:28". Pack `BOOKS_LINK_06_..._LOCAL` (dir written 22:12) | CONFIRMED in ledger; guard line absent |
| 10 | Lookback_Days_Prior_BYOD (table) | created 23:47 | **No record** | The Nday proc creates this table if it is missing (pack `BOOKS_LINK_03...\02_DEPLOY_SP_Book_Sales_Nday_BYOD.sql` lines 50 to 51; same in RUN_BYOD_BOOKS_ALL_IN_ORDER.sql line 403). So a run of SP_Book_Sales_Nday_BYOD (or that CREATE block) happened at or just before 23:47. No ledger line, no guard line, no log of that run. The ledger line 31 (21:31) says the table "not yet created". `RUN_REMAINING_BYOD_PROCEDURES.sql` (written 22:42) has `EXEC dbo.SP_Book_Sales_Nday_BYOD @LookbackDays = 30` at line 71, so a run of that script in SSMS is a candidate | INFERRED candidate only; who and how UNKNOWN |

## Count
- Matches a recorded deploy: 6 (#3, #4, #5, #6, #8, #9). All six are in OVERNIGHT_LEDGER.csv with the same modify_date; none in PROGRAMME_STATE.md, QUEUE.csv, `ledger\` or a bundle.
- Matches a recorded run (table created by a run): 2 (#2, #7), INFERRED.
- No record: 2 (#1, #10). Both are tables. Both fit a procedure run, neither has a run time on file.

## Other findings
- The 6 "not yet matched" items in the source note: SP_Wholesale_Invoiced_Prev_Week_BYOD 21:04:49 and SP_Book_Sales_50day_BYOD 21:05:01 DO match (ledger lines 24 and 25, and guard ALLOW fingerprint lines at 21:04:40 and 21:04:53). SP_Retail_OHQ_New_BYOD 12:04 matches PROGRAMME_STATE.md line 89 (person edit, @TestRecipient default only). SP_EDGAR_Update_Remain_PO_Qty2_BYOD and SP_NonBook_Pricing_BYOD at 14:00 match bundle_2026-10-19c (ledger results.csv 14:01 "DEPLOYED: bundle_2026-10-19c, definition verified"; VERIFY_RESULT_2026-10-19_1401.csv). Tables WHS_Stock_Book_Opening_BYOD and RetailOhq_Book_Linear_BYOD at 12:07: I found no record; I did not search past the files above. UNKNOWN.
- The deploy script path in the guard log for the 21:05 deploys is `...\fixes\direct_src\books_link\...`, not the `validation\run_2026-10-19\packs\` copies. I did not compare file contents or hashes, so I cannot say the live text equals the pack text. UNKNOWN.
- The Nday 21:37 redeploy used a script fixed after 21:31, but the pack file in `packs\BOOKS_LINK_03_...` was last written 21:10. Which file was deployed is UNKNOWN from files alone.
- Stale: PROGRAMME_STATE.md says 232 live, 11 not live, and does not mention any 19 Oct evening deploy. QUEUE.csv and STATUS_BY_PROCEDURE.csv still list Top500_Franchise as NOT DEPLOYED. `bundle_2026-10-19d` is empty (BUNDLE_19D_RECONCILIATION.md) and is not the source of any of these.
- Backups: ledger line 8 says a backup row exists for Top500_Franchise. No backup is claimed for the other altered procs (#8, #9 were ALTERs of live procs). UNKNOWN whether rollback copies exist.

## Decisions for Lori (nothing here is concluded to be a breach)
1. **Who ran what at 15:25 and 23:47?** Tables #1 and #10 have no record. Did you run SP_Book_Sales_Nday_BYOD (or RUN_REMAINING_BYOD_PROCEDURES.sql) in SSMS around 23:45, and a Franchise proc run around 15:25? A yes closes both.
2. **Why was settings.json emptied at 21:36?** Cause unknown. Do you want it checked and confirmed restored, as it was at 19:52?
3. **Accept the ledger as the record for the 6 deploys,** or want a read-only definition dump (VERIFY_RESULT style) for #3 to #9 to confirm live text equals the packs? That needs a session started in the project with database access.
4. **Register update.** Hand PROGRAMME_STATE.md / QUEUE.csv / STATUS_BY_PROCEDURE.csv catch-up (Top500_Franchise now deployed, Nday, PO_Lines_Books, Mins_Report, 50day new) to a session in the project folder?
5. **Rollback copies** for the altered procs #8 and #9: confirm backups exist before more changes.
