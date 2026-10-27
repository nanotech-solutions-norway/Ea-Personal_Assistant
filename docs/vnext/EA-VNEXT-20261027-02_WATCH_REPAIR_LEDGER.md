# EA vNext — Controlled Hourly Watch Classification Repair Ledger
**Started:** 27.10.2026 after 17:59 Europe/Oslo  
**Work ID:** `EA-VNEXT-20261027-02`  
**Status:** `PREPARED / AUTHORIZED_BY_OPERATOR / WRITE_NOT_YET_ATTEMPTED`  
**Parent decision:** `EA-VNEXT-20261027-01`; PR #101 MERGED as `2946ab1cff106be20820e3c3472f7a9a132f0754` at 16:59:08 UTC.  
**Scope:** Correct ONE existing hourly native Email Watch reminder-classification paragraph only; preserve the rest of its exact prompt and its task ID, hourly `condition_watch`, enabled state, timezone, last run, and owner. Prepare Level 2A read-only/synthetic canary plan. The operator's “Merged. Proceed as recommended” approves the previously proposed targeted correction and diagnostic continuation; no additional send/Calendar/CRM/Drive/production cloud authorization is inferred.
**Source authority:** `active-source/03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md` blob `66ca58343758e55dcddd679d498f2731e38a2fe3`; `03B` and `07B`, plus merged `docs/vnext/M4_RUNTIME_POLICY_REPAIR_PROPOSAL_20261027.md` blob `0600a2d045c229399cb2a97223c60e6d9958daeb`.

## Preparation and change envelope

- Native task: existing `Ea Business Email Watch` (private provider ID is verified in provider, not stored in this public repository).
- Before: enabled, hourly condition_watch; prompt contains exactly one contradictory line D declaring reminder-free internal private follow-ups `REMINDER_DISABLED` as a defect and proposing popup 30 minutes before start.
- After intent: replace only paragraph D with classification `FOLLOWUP_REMINDERS_OFF_BY_POLICY`; no new popup/email reminders for private internal follow-ups, no change to meeting reminder standards; continue independent due-case reconciliation and notify only when supported.
- Effective 03A/03B authority is already approved; this is a runtime classification repair, not an unapproved rule promotion.
- Required checks: exact one old-string occurrence; no changes to unrelated characters; after provider update, independent task peek must match expected prompt exactly, same ID/title/enabled/mode/schedule, no unauthorized external side effect.
- Recovery if provider update or readback ambiguous: STOP, re-peek and classify `AMBIGUOUS_WRITE`; never blindly retry. Restore the previously captured original prompt only by an independently approved targeted compensation.
- Current Gmail profile/draft read-only checks: both account profiles and draft listings reachable; `From` metadata absent on returned draft summaries; `create_draft`/`update_draft` expose no explicit send-as selector. Do not claim arbitrary sender alias verified.
- Operator has not authorized any customer draft or Calendar mutation in this work ID. No M5 live canary in this work ID; planning only.

## Events
| ID | State | Event | Result |
| --- | --- | --- | --- |
| E001 | PREPARED | PR #101 merge verified; 03A/07B/03F/source/M4 proposal readback; existing live watch config and last run read | PASS; no prior rule promotion |
| E002 | PREPARED | Source-approved internal reminders checked; Gmail both accounts profile/draft-read reachable; sender alias selector unavailable in current tools | PASS; alias `UNVERIFIED` |
| E003 | PREPARED | Dedicated feature branch from merged PR #101 for redacted source/readback evidence | `feature/ea-vnext-watch-policy-20261027`; main unchanged |
| E004 | PREPARED | Single native watch D-paragraph replacement | Not executed; readback pending |

**Provider external effects:** no emails, meeting invitations, customer Calendar writes, CRM, Drive or Azure mutations in this preparation stage. `LEVEL_2B_2C_HOLD`, `PRODUCTION_CUTOVER_HOLD`.

## Verified repair continuation — 27.10.2026

| ID | State | Before → after | Provider evidence / restriction |
| --- | --- | --- | --- |
| E004 | VERIFIED | Live prompt previously contained exactly one old reminder paragraph → only that paragraph replaced | Native `Automations.update` success then separate `peek`: full 10,038-character prompt exact match; unchanged task ID/title/enabled=true/hourly `condition_watch` recurrence; previous prompt length 9,601; no Calendar event writes |
| E005 | VERIFIED | No scoped post-change report → `EA-VNEXT-20261027-02_RUNTIME_READBACK.md` added on feature branch | Commit `96379e9da03a16b09ed78a8df8571abca5e08412`; blob `ae5b33c87e95b9ebcc3c6de7eaf141607608e33f`; independent text readback PASS |
| E006 | VERIFIED | No M5 plan → bounded synthetic/shadow/internal-only canary proposal added | Commit `3535f755a1d197538c52b8c0857f5da283b473be`; blob `3f859ebdf788d8f73311fb890750b70bbec95869`; independent text readback PASS; C2/C3 writes not executed |
| E007 | VERIFIED | Canonical 07B lacked exact new runtime classification provenance → feature-branch addendum proposed | Commit `79fa981e54955e4e1ac9302c2e9dbc0679470d8f`; blob `63c4aa2e46727ddcb13b8deada8a9eb2a13c0661`; source old prefix preserved; exact readback PASS. **Not yet merged, not new canonical authority.** |

**Provider result:** confirmed task prompt replacement only, no uncontrolled retries; no customer data, Gmail draft, send, Calendar event, CRM or Drive mutation. Sender-alias control unsupported in exposed draft action schema; both Gmail profiles and draft metadata reachability PASS but `from` absent in returned draft summaries. **Operational hourly outcome after repair: NOT_YET_ACCEPTED**. Production cutover and Level 2B/C HOLD.
