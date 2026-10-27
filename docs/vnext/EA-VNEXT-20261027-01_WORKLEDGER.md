# EA vNext — M1 controlled rebuild work ledger — 16:06, 27.10.2026 (Europe/Oslo)

**Work ID:** `EA-VNEXT-20261027-01`  
**Status:** `PREPARATION_ONLY / FEATURE_BRANCH / PENDING_REVIEW`  
**Canonical owner:** Ea Personal Assistant repository, one workstream-specific ledger  
**Parent source commit:** `370891a1e2058b4c15e546382b787bdfb1438721`  
**Global event protocol:** `ai-memory-ops/protocols/operational_event_logging_rollback_CURRENT.md`, blob `0171fa4518ddfffef4c05254893da2bfe04ee9ac`  
**Authority:** Operator approved Option B controlled rebuild (27.10.2026), then instructed proceeding with M1 baseline preservation, source authority consolidation and isolated synthetic rule tests. Approval does **not** permit production migration, existing-task modification, protected-main merge, new cloud deployment, confidential-data copies, Level 2B/C activation or external messaging.
**Scope/target:** new non-sensitive `docs/vnext/` files on `feature/ea-vnext-m1-20261027` only; current production integrations unchanged.
**Rollback reference:** close the unmerged draft PR and delete only the new feature branch after an explicit approved recovery decision; never claim production rollback because this branch does not change production.

## Append-only events

| Event | Timestamp / stage | Tool/actor | Before → after | Idempotency/attempt | Evidence/readback | Open action |
| --- | --- | --- | --- | --- | --- | --- |
| E001 | 27.10.2026 / PREPARED | Operator and Ea / read-only GitHub, Drive, Automations | Existing current baseline → fixed-source M1 proposal identified | EA-VNEXT-20261027-01/M1/PREFLIGHT, attempt 1 | GitHub source inventory and protected `main` commit `370891a`; Drive vault index retrieved; five Ea task states read; no duplicate vNext branch/PR found | Create isolated branch |
| E002 | 27.10.2026 / AUTHORIZED | Operator instruction | Preparation requested → branch-only non-sensitive documentation and synthetic tests allowed | EA-VNEXT-20261027-01/A1, attempt 1 | Current explicit instruction `Proceed as recommended` following approved rebuild and limited M1 gate; no release rights added | Preserve production state |
| E003 | 27.10.2026 / ATTEMPTED | GitHub create_branch | No matching vNext branch → `feature/ea-vnext-m1-20261027` returned | EA-VNEXT-20261027-01/BRANCH, attempt 1 | Connector returned branch name; exact commit start `370891a...`; branch-head readback pending | Write this work ledger, then verify |
| E004 | 27.10.2026 / PREPARED | GitHub create_file | New work-ID ledger absent → expected new file on branch | EA-VNEXT-20261027-01/LEDGER, attempt 1 | Prewrite check: `docs/vnext/EA-VNEXT-20261027-01_WORKLEDGER.md` absent on `main`; provider readback pending | Independently fetch created file |

## Safety and source-boundary notes

- Public GitHub: do not commit private correspondence, actual sender email addresses, customer payloads, financial/accounting records, calendars, secrets, OAuth tokens or confidential files.
- Historical/derived Drive mirrors are **not** independent authority. Do not promote PENDING_REVIEW changes.
- Canonical 03A/03B internal Calendar follow-ups have **no popup or email reminders**, reaffirmed 20 October and merged in PR #93. The newer 27 October live Email Watch addendum requesting a 30-minute popup is a **specific unresolved conflict**, not an approved replacement for that canonical rule.
- Level 1 approved; Level 2A controlled internal only; Level 2B/C HOLD. Azure staging approval issue #84 remains NO_DEPLOYMENT and budget/approval-gated.
- External writes must be independently read back. An ambiguous write must not be retried blindly.

## Remaining checkpoints
- [ ] Fetch ledger from feature branch and verify content.
- [ ] Write/readback M1 baseline and authority/conflict inventory.
- [ ] Write/readback M2 migration and acceptance specification.
- [ ] Run offline synthetic rule tests; capture count and failures without claiming backend acceptance.
- [ ] Open a draft proposal PR, read back PR and changed files; do not merge.
- [ ] Drive mirroring: defer pending an exact authorized destination and provenance plan; **MIRROR_PENDING**.
