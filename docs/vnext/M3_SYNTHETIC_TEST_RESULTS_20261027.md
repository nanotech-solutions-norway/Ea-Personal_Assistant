# Ea vNext — Offline synthetic rule test evidence — 16:06, 27.10.2026 (Europe/Oslo)

**Work ID:** `EA-VNEXT-20261027-01`  
**Class:** `SYNTHETIC_ONLY / NOT_PRODUCTION_VALIDATED`  
**Fixture under test:** `docs/vnext/synthetic_policy_guard.py`; tests `docs/vnext/test_synthetic_policy_guard.py`.
**Execution:** isolated Python 3 test runtime using `python3 -m unittest -v test_synthetic_policy_guard` from the fixture directory.
**Result:** `PASS`, 19 named tests, 0 errors, 0 failures, process return code 0.

## Fixture coverage

- Denial of unknown operations and external action set (including send, invitations, provider deletion, production cutover and Azure deployment).
- Espen chat-only/manual Outlook route.
- Approved recipient-level 03D suppression; a separate explicit new-draft request is evaluated only for its scoped simulated action.
- Wrong/unverified sender, thread anchor, stale source, existing draft, unwanted signature and unverified factual dependencies.
- Private follow-up without reminders; popup/email reminder request returned `PENDING_REVIEW` instead of silently overriding 03A/03B.
- No external attendee in private follow-up, no duplicate follow-up creation, and allowed read-only reconciliation.

## Execution limitation

The test runner emitted a non-fatal startup warning from an unrelated optional spreadsheet runtime warmup before the `unittest` results. The Python exit status was 0 and all 19 policy fixtures passed. No live network or provider service was used or verified. These tests exercise illustrative logic only and do not demonstrate the persistent queue, IAM, Gmail alias behavior, event delivery, post-write readback, database transaction integrity or Level 2A acceptance window.

## Release interpretation

**M3 synthetics = OFFLINE TEST PASS only.** Do not promote these fixtures as approved production authorization, do not mark Level 2B/C active and do not count these 19 tests toward the canonical 100 actionable case / 14-day provider evidence gate. Provider integration and live canaries remain HOLD pending separate authorizations.
