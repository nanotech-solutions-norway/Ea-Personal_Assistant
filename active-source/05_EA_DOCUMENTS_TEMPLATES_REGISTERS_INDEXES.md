# 05 — Ea Documents, Templates, Registers and Indexes

Status: READY_FOR_LEVEL_1_CUSTOMIZATION  
Authority: Active-source framework  
Level: Level 1 active

## Purpose
This file defines the reusable document, template, register and index layer for Ea.

## Required templates
- `EA_EMAIL_REPLY_TEMPLATE.md`
- `EA_GMAIL_DRAFT_FORMATTING_GUIDE.md`
- `EA_MEETING_MEMO_TEMPLATE.md`
- `EA_DUE_DILIGENCE_REPORT_TEMPLATE.md`
- `EA_DAILY_BRIEFING_TEMPLATE.md`
- `EA_FOLLOW_UP_TRACKER_TEMPLATE.md`
- `EA_LEAD_LIST_TEMPLATE.md`
- `EA_TRANSCRIPT_SUMMARY_TEMPLATE.md`
- `EA_MEETING_MINUTES_TEMPLATE.md`
- `EA_DECISION_LOG_TEMPLATE.md`
- `EA_LEGAL_REVIEW_MEMO_TEMPLATE.md`
- `EA_CONTRACT_RISK_TABLE_TEMPLATE.md`
- `EA_BUDGET_REVIEW_TEMPLATE.md`
- `EA_FINANCIAL_SUMMARY_TEMPLATE.md`
- `EA_TAX_NOTE_TEMPLATE.md`
- `EA_SKILL_CANDIDATE_PACK_TEMPLATE.md`
- `NTSN_INVOICE_GENERATION_STANDARD.md`
- `NTSN_INVOICE_VISUAL_QA_CHECKLIST.md`

## Required indexes/registers
- `EA_CONTACT_AND_COMPANY_INDEX.md`
- `EA_ACTIVE_PROJECTS_INDEX.md`
- `EA_PRODUCT_REFERENCE_MAP.md`
- `EA_PRICE_REFERENCE_MAP.md`
- `EA_APPLICATION_REFERENCE_MAP.md`
- `EA_EMAIL_SEARCH_QUERY_LIBRARY.md`
- `EA_STORAGE_INDEX.md`
- `EA_ATTACHMENT_CATALOG.md`
- `EA_COMPRESSED_FILE_CATALOG.md`
- `EA_DUE_DILIGENCE_RISK_SCORING.md`
- `EA_CONFIDENTIALITY_CLASSIFICATION.md`
- `EA_RECORDING_CONSENT_REGISTER.md`
- `EA_WRITEBACK_PERMISSION_REGISTER.md`
- `EA_LEGAL_RISK_REGISTER.md`
- `EA_FINANCIAL_ASSUMPTIONS_REGISTER.md`
- `EA_CALCULATION_AUDIT_LOG.md`
- `EA_SKILL_REGISTRY.md`
- `EA_PENDING_SKILL_REVIEW_REGISTER.md`
- `EA_CANONICAL_SKILL_REGISTER.md`
- `NTSN_INVOICE_VALIDATION_LOG.md`
- `NTSN_INVOICE_SOURCE_REFERENCE_REGISTER.md`

## Output format rules
| Output | Format |
|---|---|
| Protocols/workflows/logs/registers | `.md` |
| Editable reports/memos | `.docx` |
| Final distribution reports/memos | `.pdf` |
| Trackers/budgets/calculations | `.xlsx` / Google Sheets |
| Lightweight imports/exports | `.csv` |
| Backend schemas | `.json` / `.yaml` |

Invoice-specific output rule:
- Rendered PDF is the authoritative visual invoice output.
- DOCX is an editable working copy and must be re-rendered before approval.
- Customer-specific invoice files remain in controlled Drive/accounting storage, not GitHub.

## File naming conventions
- `Ea_Meeting_Memo_[Company]_[Topic]_[HHMM_DDMMYYYY].docx`
- `Ea_Due_Diligence_[Company]_[HHMM_DDMMYYYY].docx`
- `Ea_Email_Context_Summary_[Company]_[HHMM_DDMMYYYY].docx`
- `Ea_Session_Close_[Topic]_[HHMM_DDMMYYYY].md`
- `Ea_Legal_Review_[Company]_[Document]_[HHMM_DDMMYYYY].docx`
- `Ea_Financial_Review_[Topic]_[HHMM_DDMMYYYY].xlsx`
- English NTSN invoice: `Invoice15xxx.pdf`
- Norwegian NTSN invoice: `Faktura15xxx.pdf`
- Editable invoice working copy: same stem with `.docx`

## NTSN invoice template family

Status: USER_APPROVED operating logic, 28.07.2026.

- The NTSN invoice family is separate from the Onyx Scandinavia invoice family.
- NTSN invoice generation may use only NTSN-issued `Invoice15xxx` and `Faktura15xxx` files as historical visual references.
- Onyx invoices must not be used for NTSN logo placement, seller identity, payment information, legal footer or page geometry.
- The approved visual baseline uses one-page A4 geometry with logo upper left, customer block left, seller/invoice metadata right, a full-width item table, aligned VAT and total sections and payment information at the bottom.
- The official invoice number must be retrieved from the accounting/invoice register or explicit user instruction.
- A PDF render must pass visual QA before delivery.

### NTSN invoice visual QA minimum fields
| Check | Status | Evidence | Reviewer/date |
|---|---|---|---|
| NTSN-only source set used |  |  |  |
| Onyx reference set excluded |  |  |  |
| Official invoice number source confirmed |  |  |  |
| Logo clear of all text |  |  |  |
| Customer and seller blocks aligned |  |  |  |
| Invoice metadata aligned |  |  |  |
| Item columns aligned |  |  |  |
| Totals recalculate |  |  |  |
| VAT treatment source-supported |  |  |  |
| Payment details sourced from NTSN |  |  |  |
| One-page A4 output verified |  |  |  |
| Filename and language match |  |  |  |
| Sending/posting approval state recorded |  |  |  |

### NTSN invoice source register minimum fields
| Reference file | Language | Issuer verified as NTSN | Currency | VAT pattern | Layout relevance | Source location | Review date |
|---|---|---|---|---|---|---|---|

Do not place customer names, invoice content, bank details, accounting exports or confidential attachments in the public GitHub register. Use sanitized file-pattern and control metadata only.

## Product reference map minimum fields
| Product | Approved name | Use case | Key claims | Source | Status | Review date |
|---|---|---|---|---|---|---|

Product naming rules:
- Always write SiO₂/TiO₂.
- Hirec100 → Hirec-R.
- Hirec 450 water-based → Hirec PFW9.
- Hirec 450 solvent-based → Hirec PFS10.

## Follow-up tracker minimum fields
| Company | Contact | Email/domain | Case/project | Last inbound | Last outbound | Due | Status | Next action | Confidentiality note |
|---|---|---|---|---|---|---|---|---|---|

## Skill Candidate Pack template
Each new out-of-protocol skill must include:

- skill name;
- purpose;
- allowed tasks;
- disallowed tasks;
- source basis;
- risk classification;
- approval requirements;
- file/tool requirements;
- confidentiality rules;
- validation tests;
- recommended storage location;
- proposed authority level.
