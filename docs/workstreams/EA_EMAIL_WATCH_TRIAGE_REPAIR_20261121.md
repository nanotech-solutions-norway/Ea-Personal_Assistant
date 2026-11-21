# Ea Email Watch — Fail-Closed Triage Repair (21.11.2026)

**Status:** CODE-ONLY / SYNTHETIC TESTS / PENDING_REVIEW / NOT_DEPLOYED / NOT_CANONICAL  
**Workstream:** Ea Business Email Watch; Level 2A INTERNAL UNSENT only; Level 2B/C HOLD.  
**Governing sources:** current operator request; Ea 07B blob `85691ccfe575ec1c4231bad8f5c5b023fffaa721`; 03D `596c5f90d64114a73caaae386d9007be189de43b`; 03F `c40ad6581b1ffb8c25861eb36fc8d7160b0d0725`; 03I `2c771eeea1c778668fd85d8bd15b459eb3795b00`.

## Verified problem classes

1. The enabled native hourly ChatGPT task may finish without invoking live Gmail. A completed run is not an acceptance result. Historical business cases remain unreviewed if only metadata inventories are retrieved.
2. Existing mail APIs can return sender under `from` or `from_`; absent sender data must be UNKNOWN rather than raising `TypeError` or proving a particular alias.
3. The current native Gmail `create_draft` action has no explicit `from_address`/send-as selector. A previously listed draft with a valid From does **not** prove the new-draft sender identity. Block new Ruben-persona drafting when selected send-as cannot be proven.
4. Existing Calendar and CRM narratives may mention historical drafts that have been sent, modified, or removed. Use the current Gmail draft list, exact provider message ID, full current thread and SENT as the governing business evidence.
5. The existing P1 and P2 code modules are synthetic, read-only and NOT_DEPLOYED; a green CI suite is not evidence that the hourly ChatGPT task has been repaired in production.

## Change: `workstreams/p2/email_watch_triage.py`

- Null-safe sender field and inventory health state handling.
- Deterministic five-case selection with two oldest overdue cases preserved unless displaced by immediate-severity cases.
- Mandatory per-case gates: recipient-specific 03D suppression, Espen chat-only, complete thread, current SENT, existing draft, factual dependencies, source account, verified send-as and actual reply anchor.
- No `DRAFT_VERIFIED` until independent current Gmail message + draft inventory match exact draft ID, message ID, thread ID, From, To, CC, subject, clean response body, DRAFT label, attachment manifest and uniqueness.
- Private solo Calendar follow-up reminder verification, with no event writes.
- No external clients, token handling, customer information, persistence, webhook, scheduler, provider writes, approval or production deployment.

## Acceptance tests

Run `python -m unittest discover -s workstreams/p2/tests -p 'test_*.py' -v` under current repository PR CI. The 19 added synthetic tests explicitly reject provider-only health as completed case preflight and sender-alias inference, and preserve 03D and 03F gates.

**Still required for actual operational recovery:** instrument one native task run to prove live provider calls, process an actual eligible case to a correct in-thread unsent draft with post-write QA under a verifiable sender, reconcile stale CRM/Calendar in their owning workflows under exact write authority, independently read back the resulting provider state, and ensure a canonical redacted ledger. Do not claim acceptance merely because this PR merges.

**Mutation boundary:** Repository code-only repair. No Gmail send/draft write, Calendar create/update, Drive mirror, CRM mutation, schedule alteration, new task, commercial release, 2B/2C activation, or canonical-promotion authority.
