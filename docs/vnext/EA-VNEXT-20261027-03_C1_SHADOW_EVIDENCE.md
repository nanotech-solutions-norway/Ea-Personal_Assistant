# Ea vNext M5 C1 — Bounded Read-Only Shadow Acceptance Evidence

**Work ID:** `EA-VNEXT-20261027-03`  
**Date:** 27 October 2026, after 20:20 Europe/Oslo  
**Status:** `C1_BOUNDED_READ_COMPLETE / ACCEPTANCE_PARTIAL / EXTERNAL_WRITES_ZERO`  
**Parent:** `EA-VNEXT-20261027-02` merged PR #102 at commit `54a4ef78a172b7617e586e95a3972e8ee2fd96c8`.  
**Authority:** Current operator's instruction to proceed after reviewed PR #102. Scope remains read-only M5 C1 (at most five business cases) and controlled non-sensitive source documentation; **not** approval of C2 writes, Calendar changes, email sending, CRM mutations or M8 production cutover.
**Confidentiality:** Real case IDs, subjects, customer/employee names, correspondence, recipients, event links, commercial specifics and personal details are deliberately omitted from this **public** GitHub artifact. Private provider evidence was read directly but not replicated; avoid reconstructing private URLs from this document.

## Native task post-change observation

- 27 October hourly Email Watch configuration: `enabled=true`, `condition_watch`, hourly recurrence, corrected reminder classification present; old contradictory instruction absent.
- Latest observed post-repair scheduled run completed. This proves task execution, **not** queue clearance or delivery.
- The run recognized existing 30-minute popup overrides on three internal follow-ups as `FOLLOWUP_REMINDER_POLICY_MISMATCH`, and did not mark correctly disabled reminders as defective.
- Five priority cases were inspected by the native watch. No new drafts were created or sent. It still reported **20 controlled-cohort cases `PENDING_COVERAGE`**, older pending internal decisions, and two known reply-threading deficiencies.
- Native task notification delivery and durable autonomous work-state ledger remain `UNVERIFIED`.

## C1 independently verified provider reads

| Evidence slice | Scope / count | Disposition |
| --- | --- | --- |
| Gmail business conversation completeness | Five selected existing threads; returned totals matched total message count, none truncated | `5/5 FULL_THREAD_READ_PASS` |
| Gmail draft inventory | Four unsent business-account draft objects returned, no further pagination | `DRAFT_LIST_READ_PASS`; `From` alias could not be proved from blank draft-summary metadata |
| C1-A | Full customer request thread and one unsent reply in the **same** native thread | `WAITING_INTERNAL / VERIFIED_DRAFT_EXISTS`; never create duplicate |
| C1-B | Full technical sample inquiry and a subsequent sent reply | `WAITING_INTERNAL`; no new inbound answer requirement inferred |
| C1-C | Full supplier/formulation inquiry and a later sent answer | `WAITING_INTERNAL / SOURCE_VERIFICATION_REQUIRED`; no unsupported substitution |
| C1-D | Full current client exchange, latest response marked `SENT`; next step a future **telephone follow-up**, not another email | `FOLLOW_UP_REQUIRED / NO_DUPLICATE_EMAIL` |
| C1-E | Full existing textile business thread; recent sent correspondence; two separate technical draft threads are not the source correspondence | `DRAFT_THREADING_REVIEW_REQUIRED`, not `DRAFT_VERIFIED` |
| Calendar follow-up search | Bounded October–early November primary Calendar window returned 40 follow-up events, complete page | `SEARCH_PASS`; entries classified by event-detail reads only |
| Calendar event details | Seven existing private, transparent, attendee-free, 15-minute examples read | Three `FOLLOWUP_REMINDER_POLICY_MISMATCH`; four `FOLLOWUP_REMINDERS_OFF_BY_POLICY` |
| Calendar historical duplicates | Two case examples had multiple past follow-up entries | `HISTORICAL_DUPLICATE_RECONCILIATION_REQUIRED`, do not delete without scope/approval |
| CRM reference (stored Excel-format Drive artifact) | Bounded source fetch succeeded; last-modified metadata 22 October; status excerpts compared to newer Gmail/provider evidence | `CRM_STALE_STATUS_CANDIDATES`, **not** authoritative state overwrite; exact current CRM source/version must be confirmed |

### Observed limitations and no-success inflation

- The five verified threads are a deliberately selected bounded C1 sample, not a complete 25-case cohort scan or a representative random sample.
- “Most recent SENT” in a Gmail thread does not establish product sourcing, pricing, stock, shipping, legal or regulatory approval.
- An existing draft may still be unusable if the verified source sender alias is unsupported, its body contains unexpected quoted content, or the recipient/attachment differs. The one in-thread draft is verified **as in-thread and unsent**, not certified send-ready after full independent draft-body QA.
- The separate technical drafts cannot be silently moved or recreated; doing so risks duplicates and violates scope.
- Three popup mismatches are provider verified. Calendar search summaries are not reliable reminder evidence; `read_event` was used for each selected event.
- The Drive CRM reference resolved to an Excel-format stored file rather than a native editable Google Sheet, despite its supplied Sheets-shaped URL. Therefore **do not assume direct native range edits or conclude that this is the latest writable CRM master.**
- No controlled cohort backlog was closed; no missing provider action should be inferred completed from task-run completion.

## C1 acceptance matrix

| Gate | Status | Reason |
| --- | --- | --- |
| Read-only scope and zero customer/provider mutations | PASS | Only provider reads, non-sensitive GitHub preparation artifacts |
| 5 full-thread source checks | PASS | Five exact returned full thread counts and `truncated=false` |
| Current hourly post-change classification | PASS for inspected cases | Correct no-reminder policy and mismatch detection observed |
| Per-case dispositions source-bound | PASS in sampled cases | No missed draft automatically recreated or case silently closed |
| All 25 controlled cohort cases cleared | NOT MET | Twenty remain pending coverage in latest native watch |
| Sender alias and all draft bodies/attachments verified | NOT MET | Exposed draft tools have no explicit From selector; old draft threading issues |
| Provider-verified repair of 3 Calendar reminders | NOT PERFORMED | Requires explicit separate Calendar-change approval and pre/post event readback |
| CRM register correction and source writeback | NOT PERFORMED | Requires source confirmation and separate exact approval |
| Level 2A C2 actual provider write canary | NOT AUTHORIZED / NOT PERFORMED | Only bounded C1 read-only approved |
| M7 100 consecutive actionable cases / 14 days | NOT MET | A C1 sample never satisfies acceptance endurance |
| Level 2B/C or production cutover | HOLD | Explicit approval and separate deployment proof absent |

## Recommended independently gated repair batch

1. **R1 Calendar:** Identify the three verified historical popup mismatches, confirm per-event owner/type/exact canonical 03A scope, propose removal of popup override **without modifying event time, visibility, attendees or descriptions**, and perform provider readback only after explicit scoped approval. Historic instances remain evidence; any irrelevant past-event adjustment must be justified.
2. **R2 Gmail threading:** Review the two separate technical drafts against their original conversation, full body, attachment manifest, sender identity, 03D suppression and existing draft provenance. Propose a safe owner-approved in-place reconciliation; do **not** make an unthreaded replacement or bypass unsupported sender alias.
3. **R3 CRM:** Confirm actual current writable master, compare status rows to latest Gmail SENT and Calendar event before any individual write, preserve operator-closed cases. Avoid propagating stale Excel mirror metadata.
4. **R4 Fairness:** In a future bounded scheduled run, show oldest-overdue carried-forward case dispositions and case cursor, not just 5 recent cases, until all originally pending case IDs have an independently evidenced state.
5. **R5 Notification:** Keep Calendar event popup delivery, ChatGPT scheduled task delivery, and case-execution routing as separate systems. Do not claim delivery or add an external sending channel without authorization.
6. **R6 Level 2A C2 canary:** Before any **real** unsent Gmail or internal Calendar write, request an exact cohort, account, recipient/identity, event, suppression and business-case authorization; source-verify once more immediately before mutation.

**Exit status:** `C1_READ_ONLY_SAMPLE_COMPLETE / M5_NOT_ACCEPTED / NEXT_REPAIR_BATCH_PENDING_EXACT_AUTHORIZATION / LEVEL_2B_C_HOLD / CUTOVER_HOLD`.
