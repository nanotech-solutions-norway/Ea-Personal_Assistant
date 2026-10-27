# Ea vNext — M5 Controlled Level 2A Canary Plan (Non-executing)

**Date:** 27.10.2026, Europe/Oslo  
**Work ID:** `EA-VNEXT-20261027-02`  
**Status:** `CANARY_DESIGNED / EXECUTION_NOT_AUTHORIZED / LEVEL_2B_2C_HOLD`  
**Scope:** Internal-only, no customer emails sent, no calendar external attendees, no user files shared or deleted, no Azure resources or managed sync provisioned.

## Purpose

Measure whether proposed vNext transaction/reconciliation rules produce provider-verified internal outcomes without losing older actionable cases, duplicating drafts, changing sender identity, violating 03D suppression, adding inappropriate reminders or making unsupported product/commercial claims.

## Candidate cohorts

| Stage | Number | Source/selection | Permitted action | Exit test |
| --- | --- | --- | --- | --- |
| C0 — synthetic model | 19 existing fixtures plus new negative cases for stale read and reminder policy | Synthetic-only fixture objects with no PII | Local deterministic tests | Expected allow/deny and no provider operations |
| C1 — shadow read-only | Up to five approved existing business case IDs, de-identified in public logs | Two authorized Gmail accounts, Calendar and approved CRM, with exact source timestamps | Read/summarize/reconcile only; no writes | Every observed case disposition source-linked; 0 unsupported closure |
| C2 — isolated Level 2A internal canary | Maximum two separately named, specifically operator-authorized draft cases plus one separately authorized private internal follow-up | Provider account, sender, recipient, thread and 03D suppressions verified in advance; use owner-approved private evidence | Create or update **unsent** in-thread draft, or duplicate-safe private solo follow-up under current 03A | Every mutation independently reread; 0 duplicates, wrong threads, wrong recipients or violations |
| C3 — guarded shadow endurance | 100 consecutive actionable cases and >=14 normal-operation days (whichever longer) under canonical 08 QA criteria | Bounded live but read-only comparison; separately approved writes only | Verify per-case coverage, callbacks and provider results | 100% mandatory readback/audit, zero severe failures |

## Strict per-case preflight

1. Retrieve applicable approved source revision and current task/sink permissions; record work ID and stable account/case/action identity.
2. Read the latest full relevant Gmail thread, current SENT and drafts, Calendar event, CRM state and applicable product truth. Never reveal cross-customer material in public artifacts.
3. Check actual account identity and exact authorized send-as persona. Gmail current `create_draft`/`update_draft` do not expose an explicit `From` parameter. If exact required alias cannot be independently verified, return `SENDER_ALIAS_UNVERIFIED` and do not create a misleading draft.
4. Apply known **recipient-level** operator manual-deletion suppression per 03D. An absent draft alone is not evidence of deletion.
5. Espen Olsen authored messages: chat-only prose for manual Outlook; no Gmail drafts.
6. For Ruben drafts: native reply anchor, To/CC, subject, no Ea-authored signature, no quoted old history; exact current source and attachment proof.
7. Check an existing draft before create. If update or cleanup fails after ambiguous success, reread rather than blind retry.
8. Internal follow-up Calendar event: private, solo, transparent, no Meet, no popup/email reminders, 15 minutes, Europe/Oslo; excludes invoice/payment/customs cases.
9. Independent provider readback verifies action, draft state, exact thread, recipients/CC, body and attachment state; log status not just HTTP success.
10. Keep external communication, file permissions, procurement, shipping and commercial/legal commitments outside Level 2A authority.

## Minimal canary state envelope

`case_ref`, `source_revision`, `action_type`, `authorized_sender_class`, `recipient_suppression_status`, `idempotency_key`, `preflight_result`, `write_attempt`, `provider_readback_result`, `disposition`, `next_due_at`, `error_class`, `evidence_pointer`.

No confidential message bodies, actual customer addresses, raw identifiers, bank/accounting values or secrets in this public repository.

## Stop conditions

Stop on wrong sender/persona, wrong thread/recipient/CC, unapproved pricing/regulatory commitments, known deletion-suppression violation, duplicate draft, external attendee/action, provider permission denial, impossible readback, stale source or source conflict. Quarantine only affected case when safe; other cases remain open and accountable. A severe safety failure resets validation window.

## Acceptance and release

C0 and C1 can be completed within explicit bounded read-only preparation authority. **C2 actual writes** require a separate exact-scope canary authorization identifying concrete cases, provider account and intended mutation. C3 no external send or cutover rights. M8 production cutover needs separate approval. Level 2B/2C and managed live backend deployment remain HOLD.

## Operator decision later

Authorize at most two eligible in-thread unsent Gmail draft cases and one duplicate-safe internal follow-up for C2 after presenting private preflight and verifying there is no 03D suppression or sender-alias blocker; alternatively continue read-only C1 shadow if tools remain insufficient. No case names/addresses are assigned or presumed authorized by this design document.
