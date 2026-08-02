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
- `EA_QUOTATION_TEMPLATE_AND_DRIVE_FILING_WORKFLOW.md`
- `EA_INVOICE_APPROVAL_AND_DRIVE_FILING_WORKFLOW.md`

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
- `EA_LABEL_CREATION_REGISTER.md`

## Output format rules
| Output | Format |
|---|---|
| Protocols/workflows/logs/registers | `.md` |
| Editable reports/memos | `.docx` |
| Final distribution reports/memos | `.pdf` |
| Trackers/budgets/calculations | `.xlsx` / Google Sheets |
| Lightweight imports/exports | `.csv` |
| Brother P-touch labels | `.lbx` with `.png` preview and optional `.zip` package |
| Backend schemas | `.json` / `.yaml` |

## File naming conventions
- `Ea_Meeting_Memo_[Company]_[Topic]_[HHMM_DDMMYYYY].docx`
- `Ea_Due_Diligence_[Company]_[HHMM_DDMMYYYY].docx`
- `Ea_Email_Context_Summary_[Company]_[HHMM_DDMMYYYY].docx`
- `Ea_Session_Close_[Topic]_[HHMM_DDMMYYYY].md`
- `Ea_Legal_Review_[Company]_[Document]_[HHMM_DDMMYYYY].docx`
- `Ea_Financial_Review_[Topic]_[HHMM_DDMMYYYY].xlsx`
- `[Product]_62x102mm_[Language]_[Status].lbx`
- `Quotation - [Reference].pdf`
- `Invoice[Number].pdf`

## Product reference map minimum fields
| Product | Approved name | Use case | Key claims | Source | Status | Review date |
|---|---|---|---|---|---|---|

Product naming rules:
- Always write SiO₂/TiO₂.
- Hirec100 → Hirec-R.
- Hirec 450 water-based → Hirec PFW9.
- Hirec 450 solvent-based → Hirec PFS10.

## Label creation register minimum fields
| Product | Approved label name | SDS source/version/date | Label size | Orientation | Language | Pictograms | Signal word | H-statements | P-statements | UFI status | Supplier status | Output files | Release status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Label operating rules:
- Default label size is 62 mm width × 102 mm length, portrait, unless explicitly changed.
- Brother P-touch Editor `.lbx` is the primary editable format.
- Editable text objects are preferred; embedded images are limited to required pictograms or explicitly requested image-based versions.
- Use the largest practical font without clipping or omitting required text.
- Generate a PNG preview and package files together when useful.
- Use only approved customer-facing product names; source/legacy names remain internal references.
- Use the latest verified SDS as the classification source.
- Old, incomplete, conflicting, private-label-mismatched or UFI-incomplete SDS sources trigger `PENDING_REVIEW`.
- CLP/REACH/UFI/poison-centre/dangerous-goods and market-placement conclusions remain qualified-review-controlled.
- Confirm local-language requirements, open the `.lbx` in P-touch Editor and complete a physical print test before release.

## Quotation template and filing workflow

Status: APPROVED / CANONICAL as of 11:20, 02.08.2026.

Quotation drafting rules:
- Use the approved 2026 NanoTech Solutions Norway AS one-page A4 quotation design.
- Preserve the source logo/header, Customer and Vendor columns, Libre Baskerville typography and source font sizes, ruled terms table, grey items table, total block, note box, stamp/signature block and Main Office footer.
- Use the current quotation workbook and 2025–2026 quotation PDFs as the controlling layout evidence.
- Do not reconstruct quotations as plain-text documents.
- Do not use or merge the separate legacy 2023 blue-header quotation design unless explicitly instructed.
- Change only variable recipient, date, quotation reference, commercial terms, product, quantity, price, total and note fields.
- A quotation remains a draft until the operator explicitly approves the quotation content. Layout approval alone does not approve the commercial content.

Approved quotation Drive filing:
- Root: `https://drive.google.com/drive/folders/1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR`.
- After explicit operator approval, search for the recipient company folder and save the approved PDF there.
- If the company folder does not exist, create it under the root using the confirmed company name and the existing sibling-folder naming style.
- Do not create a new customer folder merely because a draft exists.
- Verify the PDF upload through Drive readback.

Post-approval quotation modifications:
- When the operator requests modifications after approval, overwrite the existing quotation PDF in the corresponding company folder.
- Preserve the quotation reference, filename and Drive file ID where technically possible.
- Do not create duplicate, `_v2`, `REVISED` or date-suffixed copies by default.
- Create a separate revision only when the operator explicitly requests one.
- Verify the replacement through Drive readback and treat the latest operator-approved file as active.

Invoice creation gate:
- Create the corresponding invoice only after quotation approval and operator confirmation, using the latest approved quotation as the commercial source unless explicitly changed.

## Invoice approval and Drive filing workflow

Status: APPROVED / CANONICAL as of 11:53, 02.08.2026.

Invoice approval rules:
- An invoice remains a draft until the operator explicitly approves its commercial content.
- Approval of a quotation does not by itself approve the invoice unless the operator explicitly confirms the invoice draft.
- Do not file an unapproved invoice draft in the invoice archive root.

Approved invoice Drive filing:
- Root: `https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`.
- After explicit operator approval, search the invoice root for the recipient company folder and save a PDF copy of the approved invoice there.
- If the company folder does not exist, create it under the invoice root using the confirmed company name and the existing sibling-folder naming style.
- Use the approved invoice number and filename, normally `Invoice[Number].pdf`.
- Do not create a customer folder merely because an invoice draft exists.
- Verify the file and parent folder through Drive readback.

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
