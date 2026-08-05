# Ea Schedule Prompt Update Log — 23:51, 05.08.2026

**Status:** APPROVED / CANONICAL  
**Category:** Workflow / Correction / Source reconciliation / Memory  
**Subsystems:** Scheduled tasks / Gmail / CRM / Calendar / Meetings / Learning

## Objective

Create a complete updated native Schedule prompt for the Ea business-email watch and synchronize the controlling logic across the Ea GitHub repository and Google Drive memory/log structure.

## Sources reviewed

### ChatGPT Project sources

- Runtime core
- Project learning and source authority
- Email, calendar and meeting workflows
- Scheduled tasks and routines
- QA and Level 2 HOLD files
- Product knowledge master, PENDING_REVIEW register, application map, source register and retrieval instructions

### GitHub

Repository: `nanotech-solutions-norway/Ea-Personal_Assistant`

Reviewed current active-source files, calendar and email overrides, email language profile, client/partner context, knowledge index and recent commits.

### Google Drive

Reviewed the Ea root folder, Phase 03 learning/memory folder, Phase 04 email/calendar folder, Phase 09 scheduled-task folder, the CRM operating instructions, writing-style rules, main project learning log and the email-draft-channel learning log.

## Material corrections incorporated

1. Do not create calendar entries for invoices, payment reminders, billing/collection notices, failed Autopay, subscription-payment matters, customs, Tolletaten or Altinn customs matters.
2. Suppress repeated notifications when a case has not materially changed.
3. Create or update Gmail drafts when a reply is needed, but do not notify merely because a draft exists.
4. Gmail is the default draft channel. Inster, Grupo Oesía and Tecnobit remain chat-only unless Gmail drafting is explicitly requested.
5. Verify the exact approved attachment version and remove superseded attachments when replacing a draft.
6. NTT-AT already has the NTSN address. Do not repeat it unless requested.
7. In Norwegian drafts, use `coating` instead of `belegg` for coating products and systems.
8. Proposed meeting events use `[DRAFT INVITE]`, no attendees, location `Microsoft Teams`, Teams details in the description and no Google Meet.
9. Confirmed meetings require exact date, time and timezone and duplicate checking.
10. Level 2 remains HOLD. The native task performs one bounded cycle per run and may not modify Drive/GitHub governance or claim autonomous backend operation.

## Conflict resolution

The older calendar default instructs Ea not to write `Microsoft Teams` in the location field. The current explicit operator instruction requires `Microsoft Teams` in the location field for private tentative `[DRAFT INVITE]` events. The newer instruction is recorded as the controlling exception for draft-invite events.

Older workflows permitted or previously created invoice and customs calendar reminders. Current operator instructions prohibit them. The prohibition is recorded as canonical and superseding.

The older person-based Espen Olsen drafting exception is superseded by the current recipient/project-based Inster exception.

## Files created or updated

### GitHub targets

- `active-source/07A_EA_GMAIL_BUSINESS_EMAIL_WATCH_PROMPT_2351_05082026.md`
- `active-source/03B_EA_CALENDAR_EXCLUSIONS_AND_DRAFT_MEETING_OVERRIDE_2351_05082026.md`
- `active-source/07_EA_SCHEDULED_TASKS_AND_ROUTINES.md`
- `active-source/12_EA_MASTER_INDEX.md`
- `active-source/ea_optimized_source_manifest.json`
- `knowledge/13_EA_SCHEDULED_EMAIL_WATCH_MEMORY.md`
- `knowledge/00_EA_KNOWLEDGE_INDEX.md`
- `docs/EA_SCHEDULE_PROMPT_UPDATE_LOG_2351_05082026.md`

### Google Drive targets

- Phase 09 scheduled-task prompt
- Phase 04 calendar override
- Phase 03 compact memory
- Phase 03 implementation/update log
- Main `EA_PROJECT_LEARNING_LOG.md` appended in place

## Confidentiality check

The prompt and logs contain sanitized operating rules only. They do not store passwords, tokens, bank details, private customer attachments, protected download credentials or confidential commercial correspondence.

## Validation status

The source reconciliation and file synchronization are complete when readback succeeds. The actual native scheduled task still requires a manual execution test before it should be treated as fully validated.
