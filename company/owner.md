# How the Owner Works

## Who
Lori Ryan, Digital Technical Manager at Easons, Dublin. Owns Easons.com and DubrayBooks.ie across ecommerce operations, GTM and analytics implementation, vendor management and programme governance. The in-house development team is Samir and Lori (on 2026-10-20 Lori said "its just samir and me for the inhouse"; the earlier note said two developers, so treat Samir as the one in-house developer unless Lori says otherwise). Works with an external agency, FTT. Main FTT contact: Mark.

## Working pattern
- Hours: 08:30 to 17:00. Available outside office hours for P1 only. Nothing else goes to Lori out of hours.
- Morning briefing order: risks first, then what changed overnight, then decisions needed.

## Current priorities (as of 2026-10-20)
- Black Friday readiness, with code freeze on 6 Nov (see Key dates).
- DubrayBooks.ie basket threshold promotions (Lori owns). Requirements doc written, being turned into Azure DevOps tickets.
- CCPC price history (Was/Now and 30-day lowest price compliance): Lori rewrote the price history at the weekend (17-18 Oct 2026). Ciarán owns it. Needed for Black Friday.
- D365 migration: go-live after Christmas. Current focus is delivering the stored procedures and reports for the business ASAP (BYOD 243 programme).
- GTM and sGTM sign-off.
- Easons.com on Optimizely DXP: LIVE since 2026-09-01 23:00 Irish (per master vault). Early-life support, post go-live defects and change requests with FTT. Early Life Support end date was proposed to FTT, outcome not confirmed here.
- DubrayBooks.ie: live on Medusa Cloud (migration done). Post go-live support and Black Friday readiness.

## People
- Ciarán: sponsor of the Black Friday basket threshold work; owns the CCPC price history work (always spelled Ciarán)
- Samir: in-house developer; builds the basket threshold promotions on Medusa Cloud
- Mike Courtney: owns reporting
- Mark: main contact at FTT
- D365 / BYOD stored procedure programme: Ryan Blom, Piotr Piszczyk, Priscilla, Mindaugas, Valentin (see the `reporting` job)

## Key dates (2026)
- **Code freeze: 6 November.** Lori said "6nov". Confirm it applies to both Easons.com and DubrayBooks.ie. Anything Black Friday that needs code must be built, tested and signed off before then. Always show days remaining.
- **Cyber weekend: last weekend of November.**
- **Toy Show: first weekend of December.** Treat as a trading peak.
- **D365 go-live: after Christmas.** Exact date unknown.

## Known gaps (do not guess; ask Lori)
- Basket threshold ticket: Lori said "ticket start at 1700". Unclear whether that means ticket IDs start at 1700 or a 17:00 start time. Confirm.
- Whether the CCPC price history rewrite is deployed and verified, and where.
- Exact Black Friday date she is planning around (cyber weekend is the last weekend of November).
- Exact D365 go-live date.
- Who Lori reports to.
- Anything the team must never touch beyond the rules below.

## Where things live
- Code: `C:\DEV` (Easons.com source, B2B, Dubray, monitoring jobs, JobWatch, corporate sites, and others).
- Knowledge vaults (Obsidian): `C:\claude\Vaults\` holds `master` (a ROUTER, not a knowledge base), `EasonWiki` (Easons.com implementation history), `HAL-Vault` (monitoring and operational health), `easons-vendors`. Project vaults also sit in project folders: `C:\claude\Project\b2b`, `C:\claude\Project\erosNg`.
- Active project folders: `C:\claude\Project\REPORTING` (BYOD 243), `C:\claude\Project\gtm` (GTM/sGTM). Other folders in `C:\claude\Project`: d365, dubray-orders, dubrayblog, easoncorp, easons-cloudflare-pages, mailer, orders, priceHistory.
- FTT Programme Highlight Reports (HLR), weekly PDFs: `C:\Users\lryan\EASON LIMITED\IT-Ecommerce - HLR Reports` (25 files, `NN_EAS_HLR_DD_MM_YYYY.pdf`). Newest in the folder is Week 20, 24 Jul 2026, so nothing from August to October is saved there (STALE, or FTT stopped issuing them; ask Lori). Prepared by FTT (Kashif Hasan, Mark Everard). Covers P-EAS-02 .NET Upgrade + DXP Migration, P-EAS-03 UX Upgrade, P-EAS-04 Support & ALM (to 31 Jan 2027). Read PDFs with `python -I` and `pypdf` (poppler is not installed).
- Vault rule: every project has a vault and it is kept current. See `company/rules.md` rule 6 and the `vault-keeper` employee. Routing: `C:\claude\Vaults\master\Claude Routing Rules.md`. Code beats notes when they disagree.

## How updates should be written
- Short and direct. Risks and blockers first, never a caveat at the end.
- If something is uncertain, say so.
- Executive summary: goals, deliverables, risks, dependencies, decisions required.
- Detail: issue, impact, dependency, action, owner, risk.

## Always reviewed by Lori before it goes out
- **Vendor and FTT communications.** Ownership and next actions must be explicit. Verbal agreement does not close an item without written confirmation.
- **GTM publishes.** State which container first (uat.easons.com or www.easons.com production). Test across all seven layers.
- **Anything that changes or deletes data.** Warn Lori first.
- **Orders:**
  - Test orders are fine on Easons.com in UAT and INT, and on DubrayBooks.ie in QA and UAT.
  - No real orders and no personal or payment data on either production site.
  - Production purchases are Lori's to do; agents read the evidence.
  - Name the environment before placing anything.
