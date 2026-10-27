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

## Continuation events (append-only; 27.10.2026)

| Event | Phase | Actor / tool | Before → after | Idempotency / attempt | Evidence / readback | Remaining |
| --- | --- | --- | --- | --- | --- | --- |
| E005 | VERIFIED | GitHub fetch_file | Proposed branch ledger created → text read back, no conflicting existing work-ID file | EA-VNEXT-20261027-01/LEDGER, attempt 1 | Exact branch path SHA `6f5df44b2c44a490f5e3075123ef0141b5b8509a`; PASS | Baseline capture |
| E006 | VERIFIED | GitHub create_file + fetch_file | No `M1_BASELINE_20261027.md` → source/SHA/task snapshot file recorded | EA-VNEXT-20261027-01/BASELINE, attempt 1 | Commit `3a7ab017d7ace2e030f9b0ad475a1823897a59dd`; exact content readback PASS | No external data backup inferred |
| E007 | VERIFIED | GitHub create_file + fetch_file | No scoped authority/conflict inventory → CR-01..CR-07 proposed without rule promotion | EA-VNEXT-20261027-01/AUTHORITY, attempt 1 | Commit `4034ade9f8d653df5f7556700aa9f88786b7340f`; exact content readback PASS | Operator review required |
| E008 | VERIFIED | GitHub create_file + fetch_file | No target architecture/acceptance pack → M1–M8 gates documented | EA-VNEXT-20261027-01/PLAN, attempt 1 | Commit `22c50bb66f05230fcde3e6b122e23f17bb638e85`; exact content readback PASS | M4+ separately gated |
| E009 | VERIFIED | GitHub create_file + fetch_file | No synthetic policy artifacts → Python fixture and 19 tests added | EA-VNEXT-20261027-01/SYNTHETICS, attempts 1 per file | Source commit `7af69ce81b71bc762a025b7adaf8031e6ee1c260`; tests commit `507b2720d149ed8732a64e01332270d3ea26f580`; exact content readback PASS | Not production rule engine |
| E010 | VERIFIED | Python local unittest | Synthetic fixture untested → 19/19 test functions PASS, return code 0 | EA-VNEXT-20261027-01/LOCALTEST, attempt 1 | Offline output `Ran 19 tests ... OK`; unrelated non-fatal startup warning noted in test report | Remote CI not yet verified |
| E011 | VERIFIED | GitHub create_file + fetch_file | No index and test-report file → two reviewable artifacts added | EA-VNEXT-20261027-01/REVIEWPACK, attempt 1 per file | Commits `0552a4df5f1ee395e0b91aa10ff922831d1274c0` and `e930be536a3bb4f6d6402e7bf61487ee66ce460c`; exact readback PASS | Draft PR preparation |
| E012 | PREPARED | GitHub PR creation (pending) | Feature branch verified → draft PR proposed, no merge or effect on production | EA-VNEXT-20261027-01/PR, attempt 1 planned | Exact PR URL/readback not yet available | Create one draft PR; verify and record |

**Scope remains:** feature branch only; no existing Ea task, customer provider record, product archive, Google Drive mirror or main branch changed. **Drive mirror:** `MIRROR_PENDING`. **Live backend:** `NOT_DEPLOYED`. **Canonical promotion:** `NONE`. **Release:** `HOLD`.

## Draft PR and independent provider readback — 27.10.2026

| Event | Phase | Actor / tool | Before → after | Idempotency / attempt | Evidence / readback | Remaining |
| --- | --- | --- | --- | --- | --- | --- |
| E013 | VERIFIED | GitHub create_pull_request + get_pr_info | Draft PR absent → PR #101 OPEN, DRAFT, `merged=false`, base `370891a`, branch head `158e781` | EA-VNEXT-20261027-01/PR, attempt 1 | `https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/101`; native PR readback PASS | PR review / CI after ledger amendment |
| E014 | VERIFIED | GitHub list_pr_changed_filenames | Expected eight newly added `docs/vnext/` files → exactly eight scoped additions; existing runtime files untouched | EA-VNEXT-20261027-01/PRFILES, attempt 1 | 8/8 matching proposal paths; additions only; PASS | Independent code/security review |
| E015 | VERIFIED | GitHub fetch_file main | Preflight canonical main `12_EA_MASTER_INDEX.md` blob SHA `b4578573cc8cc228d0e5dc2e3f5128d581892e4b` → unchanged after opening PR | EA-VNEXT-20261027-01/MAIN, attempt 1 | Verified same main blob SHA; PR base matches pinned `370891a`; PASS | No merge or main edit |
| E016 | READBACK | GitHub fetch_commit_workflow_runs | First observed PR security workflows → 2 SUCCESS and 2 IN_PROGRESS at verification | EA-VNEXT-20261027-01/CI, attempt 1 | Repository security baseline and Dependency review passed; Security baseline and CodeQL not complete. **CI_NOT_YET_ACCEPTED** | Do not infer full CI pass |

**External mutation summary:** feature branch, eight new non-sensitive proposal files, one draft PR, and this append-only ledger amendment. No existing user/customer provider mutation, no Drive mirror write, no Ea automation change, no protected-main merge, no cloud deployment. **LOGGING:** GitHub feature-branch ledger recorded and independently read back; Drive memory mirror `MIRROR_PENDING`; this is not evidence of durable production runtime logging. **Release:** `HOLD`.

## M4 connector diagnostics — 16:26, 27.10.2026 (Europe/Oslo)

**Scope/authority:** Operator continued the reviewed vNext controlled-rebuild plan. The next gate allows bounded, read-only capability inspection and non-sensitive proposal-branch documentation; no internal production draft, Calendar, CRM, Azure, scheduled-task, or main-branch changes. Current approved 03A/03B remain effective; the 27 October Email Watch popup suggestion is not a new approved policy. CR-01 remains `PENDING_REVIEW` only for any **future policy change**.

| Event | Phase | Actor/tool | Before → after | Idempotency/attempt | Evidence/readback | Open action |
| --- | --- | --- | --- | --- | --- | --- |
| E017 | VERIFIED | GitHub PR/info + Actions | PR #101 OPEN/DRAFT, earlier CI partly pending → 4/4 GitHub workflows SUCCESS on head `481fc7934ee7ac17789d7056488175028dffc00f` | `EA-VNEXT-20261027-01/M4/CHECKS`, 1 | Security baseline, Repository security baseline, Dependency review and CodeQL all PASS; does not prove live runtime or synthetic unittest executed by Actions | Record after proposal updates |
| E018 | VERIFIED | Gmail `list_drafts` (business and private) | Provider read-surface untested this session → both accounts reachable, returned 4/4 business draft summaries; 10 private with further page token | `EA-VNEXT-20261027-01/M4/GMAIL_READ`, 1 per account | All returned summaries DRAFT-labelled; `from` not populated in sampled summaries; no secret or customer payload copied to GitHub; no draft write | Exact sender/From alias cannot be explicitly selected by exposed draft actions |
| E019 | VERIFIED | Google Calendar `list_calendars`, bounded `search`, one `read_event` | Unknown current reachability → 8 calendars; primary writable; 20 matching existing follow-ups (no next page); sample event `reminders.use_default=false`, no override, private, transparent, no attendees | `EA-VNEXT-20261027-01/M4/CAL_READ`, 1 bounded read each | Search summaries did not include reliable reminder data; event-specific `read_event` did. Sample demonstrates **policy compliance**, not a defect | Do not alter event; preserve approved no-reminder policy |
| E020 | PREPARED | GitHub feature-branch write-ahead metadata | Current baseline and PR #101 unchanged → prepare `M4_CONNECTOR_DIAGNOSTICS_20261027.md` and scoped CR-01 clarification on same branch | `EA-VNEXT-20261027-01/M4/REPORT`, attempt 1 planned | Scope restriction: `docs/vnext/` only; source PR already draft/unmerged; no existing provider write | Write report, read back, update review status |

**Privacy:** Gmail account identities and message/recipient IDs, Calendar titles/event IDs, and full provider payloads are deliberately excluded from this public ledger. No sensitive material is saved. **Persistent production runtime logging:** NOT_VERIFIED. **External provider writes:** 0. **Drive mirror:** MIRROR_PENDING. **Release:** HOLD.
