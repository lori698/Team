# Shared Memory — Company Rules and Corrections

One notebook for the whole team. Add a line whenever the owner corrects something that should apply to everyone. Newest at the bottom. Keep each rule to one or two lines with the reason.

1. Draft, don't send. External communication needs an approved file in `approvals/approved/`. (Why: outbound messages can't be taken back.)
2. State what is confirmed vs assumed when reporting. (Why: the owner acts on these reports.)
3. Name the environment before any GTM publish or test order. No real orders or personal/payment data on production Easons.com or DubrayBooks.ie. (Why: Lori's standing rule; production purchases are hers.)
4. Warn Lori before anything that changes or deletes data.
5. Risks and blockers go first in every update.
6. Every project has a vault and it is kept current. When work on a project produces durable knowledge (a decision, a changed status, a root cause, a runbook step), hand it to `vault-keeper` with the source and date. Do not copy project detail into the master vault; it is a router. Never write secrets into any vault. Code and live evidence beat notes. (Why: Lori wants vaults maintained; most are weeks stale.)
7. Code freeze is 6 November 2026 (confirm it covers Easons.com and DubrayBooks.ie). Lori works 08:30 to 17:00 and is contacted out of hours for P1 only. Anything Black Friday related that needs code must be flagged now with days remaining. D365 is after Christmas, so the stored procedures and reports are the priority until then.
8. DXP (Easons.com) and DubrayBooks.ie on Medusa Cloud are both live. Treat their work as post go-live support, not migration. Do not describe either as upcoming.
