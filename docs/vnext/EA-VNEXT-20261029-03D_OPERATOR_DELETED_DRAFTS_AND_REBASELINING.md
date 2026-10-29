# Ea vNext — Operator-Deleted Gmail Drafts: Suppression, Readback and Release Rebaselining

**Work ID:** `EA-VNEXT-20261029-03D-01`  
**Date:** 29 October 2026, Europe/Oslo  
**Status:** `OPERATOR_DELETION_VERIFIED / 03D_SUPPRESSION_ACTIVE / NO_REPLACEMENT_DRAFT_AUTHORIZED / CASES_OPEN / CUTOVER_HOLD`  
**Authority:** Current operator instruction states the two previously repaired yet detached drafts were intentionally deleted. Approved/canonical 03D takes precedence over older generic advice to rethread or replace drafts. This report is redacted for a public GitHub repository.

## Verified live and operator facts

- The operator explicitly confirms deletion of exactly the two previously identified unsent drafts, anonymized here as **C2-A** and **C2-B**.
- Provider readback of the business Gmail account finds **zero active drafts** and no pagination. The former two draft-only threads both return `NOT_FOUND`. This independently confirms absence; **operator confirmation**, not absence alone, establishes the intentional deletion/suppression classification.
- Both original Gmail customer/technical threads remain intact; the bounded full reads returned **63/63** and **10/10** messages with no `DRAFT` children, respectively.
- Business Gmail was only **read**, never written to in this work item. No replacement drafts, sends, forwards, Calendar events, or changes to sender/recipient identity.
- The exact private native CRM register already had both draft-gate rows and follow-up outcomes updated to `OPERATOR_DELETED_SUPPRESS_RECREATE` and two operator-deletion audit rows. Preimage-checking discovered those changes were already present; the planned duplicate CRM transaction was aborted and **zero new CRM writes** were made in this work item.
- The existing native hourly `Ea Business Email Watch` task's approved prompt already enforced general 03D, but lacked a case-specific signal. A narrowly scoped prompt amendment now identifies both known deleted draft cases and their recipients **inside the private task only**. Independent native task readback confirms that the clause is persisted, the task is enabled and its previous hourly schedule is unchanged.

## Disposition change

| Control | Before | Current verified disposition |
| --- | --- | --- |
| C2-A detached draft | Corrected in place but wrong original thread; failed QA | **Intentionally deleted**, `OPERATOR_DELETED_SUPPRESS_RECREATE`; no replacement authorized |
| C2-B detached draft | Corrected in place but wrong original thread; failed QA | **Intentionally deleted**, `OPERATOR_DELETED_SUPPRESS_RECREATE`; no replacement authorized |
| Historical original correspondence | Preserved source threads | Preserved; no statement that a new response was sent |
| Underlying commercial/technical follow-ups | Open / gated | **Still open**; technical, product, commercial and factual review may continue |
| Current hourly email watch | General suppression only | Two case-specific recipient-suppression entries persisted and provider-read back |

**Important:** The old finalization recommendation to rethread **these exact two drafts** is now superseded by an explicit operator decision. Do **not** create replacement drafts or count these deliberate deletions as unresolved draft-repair failures. A future explicit operator request to prepare a fresh reply for either case will authorize only the specifically requested draft, subject to sender/recipient, threading, technical/content and no-send safeguards.

## Release tracker implications

- The older `EA-VNEXT-20261029_FINALIZATION_STATUS_AND_GATES.md` is a historical snapshot of the pre-deletion state and must not be silently reinterpreted. Its `0/2 correctly threaded` statistic is **historical, not a present count of current defective saved drafts**.
- **Suppression cleanup (case-specific): 2/2 confirmed.** This is an operational cleanup, **not** C2 native in-thread-drafting acceptance.
- The current acceptance gate F6 (`M5 C2 native correctly threaded, unsent drafts`) is **NOT YET MET**, and the two deleted cases are no longer eligible canary write objects. A future **distinct** approved canary, or an explicit source-authorized alteration of acceptance criteria, would be needed before marking F6 PASS. Do not silently swap the old gate's denominator or count deleted drafts as successful threaded drafts.
- Thus the earlier **5/9 diagnostic readiness gates** remains the last defined checklist observation. It is **not** a production percent.
- The canonical 08 QA release gate (100 consecutive actionable cases, at least 14 normal-operation days, zero wrong-recipient/thread/duplicate/03D violations, verified audit and readback) is **not certified**.
- The latest sampled hourly watch still reports outstanding sender-alias and accounting blocks and overdue cohort coverage; task run completion is not proof of delivery.
- Level 2B/2C and production cutover remain `HOLD`.

## Next safe work, in order

1. **Monitor one post-amendment hourly watch cycle** to independently confirm these two cases remain suppressed, no duplicate customer drafts were created, and their absences are not mislabeled as the primary draft QA defects. If scheduled task feedback cannot prove notification delivery, retain `COVERAGE_NOT_VERIFIED`.
2. Continue the oldest-first controlled lead backlog; distinguish source-supported replies already sent, waiting-external, waiting-internal and genuine missing responses. Do not let a suppressed draft trigger outreach. Reconcile stale CRM only with exact preimage checks and append-only audit.
3. Prepare any separate technically feasible and specifically approved new C2 canary plan; do **not** reuse these deleted draft IDs or original reply objects.
4. Build the 100-consecutive-case/14-day evidence ledger from distinct verified cases and run records, recording retries, source identity, audit/readback and failures. Never count repeated cases as independent completions.
5. Keep production deployment, sensitive external communications, external Calendar invitations and managed Level 2B/C on HOLD pending separate explicit operator release approval.

**Privacy:** No confidential party names, email addresses, source message bodies, draft IDs, private CRM URLs, pricing or sensitive correspondence appear here. Provider evidence remains in Gmail, the private CRM audit and the private automation prompt.
