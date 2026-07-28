# 12 — Ea Master Index

Status: ACTIVE_INDEX  
Authority: Active-source framework

## Active-source files

| File | Purpose | Status |
|---|---|---|
| 00_EA_PROJECT_README_AND_UPLOAD_PLAN.md | Upload and use strategy | Active |
| 01_EA_RUNTIME_CORE.md | Core runtime and approval rules | Active |
| 02_EA_PROJECT_LEARNING_AND_SOURCE_AUTHORITY.md | Learning and source authority | Active |
| 03_EA_EMAIL_CALENDAR_MEETING_WORKFLOWS.md | Secretary workflows | Active |
| 04_EA_BUSINESS_DUE_DILIGENCE_LEGAL_FINANCIAL.md | Business support workflows | Active; includes NTSN invoice controls |
| 05_EA_DOCUMENTS_TEMPLATES_REGISTERS_INDEXES.md | Templates, registers and indexes | Active framework; includes NTSN invoice template family |
| 06_EA_CUSTOM_GPT_AND_PROJECT_SETUP.md | GPT and Project setup | Active |
| 07_EA_SCHEDULED_TASKS_AND_ROUTINES.md | Scheduled routines | Active framework |
| 08_EA_QA_VALIDATION_RELEASE_GATE.md | QA and release gate | Active |
| 09_EA_LEVEL_2_MANAGED_BACKEND.md | Future backend design | HOLD |
| 10_EA_PHASE_VALIDATION_TRACKER.md | Validation tracker | Active |
| 11_EA_IMPLEMENTATION_BLUEPRINT.md | Build order | Active |
| 12_EA_MASTER_INDEX.md | Index | Active |
| ea_optimized_source_manifest.json | Manifest | Active |

## Related approved operating standards

| File | Purpose | Classification |
|---|---|---|
| `docs/canonical-rules/NTSN_INVOICE_GENERATION_STANDARD.md` | Sanitized NTSN invoice drafting, source, layout, VAT, QA and approval controls | USER_APPROVED / AUTO_APPROVED operating logic |
| `validation/NTSN_INVOICE_GENERATION_VALIDATION_20260728.md` | Sanitized validation record for the approved invoice baseline | VALIDATED |

Customer-specific invoices, bank details, prices linked to identifiable customers and accounting records remain in controlled Drive/accounting storage and are not indexed as public GitHub content.

## Operating rule
Use `active-source/` as the compact source-of-truth for ChatGPT Project operation. Keep the 89-file phase package as archive/build evidence.

For NTSN invoice drafting, apply the approved Drive operating standard and the sanitized GitHub canonical rule. Use only NTSN-issued `Invoice15xxx` / `Faktura15xxx` references and exclude Onyx Scandinavia invoices.

## Current status
Level 1: configured framework pending validation.  
Level 2: HOLD pending Level 1 finalization and validation.

## Required customization before production
- project/contact indexes;
- active project index;
- product, price and application maps;
- email query library;
- source registers;
- write-back permission register;
- QA test evidence.
