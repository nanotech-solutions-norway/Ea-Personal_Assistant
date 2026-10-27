# Ea vNext M4 — Connector and Rule-Conflict Diagnostics — 16:26, 27.10.2026 (Europe/Oslo)

**Work ID:** `EA-VNEXT-20261027-01`  
**Status:** `READ_ONLY_DIAGNOSTICS_VERIFIED / RULE_CHANGE_PENDING_REVIEW / PRODUCTION_HOLD`  
**Scope:** two authorized Gmail mailbox *draft metadata* lists; authenticated Google Calendar list, bounded event search and one event detail; approved GitHub source documents and native Email Watch config. No provider writes, new customer drafts, reminders, rule promotions, app grants, secrets, or Azure deployments.

## 1. Method and evidence boundaries

- GitHub branch: `feature/ea-vnext-m1-20261027`, draft PR #101. Prior head `481fc7934ee7ac17789d7056488175028dffc00f` had four GitHub workflows `success` (Security baseline, Repository security baseline, Dependency review, CodeQL). Any later head requires fresh CI readback.
- Current approved Calendar authority: `active-source/03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md`, source blob `66ca58343758e55dcddd679d498f2731e38a2fe3`, supported by 03B and PR #93 (merged 21 October).
- Current canonical hourly watch: `active-source/07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`, blob `65fc1d42bbac60828697192b0fb97c88c1bd14fd`; native watch inspected read-only and currently `condition_watch`/enabled.
- Two Drive 07B copies are dated 12 October and 29 September, respectively. They cannot be treated as current authoritative replacements for the GitHub file or 27 October live prompt.
- Sensitive provider message, draft, calendar or contact identifiers deliberately omitted from this public report.

## 2. Capability matrix (actual provider reads vs interface declaration)

| Interface / exact scope | Result | Evidence | Limitation and safe behavior |
| --- | --- | --- | --- |
| Business Gmail `list_drafts(max_results=10)` | `READ_PASS` | Four draft summaries, all labelled `DRAFT`; no next page in bounded result | This is an inventory snapshot only, not evidence all historical customer needs were addressed |
| Private Gmail `list_drafts(max_results=10)` | `READ_PASS / PARTIAL_PAGE` | Ten draft summaries and a provider next-page token | Do not call the first page a complete inventory |
| Gmail `create_draft` and `update_draft` input schema | `SCHEMA_VERIFIED / EXECUTION_NOT_TESTED` | Exposed fields include destination, body, reply anchor, draft ID and account connection but **no explicit `From`/send-as selector** | For an unverified required sender alias: `SENDER_ALIAS_UNVERIFIED`; do not silently substitute identity or create a customer-facing draft |
| Gmail draft-summary sender metadata | `UNVERIFIED` | `from` returned blank/not populated in the bounded draft summaries | Do not interpret blank From as correct or incorrect configured alias; avoid claims that alias is verified |
| Gmail quote-cleanup workflow | `HISTORICAL_EVIDENCE_ONLY` | 03F and earlier recovery ledger show same-draft update sometimes required and safety tools can reject updates | No create/update was performed for this M4 test; production QA remains separately gated |
| Calendar `list_calendars(max_results=15)` | `READ_PASS` | Eight visible calendars, a primary calendar and owner/writer access identified | Permissions and appointment presence do not imply notification delivery |
| Calendar `search`, primary, 20–31 October | `READ_PASS / BOUNDED` | Twenty matching follow-up events, no next page; summary response did not reliably expose reminder fields | Must use `read_event` to establish event-specific reminder state |
| Calendar `read_event` for one existing private follow-up | `READ_PASS` | `reminders.use_default=false`, empty override list, `private`, `transparent`, no attendees, confirmed event | This is **compliant with effective 03A/03B policy**; not a reminder-delivery failure |
| Calendar `create_event`/`update_event` interfaces | `SCHEMA_AVAILABLE / MUTATION_NOT_TESTED` | Reminders fields supported in read/update contracts | No event altered, no popup or notification scheduled in this task |
| Native Ea Business Email Watch | `CONFIGURATION_READ_PASS` | Enabled, `condition_watch`, hourly recurrence; full prompt and latest disposition accessible | Recorded scheduled task completion != all case work done; `delivery_status` unknown |

## 3. CR-01 effective-authority adjudication (NOT a policy amendment)

**Approved 20 October rule**, published in 03A and reaffirmed by merged PR #93: internal follow-ups and task/action events have **no popup or email reminder**; they must have `use_default=false`, `overrides=[]`. Meetings and genuine appointments preserve their distinct approved reminder settings.

**Contradictory native runtime instruction dated 27 October**, in the Email Watch's supplementary paragraph D, says: `If use_default=false and overrides=[], flag REMINDER_DISABLED` and that future private follow-ups should use a 30-minute popup `where authorized`. A subsequent run characterized disabled follow-up reminders as a workflow defect. This description conflicts with the currently approved no-reminder rule.

**Effective decision for this review:** Existing 03A/03B control remains binding unless a new exact operator policy approval supersedes it. `REMINDER_DISABLED` is a raw factual state, **not an error classification** for private internal follow-ups. For compliant entries classify `FOLLOWUP_REMINDERS_OFF_BY_POLICY`. Continue to track actual business follow-up deadlines via stateful case queue and Daily Calendar Briefing. A meeting reminder defect must be evaluated separately from internal follow-up reminders.

**Pending review, not implemented:** The operator may later approve one of: (A) retain no reminders; (B) establish a specified reminder rule for selected internal follow-ups with an explicit revision; or (C) use separate authorized notifications not implemented through Google Calendar event reminders. A change requires approval of target cohort, event/notification semantics and destination before updating native task prompts or Calendar events.

**Corrective implementation proposal:** In a **separate exact-scope approved** runtime/source change, remove the Email Watch assertion that reminder-free internal follow-ups are deficient and prevent fallback 30-minute popups. Preserve actual calendar-event data, compare source timestamps and read back the changed native task configuration. Do not adjust live behavior within this M4 audit.

## 4. M4 capability and reliability gaps

- **Alias control:** Gmail operations lack an explicit `From` selector. For the supplier reply earlier blocked by alias uncertainty, a draft cannot be called verified for the intended From identity using `create_draft` arguments alone. A mail-client/manual fallback can be proposed within approved sender scope.
- **Scope of search:** The recent Email Watch reported 21 controlled-cohort cases `PENDING_COVERAGE`; the read-only M4 probe did not process this business backlog.
- **Draft deletion:** A change in draft inventory count between runs is not evidence of operator deletion. Confirm 03D known suppression only from operator instruction or reliable evidence; do not recreate suppressed drafts.
- **Readback granularity:** Calendar summaries may omit reminder details; the concrete `read_event` result is required for reminder QA.
- **Notification delivery:** No system-push delivery proof. ChatGPT task `delivery_status=unknown` cannot establish or disprove notifications.
- **Persistent operations:** Existing GitHub backend is implemented/staged in-repository, but no accepted continuous production Gmail/Calendar/Drive synchronization. Azure issue #84 and Level 2B/C remain HOLD.

## 5. Acceptance / next stage

| Check | Status |
| --- | --- |
| Both authorized Gmail draft-metadata read surfaces reachable | PASS |
| Explicit Gmail sender-alias selection/proof available from exposed draft tool | NOT SUPPORTED |
| Calendar list/search/detail read surfaces reachable | PASS |
| Internal reminder-free Calendar event tested, source-consistent | PASS |
| Source-authority conflict exposed without live policy mutation | PASS |
| Gmail live create/update/reconcile and quote-removal retested | NOT TESTED — mutation gate |
| Complete 25-case cohort processed and all CRM stale records fixed | NOT TESTED — M5/ongoing operations |
| Persistent workflow controller / state backend live | NOT DEPLOYED |
| Production cutover / any Level 2B/C expansion | HOLD |

**Disposition:** M4 read-only provider capability review COMPLETE within bounded scope. A future, exact operator-approved M5 canary or separate runtime-policy repair may proceed only after the scope/ownership and current-source checks. This document is a proposal, not approved canonical policy.
