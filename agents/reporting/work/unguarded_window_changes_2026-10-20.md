# MDW02 changes with no guard log line, 19 Oct 2026

Source: read-only sys.objects query run by Lori in the REPORTING project session, 2026-10-20 08:02:53 (guard logged ALLOW). Server clock vs local time not confirmed. Status: CONFIRMED for the list; the reason each changed is UNKNOWN.

Why these matter: the REPORTING hook was off 14:52 to 16:47 (incident note) and `.claude/settings.json` was emptied of hooks at 21:36 on 19 Oct (cause unknown). `scripts/guard/guard_log.txt` has no decision lines from 15:03:24 until after 17:00, and none after 21:20 (the last line seen at 21:20:43).

## Changes in or after a silent stretch (10 objects)
| Object | Type | Event | Time |
|---|---|---|---|
| Book_Sales_Stock_Top500_Franchise_BYOD | table | created | 19 Oct 15:25 |
| Book_8wk_Wh_Fra_Sales_BYOD | table | created | 19 Oct 15:55 |
| SP_Book_SalesStock_Top500_Franchise_BYOD | proc | altered | 19 Oct 16:54 |
| SP_Book_Sales_Nday_BYOD | proc | created | 19 Oct 21:37 |
| SP_PO_Lines_Books_BYOD | proc | created | 19 Oct 21:37 |
| SP_Book_Mins_Report_BYOD | proc | created | 19 Oct 22:05 |
| Book_Mins_Rpt_BYOD | table | created | 19 Oct 22:05 |
| SP_Book_SalesStock_BYOD | proc | altered | 19 Oct 22:09 |
| SP_Book_SalesStock_Top500_BYOD | proc | altered | 19 Oct 22:13 |
| Lookback_Days_Prior_BYOD | table | created | 19 Oct 23:47 |

## Not yet matched (log coverage unclear)
SP_Wholesale_Invoiced_Prev_Week_BYOD altered 21:04; SP_Book_Sales_50day_BYOD created 21:05; SP_Retail_OHQ_New_BYOD 12:04; SP_EDGAR_Update_Remain_PO_Qty2_BYOD 14:00; SP_NonBook_Pricing_BYOD 14:00; tables WHS_Stock_Book_Opening_BYOD and RetailOhq_Book_Linear_BYOD 12:07. Nothing changed after 23:47.
