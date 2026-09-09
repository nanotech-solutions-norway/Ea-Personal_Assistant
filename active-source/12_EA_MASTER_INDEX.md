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
| 03C_EA_HISTORICAL_EMAIL_CONTEXT_DRAFTING_RULE_0930_07082026.md | Mandatory review of prior email threads and NTSN sent replies before materially relevant drafting | Canonical / operator-instructed |
| 03D_EA_MANUAL_DRAFT_DELETION_SUPPRESSION_RULE_1111_09092026.md | Known operator-deleted Gmail drafts suppress automatic recreation until a new explicit drafting instruction | Approved / Canonical / operator-instructed |
| 04_EA_BUSINESS_DUE_DILIGENCE_LEGAL_FINANCIAL.md | Business support workflows | Active |
| 05_EA_DOCUMENTS_TEMPLATES_REGISTERS_INDEXES.md | Templates, registers and indexes | Active framework |
| 05A_EA_DOCUMENT_TEMPLATE_RECREATION_CONVERSION_STATIC_RULES_0349_08082026.md | Default rules for template creation, document drafting, conversion, recreation, extraction and template population for DOCX/PDF/XLSM | Canonical / operator-instructed |
| 05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md | Automatic canonical Quote, Packing List, RFQ and legacy editable PO template selection/use | Canonical / operator-instructed |
| 05C_EA_CANONICAL_PO_DRAFTING_PDF_LAYOUT_STANDARD_0219_09092026.md | Canonical PO drafting, A4 layout, Libre Baskerville typography, branding, signature placement and final-PDF QA | Canonical / operator-instructed |
| 06_EA_CUSTOM_GPT_AND_PROJECT_SETUP.md | GPT and Project setup | Active |
| 07_EA_SCHEDULED_TASKS_AND_ROUTINES.md | Scheduled routines and execution boundaries | Active |
| 07A_EA_GMAIL_BUSINESS_EMAIL_WATCH_PROMPT_2351_05082026.md | Historical approved hourly business-email schedule prompt | Canonical predecessor / supporting |
| 07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md | Current canonical hourly business-email draft/follow-up runtime source | Approved / Canonical / operator-instructed |
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
| `docs/EA_CLEANUP_RUN_1728_09092026.md` | Clean-up protocol authority/freshness/completeness/conflict/readback run | AUTO_APPROVED operational log; unresolved semantic drift remains PENDING_REVIEW |
| `docs/EA_DOCUMENT_TEMPLATE_STATIC_RULES_UPDATE_LOG_0349_08082026.md` | Implementation and validation log for the canonical document/template static rules | Approved / Canonical |
| `docs/decisions/EA_DECISION_DOCUMENT_TEMPLATE_STATIC_RULES_0349_08082026.md` | Operator decision establishing the document/template static rules | Approved / Canonical |
| `docs/decisions/EA_DECISION_CANONICAL_DOCUMENT_TEMPLATES_0405_08082026.md` | Operator decision establishing Quote/Packing List/RFQ/PO canonical templates | Approved / Canonical |
| `docs/decisions/EA_DECISION_CANONICAL_PO_DRAFTING_STANDARD_0219_09092026.md` | Operator decision establishing the 05C canonical PO drafting/final-PDF standard | Approved / Canonical |
| `registers/EA_CANONICAL_DOCUMENT_TEMPLATE_REGISTER_0405_08082026.md` | Canonical XLTM template filenames, Drive IDs, hashes and validation status | Approved / Canonical |
| `registers/EA_CANONICAL_PO_DRAFTING_STANDARD_REGISTER_0219_09092026.md` | Canonical PO rule, PDF reference, logo and legacy editable-template relationship | Approved / Canonical |
| `registers/EA_LABEL_CREATION_REGISTER.md` | Brother P-touch label workflow and validation history | Active operational register / regulatory release pending review |

## Precedence

Apply current explicit operator instructions first. For the hourly email watch, apply the sources in this order where a conflict exists:

1. `03D_EA_MANUAL_DRAFT_DELETION_SUPPRESSION_RULE_1111_09092026.md` for known operator-deleted draft suppression;
2. `07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md` as the current canonical hourly runtime source;
3. `07A_EA_GMAIL_BUSINESS_EMAIL_WATCH_PROMPT_2351_05082026.md` as predecessor/supporting authority where not superseded;
4. `03C_EA_HISTORICAL_EMAIL_CONTEXT_DRAFTING_RULE_0930_07082026.md`;
5. `03B_EA_CALENDAR_EXCLUSIONS_AND_DRAFT_MEETING_OVERRIDE_2351_05082026.md`;
6. `03A_EA_EMAIL_DRAFT_CHANNEL_OVERRIDE_1744_05082026.md`;
7. `03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md`;
8. `03_EA_EMAIL_CALENDAR_MEETING_WORKFLOWS.md`;
9. older CRM and follow-up implementation notes.

For document/template work, apply:

1. current explicit operator instruction;
2. the designated current APPROVED/CANONICAL document-specific workflow or explicitly designated alternative template;
3. `05C_EA_CANONICAL_PO_DRAFTING_PDF_LAYOUT_STANDARD_0219_09092026.md` for PO drafting and final PDF;
4. `05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md` for Quote, Packing List, RFQ and for PO editable-workbook retrieval/functionality when applicable;
5. `05A_EA_DOCUMENT_TEMPLATE_RECREATION_CONVERSION_STATIC_RULES_0349_08082026.md`;
6. `05_EA_DOCUMENTS_TEMPLATES_REGISTERS_INDEXES.md`;
7. current verified source files and connector evidence;
8. older supporting material.

For PO final PDF, 05C supersedes conflicting older 05B visual-layout requirements, including the old default requirement for Address/Website QR graphics. 05B continues to control the legacy functional XLTM/XLSM template when an editable Excel PO is explicitly requested or required.

## Operating rule

Use `active-source/` as the compact source of truth for ChatGPT Project operation. Keep the phase-package archive as build evidence.

Before materially relevant business-email drafting, review the complete current thread and relevant historical correspondence, with particular emphasis on prior NTSN sent replies. Historical replies guide tone, continuity, terminology and relationship context, but changeable facts must be revalidated against current reliable sources.

Known operator deletion of a Gmail draft is an intentional suppression signal under 03D. Automated hourly/recovery routines must not recreate that draft unless a new explicit operator drafting instruction authorizes the specific draft.

The live `Ea Business Email Watch` remains hourly and enabled. Canonical `condition_watch` versus live `exact_schedule` is an unresolved `CONTROL_PLANE_DRIFT / PENDING_REVIEW`; no clean-up routine may silently choose one. The live resilience additions are preserved as runtime evidence pending explicit reconciliation.

For template creation, document drafting, document conversion, document recreation, information extraction and recreation/template population involving DOCX, PDF, XLSX/XLSM or derived template formats, apply 05A automatically unless the operator explicitly overrides it. The operator does not need to restate those static rules for each request.

When the operator requests a Quote/quotation, Packing List or RFQ/Request for Quote, retrieve and use the corresponding registered canonical XLTM master under 05B automatically.

When the operator requests a PO/Purchase Order:
- apply 05C automatically for drafting and final fixed-layout PDF;
- use the 05C canonical PDF reference for visual layout only, never as a source of reusable transaction values;
- use current verified quotation/order evidence for prices, items and commercial terms;
- use Libre Baskerville for all visible PO text;
- use only the canonical top-right PO logo;
- preserve the grey divider under every Terms and conditions row;
- place the validated signature/stamp directly on the signature line;
- retrieve the legacy 05B PO XLTM only when an editable Excel PO is explicitly requested or functionally required.

Canonical template Drive folder: `Canonical Document Templates`, ID `19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`.

05C Drive file ID: `1L_MZD3Y-JnyI6nTHKV7E6eJAUsmtY8wp`.  
Canonical PO PDF reference ID: `1NliiqekZMO6Uii8vTXSs11aoFylXZ8CA`.  
Canonical PO top-right logo ID: `1V4KpZwpXteMHVOAFsZh68bc6juDtfAmq`.

Invoice, payment and customs matters may be reported when material, but must not create calendar entries. Draft meeting invitations follow the current Microsoft Teams location rule in the 03B override.

## Current status

Level 1 baseline: APPROVED for use on 06.07.2026. Post-approval canonical additions and runtime changes remain subject to the targeted validation/readback items below; this does not revoke the approved baseline.  
Level 2: HOLD. Planning or implementation requires separate explicit operator approval.

## Required validation

- manual hourly prompt test;
- full-thread, historical-correspondence and attachment-version test;
- notification deduplication test;
- invoice/customs calendar exclusion test;
- confirmed and proposed meeting test;
- Gmail/Inster channel test;
- NTT-AT address and Norwegian terminology test;
- document/template static-rule discovery and precedence test;
- canonical Quote/Packing List/RFQ template selection and Drive retrieval test;
- canonical 05C PO standard discovery and precedence test;
- canonical PO A4/Libre-Baskerville/top-right-logo/signature-on-line/terms-divider visual test;
- populated-template reconstruction and validation-copy test;
- DOCX/PDF/XLSM/XLTM preservation and output-format test;
- formula/validation/VBA-preservation test for canonical XLTM templates;
- target-sheet-only PDF preview/final-output test where legacy workbook rendering is explicitly requested;
- 03D manual-draft-deletion suppression test across hourly and recovery routines;
- explicit reconciliation decision for live `exact_schedule` vs canonical `condition_watch`, followed by synchronized runtime/source readback;
- external-action and Level 2 HOLD test.
