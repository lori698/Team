# BYOD 243: where we are (morning report, 20 Oct 2026) DRAFT

**DRAFT. TEST INCOMPLETE until the AX compares are complete.** Prepared by the reporting employee for Lori Ryan. File-only: no SQL run, nothing refreshed from MDW02, nothing sent.

**Freshness warning.** The newest project evidence I could read is dated 19 Oct 2026: runner PROGRESS.md built 19 Oct 15:03, SUMMARY.json built 19 Oct 16:40 (its snapshot field still says 2026-10-18), DECISIONS_NEEDED.csv last row 19 Oct 15:03, huddle addendum 19 Oct afternoon. Nothing dated 20 Oct was found. I could not refresh the MDW02 snapshot, the deployment ledger, or anything that today's work may have changed. All counts below are as at 19 Oct.

D365 go-live is after Christmas. Priority is delivering the stored procedures and reports for the business as soon as possible. "Verified on real D365 data" stays at what the files say: **0 of 243**.

## 1. Risks and blockers (first)

| # | Issue | Impact | Dependency | Action | Owner | Risk |
|---|---|---|---|---|---|---|
| 1 | The SQL guard hook is empty in the project settings (`C:\claude\Project\REPORTING\.claude\settings.json` has `"hooks": {}`). The same file also allows `Bash(sqlcmd:*)` with no restriction. PROGRESS.md says the runner stopped at 19 Oct 15:03 with GUARD_FAILED because there is no PreToolUse hook to run_guard.ps1. | No guard on any SQL run from the project. Unattended runner is stopped (flag STOP), so compare and queue work stopped from 15:03 on 19 Oct. | Lori restores the hook from a session started in the project folder. I have not changed it. | Lori to decide and restore, then re-run the runner preflight. Also decide whether to review what ran while the hook was off (15 to 17 Oct was already an open question; today's gap is new). | Lori | HIGH |
| 2 | Nothing is verified on real D365 data (0 of 243). 124 procedures cannot be tested until D365 holds the data, 13 more wait on unknown D365 fields. | The business cannot rely on any report yet. Go-live is after Christmas but the business wants the reports ASAP. | The business creates test data (B2C Easons, Dubray, B2B, Eros test orders pending); Ryan Blom pushes entities. | Chase the test orders and the missing entities with written dates. | Ryan Blom, the business, Lori | HIGH |
| 3 | 24 procedures were deployed on Lori's approval before their AX compare finished (bundles 18b, 18c). Compares are still being completed. No coding error found so far, but not proven. | A conversion defect could sit live. | AI agent finishes compares; runner is stopped (risk 1). | Restart compares once the guard is back. Roll back any proven defect from `dbo.T2_Backup_BYOD_20261012`. | AI agent, Lori | MEDIUM |
| 4 | 4 franchise procedures plus Retail_OHQ_New are not deployed: franchise stock and till data lives in MDW, not AX or D365 (huddle item 4). Auth_Grp_Vend runs on old 14 Oct text because the approved redraft needs a chain table that does not exist in MDW02. | Franchise reporting not delivered. | Lori sends Priscilla the list; Priscilla sets up the MDW02 feed. | Send `Franchise_Data_Requirements_2026-10-19` to Priscilla and get a written date. | Lori, Priscilla | HIGH |
| 5 | Ecomm_NonBook_Catalog reads the unreachable Commerce server `sqlcluster01\easonslive`. Other reports have the same issue. | Procedure cannot be deployed. Go-live read of Commerce data is undecided. | Priscilla's catalog metadata to Lori and Claude; Piotr Piszczyk on the Commerce server. | Build the catalog feed into MDW01 and MDW02 (huddle item 5). | Lori, Priscilla, Piotr Piszczyk | MEDIUM |
| 6 | Missing D365 fields: MaximumPostingDifference, Disclaimer, Trading Imprint, PubDate. DevOps tickets 1556 and 1557 raised, third ticket has no number in the files. | 7 procedures cannot be fully verified. | Valentin raises and tracks tickets for Mindaugas; Ryan Blom pushes PubDate. | Get ticket numbers and dates in writing. | Valentin, Mindaugas, Ryan Blom | MEDIUM |
| 7 | Project agent files still reference the old path `C:\claude\REPORTING` (13 hits across 5 files in `.claude\agents`: ax-analyst, byod-conversion-reviewer, independent-quality-reviewer, reporting-governance, sql-test-reconciler). The project now lives in `C:\claude\Project\REPORTING`. RULES.md and `.claude\settings.json` permission entries also use the old path. | Agents can read or write the wrong location, or approvals do not match. | None. | Fix paths from a session in the project folder. Not changed by me. | Lori | MEDIUM |
| 8 | Interim email rule: every emailing procedure sends to lryan@Easons.com and PDiniz@easons.com only. Original recipients are kept only in the AX originals. | If not switched back at go-live, business recipients never get the reports. | Go-live checklist. | Add to the go-live checklist with an owner. | Lori | MEDIUM (at go-live) |
| 9 | Security: SMS gateway password sits in the live text of Ecomm_Order_Import_Check (PROGRAMME_STATE, 18 Oct). No record of rotation. | Credential exposure. | None. | Rotate it. | Lori | MEDIUM |
| 10 | 3 live procedures are quarantined because they send email (B2C_GiftCard_Weekly, DumpKey_Extract_Finance, Dubray_Open_Sales_101). Dubray_Open_Sales_101 has no recorded reason for the lock (19 Oct report). | Cannot be run or unlocked by the agent. | Lori decides post go-live email behaviour. | See decisions below. | Lori | LOW |

## 2. What changed since the last report

Compared with the 19 Oct morning report (evidence 19 Oct 08:27), PROGRAMME_STATE (18 Oct 21:30 header, with 19 Oct additions), and the later 19 Oct files.

| Change | Source and date | Tag |
|---|---|---|
| Live-awaiting-test count moved from 86 to 88; not-live open from 6 to 4; not-live column unknown stays 1. This fits EDGAR_Update_Remain_PO_Qty2 and NonBook_Pricing (bundle_2026-10-19c) now showing as Deployed: awaiting test. I did not read the deployment verify output, so the deployment itself is not confirmed by me. | runner\STATUS_BY_PROCEDURE.csv and PROGRESS.md (19 Oct 15:03) | INFERRED |
| Runner stopped at 19 Oct 15:03: GUARD_FAILED, STOP flag, database mode off. 27 live runs, 24.42 of 60 USD spent that day. | PROGRESS.md 19 Oct | CONFIRMED |
| Huddle decisions 1 to 11 recorded (19 Oct): Remain_PO_Qty2 first-run line accepted; eSchool_Push_Parked and NotifyMe_Counts retired; franchise via MDW; NonBook_Catalog feed from Priscilla's metadata; 3 missing-field tickets; PubDate with Ryan. | DECISIONS_2026-10-19_HUDDLE.md | CONFIRMED |
| Addendum: HOCLUPRODAXSQL reads repointed to BYOD; HOCLUBISQL01 cube stays after go-live; C001 decommissioned; TrueCommerce Watermark only; several test-data items dropped; Footfall condition added. | DECISIONS_2026-10-19_HUDDLE_ADDENDUM.md | CONFIRMED |
| Completed 19 Oct: RetailPeriodicDiscount republished (not re-checked by us); D365_BYOD_UAT timeout 600 to 1800 s; tickets 1556 and 1557; DumpKey_Extract_Finance run on D365 data (6 rows, C003 store 071); B2C_GiftCard_Weekly run empty (0 qualifying, needs an online gift card order). Run by people, not yet in the ledger. | Addendum | CONFIRMED (as reported by Lori) |
| Email rule added (Lori, 19 Oct pm): internal recipients only until go-live. | Addendum | CONFIRMED |
| Retail_OHQ_New altered by a person 19 Oct 12:04 (default @TestRecipient only). | PROGRAMME_STATE 19 Oct afternoon | CONFIRMED |
| New open compare questions: SuppProd_Upd_Multi_Mins (1 row differs by 1e-8, likely float versus decimal, not queried); Dubray_Ecomm_Range PORemain differs on 287 of 8488 rows (likely D365 PO data, not confirmed); Adjustments_C003 and C015 compare blocked by the guard; AXStockValueReport and Ecomm_Range_Mgmt compares exceed the 600 s timeout. | DECISIONS_NEEDED.csv 19 Oct 15:00 | CONFIRMED |
| Newer 19 Oct requests exist: `reports\requests_2026-10-19\for_Valentin_Wholesale_slow_run.md` and `Questions_slow_BYOD_reads_Val_Erick_Piotr.md`. I did not read them. | Glob only | UNKNOWN content |

Nothing is known for 20 Oct. Anything done since 19 Oct 16:40 is not reflected here.

## 3. Decisions needed from Lori

1. Restore the SQL guard hook in the project settings, then re-run the runner preflight. Owner: Lori. Do first.
2. Review whether anything ran unguarded (15 to 17 Oct, and since the hook went empty). Owner: Lori.
3. SuppProd_Upd_Multi_Mins: accept the 1e-8 difference or agree a 0.01 tolerance (agreed_by needed in writing). Owner: Lori.
4. Adjustments_C003 and C015: allow the compare scripts to be rewritten so each OPENQUERY body starts with SELECT or WITH? Owner: Lori.
5. Quarantined email procedures: what does email do after go-live (keep, re-target, remove)? Owner: Lori.
6. Ecomm_NonBook_Catalog: how Commerce data is read at go-live. Owner: Lori with Piotr Piszczyk.
7. Excel master reports (huddle item 9): how many reports are there? Owner: Lori (with Mike Courtney for reporting ownership).
8. Send the franchise data list to Priscilla (huddle item 4). Owner: Lori.
9. Approve the next bundle when ready: Retail_OHQ_New and Book_SalesStock_Top500_Franchise packs are held by a false builder finding; deploy needs Lori. Owner: Lori.
10. Close stale DECISIONS_NEEDED rows (Remain_PO_Qty2 accepted at huddle; NonBook_Pricing now deployed; about 80 runner permission rows are noise). Owner: Lori.

## 4. Position table (243 procedures)

Source: `orchestration\programme\runner\STATUS_BY_PROCEDURE.csv`, rows counted by status (244 lines including header); same numbers in PROGRESS.md (19 Oct 15:03). Not refreshed from MDW02.

| Status | Count | Tag |
|---|---|---|
| Deployed: awaiting test | 88 | CONFIRMED (file count) |
| Deployed: data-blocked (needs D365 data) | 124 | CONFIRMED |
| Deployed: column unknown | 13 | CONFIRMED |
| Not deployed: implementation open | 4 | CONFIRMED |
| Not deployed: column unknown | 1 | CONFIRMED |
| Live, quarantined | 3 | CONFIRMED |
| Retired or out of scope | 10 | CONFIRMED |
| **Total** | **243** | CONFIRMED (88+124+13+4+1+3+10) |
| Verified on real D365 data | 0 | CONFIRMED per files. DumpKey_Extract_Finance is a PASS candidate, not in the ledger. B2C_GiftCard_Weekly stays DATA PENDING. |
| Live now in MDW02 (including 8 retired that still exist) | 236 | INFERRED (243 minus 5 not deployed minus 2 retired not live; REMAINING_PROCEDURES also says 236) |
| AX compare complete for the 24 deployed without AX proof | Not stated | UNKNOWN (runner stopped; "none found so far") |
| Deployed after 19 Oct 16:40 | Not known | UNKNOWN |

The 5 not deployed: Book_SalesStock_Top500_Franchise, Ecomm_NonBook_Catalog, EDGAR_Add4a_Fran, Retail_OHQ_New (open); FRAN_EDGAR_Add_Items (column unknown). Plus FRAN_EDGAR_Auth_Grp_Vend is counted as deployed but runs old 14 Oct text; the approved redraft is not live.

Register status mix from SUMMARY.json (built 19 Oct 16:40): functional DATA PENDING 195, NOT TESTED 38, EXCEPTION APPROVED 10; safety REVIEW REQUIRED 137, PASS 102, QUARANTINED 3, NOT REVIEWED 1. Technical failure 7 and structural dependency pending 20. These are register views and do not map one to one to the table above.

## 5. Next actions with owners

| Owner | Next action |
|---|---|
| Lori | Restore the guard hook (decision 1); restart the runner after preflight; decisions 2 to 10 above; send franchise list to Priscilla; rotate the SMS password; go-live email checklist item. |
| Ryan Blom | Push PubDate (try EcoResProductAttributeValueStaging or V3Staging per PROGRAMME_STATE); push the missing entities; check why VendTableCube_DEStaging has no C003 or C015 rows; confirm RetailPeriodicDiscount republish columns. |
| Piotr Piszczyk | Commerce server (`sqlcluster01\easonslive`) answer for NonBook_Catalog and the go-live read; confirm NotifyMe retirement is recorded as done. |
| Priscilla | Franchise data into MDW02 (stock, TransactionHeader, TransactionEntry, Store); catalog metadata for NonBook_Catalog; confirm Retail_OHQ_New differences are D365 data. |
| Mindaugas | Investigate the three missing fields (tickets 1556, 1557 and the third). |
| Valentin | Confirm the third DevOps ticket number; raise and track the tickets; the slow BYOD read questions (reports\requests_2026-10-19). |
| Mike Courtney | Reporting owner: confirm the Excel master report count and the Master Data Reports BYOD folder approach (huddle item 9). |
| AI agent (through Lori) | After the guard is restored: finish compares for the 24, fix builder false finding on Retail_OHQ_New and Book_SalesStock_Top500_Franchise, rebase on the 19 Oct 12:04 live text. |

### Owner block: Ryan Blom
- Open: PubDate entity push (Ecomm_PreOrder, Ecomm_PreOrders_Expiring); franchise entity field (FRAN_EDGAR_Add_Items); vendor rows for C003 and C015.
- Needed: written date for each push. Verbal agreement does not close an item.

### Owner block: Piotr Piszczyk
- Open: Commerce server `sqlcluster01\easonslive` for Ecomm_NonBook_Catalog and the go-live position; MaximumPostingDifference need already confirmed (huddle item 10).
- Needed: written answer on how Commerce data is read at go-live.

## 6. Contradictions and stale facts between files

| # | Finding | Files and dates |
|---|---|---|
| 1 | Guard hook: PROGRAMME_STATE says the hook path was fixed 18 Oct 13:50 and the suite passed 143/143. The project `settings.json` now has `"hooks": {}` and PROGRESS.md (19 Oct 15:03) shows GUARD_FAILED. The state file is stale on this. | PROGRAMME_STATE.md (18 Oct 21:30); settings.json (current); PROGRESS.md |
| 2 | Position table: PROGRAMME_STATE shows 84 / 124 / 13 / 9 / 2 / 3 / 8 (18 Oct 21:23). The 19 Oct report shows 86 / 124 / 13 / 6 / 1 / 3 / 10. The status CSV and PROGRESS show 88 / 124 / 13 / 4 / 1 / 3 / 10. Three different snapshots. | PROGRAMME_STATE.md; Morning_Report_2026-10-19.md; STATUS_BY_PROCEDURE.csv |
| 3 | SUMMARY.json says 234 deployed and 9 not deployed, built 19 Oct 16:40 but with `"snapshot": "2026-10-18"`. The CSV implies 236 live and 5 not deployed. The REMAINING file says "the 236 deployed". | SUMMARY.json; STATUS_BY_PROCEDURE.csv; REMAINING_PROCEDURES_2026-10-19.csv |
| 4 | PROGRESS.md heading says "7 procedures not deployed" but the table above it shows 5, because 2 of the 7 were retired. Its sub-list (2+2+1) also sums to 5 with different wording. | PROGRESS.md 19 Oct 15:03 |
| 5 | 19 Oct report lists Remain_PO_Qty2 and NonBook_Pricing as not live (ready to deploy in 19c). The CSV shows both as deployed. Likely deployed after the report; the DECISIONS_NEEDED rows for both are still OPEN. | Morning_Report_2026-10-19.md; STATUS_BY_PROCEDURE.csv; DECISIONS_NEEDED.csv |
| 6 | PROGRAMME_STATE next action 4 says "switch on the unattended runner", but the same file says it was started 19 Oct 08:31, and PROGRESS shows it stopped 15:03. | PROGRAMME_STATE.md; PROGRESS.md |
| 7 | PROGRAMME_STATE points to `reports\BYOD_243_Morning_Report_2026-10-19_SENT.pdf`. The report files are now in `reports\old\`. The latest morning report .md I used is `reports\old\BYOD_243_Morning_Report_2026-10-19.md`. | PROGRAMME_STATE.md; reports folder listing |
| 8 | RULES.md still says "22 build-now procedures", "Open decision D1" about the franchise POS source, and "everything under `C:\claude\REPORTING`". The programme is now 243 procedures, franchise is decided (huddle item 4), and the path is `C:\claude\Project\REPORTING`. | RULES.md (10 Oct snapshot) |
| 9 | Old path `C:\claude\REPORTING` in 13 places across 5 agent files, and in `settings.json` permission entries. | `.claude\agents\*.md`; settings.json |
| 10 | Catalog metadata: REMAINING file says Claude has not received Priscilla's metadata; the 19 Oct report says Priscilla sent it to Lori. Probably the file has not reached Claude yet. | REMAINING_PROCEDURES_2026-10-19.csv; Morning_Report_2026-10-19.md |
| 11 | DumpKey_Extract_Finance and B2C_GiftCard_Weekly were run on D365 data by people on 19 Oct but are not in the ledger or VERIFICATION_MATRIX. The 19 Oct report listed both as quarantined and verified by Priscilla or Ryan. Verified count stays 0. DumpKey shows Days_Since_Trans = -19, which needs an AX behaviour check before any PASS. | Addendum items 17, 18 |
| 12 | Open rows for Ecomm_NonBook_Catalog in DECISIONS_NEEDED (linked server) conflict with the register READY FOR APPROVAL status; REMAINING file says the pack still reads the production Commerce server. | DECISIONS_NEEDED.csv; REMAINING_PROCEDURES_2026-10-19.csv |
| 13 | owner.md lists the programme people but names Ryan Blom, Piotr Piszczyk, Priscilla, Mindaugas, Valentin without surnames for the last three; no contradiction, but the report uses first names as the files do. | owner.md |

Files read: company\owner.md, voice.md; agents\reporting\job.md, playbooks\morning-report.md; PROGRAMME_STATE.md, RULES.md, AUTONOMY_POLICY.md, SUMMARY.json, DECISIONS_NEEDED.csv, REMAINING_PROCEDURES_2026-10-19.csv, STATUS_BY_PROCEDURE.csv, PROGRESS.md, both 19 Oct decision files, the 19 Oct morning report, and `.claude\settings.json` (read only). Not read: the two 19 Oct request files, VERIFY_RESULT files, the ledger.
