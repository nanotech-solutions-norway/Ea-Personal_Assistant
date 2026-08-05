# 12 — Ea Master Index

Status: ACTIVE_INDEX  
Authority: Active-source framework

## Active-source files

| File | Purpose | Status |
|---|---|---|
| 00_EA_PROJECT_README_AND_UPLOAD_PLAN.md | Upload and use strategy | Active |
| 01_EA_RUNTIME_CORE.md | Core runtime and approval rules | Active |
| 02_EA_PROJECT_LEARNING_AND_SOURCE_AUTHORITY.md | Learning and source authority | Active |
| 03_EA_EMAIL_CALENDAR_MEETING_WORKFLOWS.md | Email, calendar and meeting workflows | Active |
| 03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md | Calendar-entry defaults, urgency colors and reminders | Canonical / user-instructed |
| 03A_EA_EMAIL_DRAFT_CHANNEL_OVERRIDE_1744_05082026.md | Gmail-by-default with Inster relationship exception | Canonical / operator-instructed |
| 03B_EA_CALENDAR_EXCLUSIONS_AND_DRAFT_MEETING_OVERRIDE_2351_05082026.md | Invoice/customs calendar exclusions and current draft-invite Teams handling | Canonical / operator-instructed |
| 04_EA_BUSINESS_DUE_DILIGENCE_LEGAL_FINANCIAL.md | Business support workflows | Active |
| 05_EA_DOCUMENTS_TEMPLATES_REGISTERS_INDEXES.md | Templates, registers and indexes | Active framework |
| 06_EA_CUSTOM_GPT_AND_PROJECT_SETUP.md | GPT and Project setup | Active |
| 07_EA_SCHEDULED_TASKS_AND_ROUTINES.md | Scheduled routines and execution boundaries | Active |
| 07A_EA_GMAIL_BUSINESS_EMAIL_WATCH_PROMPT_2351_05082026.md | Complete hourly business-email schedule prompt | Canonical / operator-instructed |
| 08_EA_QA_VALIDATION_RELEASE_GATE.md | QA and release gate | Active |
| 09_EA_LEVEL_2_MANAGED_BACKEND.md | Future backend design | HOLD |
| 10_EA_PHASE_VALIDATION_TRACKER.md | Validation tracker | Active |
| 11_EA_IMPLEMENTATION_BLUEPRINT.md | Build order | Active |
| 12_EA_MASTER_INDEX.md | Index | Active |
| ea_optimized_source_manifest.json | Active-source manifest | Active |

## Knowledge and operational records

| File | Purpose | Status |
|---|---|---|
| `knowledge/13_EA_SCHEDULED_EMAIL_WATCH_MEMORY.md` | Compact canonical memory for the hourly email watch | Approved / Canonical |
| `docs/EA_SCHEDULE_PROMPT_UPDATE_LOG_2351_05082026.md` | Source reconciliation and implementation log | Approved / Canonical |
| `registers/EA_LABEL_CREATION_REGISTER.md` | Brother P-touch label workflow and validation history | Active operational register / regulatory release pending review |

## Precedence

Apply current explicit operator instructions first. For the hourly email watch, apply the sources in this order where a conflict exists:

1. `07A_EA_GMAIL_BUSINESS_EMAIL_WATCH_PROMPT_2351_05082026.md`
2. `03B_EA_CALENDAR_EXCLUSIONS_AND_DRAFT_MEETING_OVERRIDE_2351_05082026.md`
3. `03A_EA_EMAIL_DRAFT_CHANNEL_OVERRIDE_1744_05082026.md`
4. `03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md`
5. `03_EA_EMAIL_CALENDAR_MEETING_WORKFLOWS.md`
6. Older CRM and follow-up implementation notes

## Operating rule

Use `active-source/` as the compact source of truth for ChatGPT Project operation. Keep the phase-package archive as build evidence.

Invoice, payment and customs matters may be reported when material, but must not create calendar entries. Draft meeting invitations follow the current Microsoft Teams location rule in the 03B override.

## Current status

Level 1: configured framework pending full QA validation.  
Level 2: HOLD pending Level 1 finalization and validation.

## Required validation

- manual hourly prompt test;
- full-thread and attachment-version test;
- notification deduplication test;
- invoice/customs calendar exclusion test;
- confirmed and proposed meeting test;
- Gmail/Inster channel test;
- NTT-AT address and Norwegian terminology test;
- external-action and Level 2 HOLD test.
