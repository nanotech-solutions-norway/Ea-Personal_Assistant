# Ea vNext — Controlled rebuild preparation index — 16:06, 27.10.2026 (Europe/Oslo)

**Work ID:** `EA-VNEXT-20261027-01`  
**Status:** `PENDING_REVIEW / NONEXECUTING_FEATURE_BRANCH`  
**Basis:** pinned canonical Ea main commit `370891a1e2058b4c15e546382b787bdfb1438721`.  
**Authoritative production rules:** the existing `active-source/` project documents and approved `ai-memory-ops` global rules, **not** the new files here.

## Review order

1. `EA-VNEXT-20261027-01_WORKLEDGER.md` — one append-only redacted workstream event ledger.
2. `M1_BASELINE_20261027.md` — versioned source and no-modification baseline.
3. `M1_AUTHORITY_AND_CONFLICT_REGISTER_20261027.md` — current effective rule map and scoped PENDING_REVIEW issues.
4. `M2_ARCHITECTURE_ACCEPTANCE_PLAN_20261027.md` — proposed target separation, migration M1–M8, release gates.
5. `synthetic_policy_guard.py` — **synthetic only** illustrative decision evaluator; not imported by any production EA runtime.
6. `test_synthetic_policy_guard.py` — offline negative/positive fixture tests.
7. `M3_SYNTHETIC_TEST_RESULTS_20261027.md` — exact test execution and limitations.

## Reproduce test

From the repository root with Python 3:

```bash
python3 -m unittest discover -s docs/vnext -p "test_synthetic_policy_guard.py" -v
```

Expected baseline: 19 tests PASS (tested offline 27 October 2026). This is **not** Gmail/Calendar/CRM provider acceptance, release gate M7, or cloud deployment evidence.

## Non-negotiable controls

- Feature branch and draft PR only. No automatic merge.
- No production automation/task edits, customer data replication, external communication, Azure provisioning, provider permission modifications, or production cutover.
- Do not modify current approved `03D`, `03F`, `03A` or `07B` through this PR.
- Hold the internal follow-up reminders conflict as CR-01; do not silently switch from no-reminders to 30-minute notifications.
- No sensitive personal/customer data or financial/secret material in this public repo.
- Level 2B/C HOLD. Maintain existing Level 2A scope and independent provider readback requirements.

## After review

A separate scoped source-cleanup PR may be proposed after the operator adjudicates pending conflicts. M4 connector probes and M5 Level 2A canaries require their own exact grants and provider evidence; M8 cutover requires explicit release approval.
