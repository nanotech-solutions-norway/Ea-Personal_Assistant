# 05D — Commercial Document Reference-Only Naming and Versioned Google Drive Filing — 19.11.2026

**Status:** APPROVED / CANONICAL BY EXPLICIT OPERATOR INSTRUCTION (19.11.2026), subject to verified source promotion/readback.
**Scope:** NTSN-generated Quotes, Purchase Orders (PO), Requests for Quotation (RFQ; operator "PFQ" refers to the supplied RFQ folder), Packing Lists, Invoices and equivalent reference-numbered commercial documents. Internal drafting/filing only. Does not authorize sending, commercial approval, accounting release, or external commitments.

## 1. Unique filenames and revision references

1. **Use the exact document reference as the complete base filename.** Example: `PO-CITROX-20261119-01.pdf`. Use no `DRAFT`, `REV1`, `FINAL`, dates outside the reference, customer names or suffixes. Editable file formats, where required, use the same reference-only base.
2. **Retain every generated version separately.** A second separately generated draft of the same transaction must receive the next valid sequential reference, e.g. `PO-CITROX-20261119-02.pdf`; third `-03.pdf`. The reference printed inside the document, the downloadable file, the Gmail attachment and the Drive filename must match. Never rename a PDF alone if its printed reference is different.
3. Before assigning a reference, check the authoritative document register and actual destination folder (and related case) for collisions. Allocate a new sequence under the approved document-type numbering convention; do not invent missing or unverified references. **No silent overwrite, rename, move or deletion of prior versions.** If an earlier document has already been issued, preserve its released state and reference; a new draft must not silently amend it.
4. **Invoices are an accounting-controlled exception.** Preserve `Invoice[Number].pdf` and `Faktura[Number].pdf`, or an explicitly approved invoice reference. Never increment an issued invoice number or create a duplicate legal invoice simply to name a draft. Request a new, accounting-authorized number where required; block filing of an unnumbered or conflicting invoice and mark PENDING_REVIEW. Filing a draft does not constitute issuance, booking, tax approval or sending.

## 2. Operator-designated destination folders (verified 19.11.2026)

| Document | Canonical Google Drive parent folder ID | Company folder is named after |
| --- | --- | --- |
| Quote / quotation | `1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR` | Customer / quote recipient |
| PO / purchase order | `1etKL-OZEABsHxt9vkj5HjNidCwpH9ZjX` | Supplier / vendor |
| RFQ / request for quotation | `1OUNEbK-iNuVDV08VxLXb2zs9x66zU5Ck` | Supplier / vendor |
| Packing list | `1HDxtw0OhC00c98rxvL1WbOkqZ9LgDk9V` | Consignee / recipient company |
| Invoice | `17UTt1HjdaThZeu844NcKsNq4ygOhC8gX` | Billed customer, from existing approved invoice rule until operator gives another destination |

The **explicit user-selected PO root** `1etKL-OZEABsHxt9vkj5HjNidCwpH9ZjX` supersedes older, indexed historical PO root `1ozfYyGfU8vTbtojv9NBoXVK3cqCTR9RT` for this workflow. Do not merge folders or relocate historical records silently. The NTSN business Drive index is a partial navigation aid, not proof of current destination.

## 3. Each generated version: company-folder lookup and upload

1. Ground the document type, *actual company role and legal company name* from the document and current verified source. Inspect the exact operator-selected root, its existing child folders and identity/alias duplicates. If multiple companies or aliases make filing ambiguous, mark PENDING_REVIEW rather than guessing.
2. Reuse the correctly identified existing company subfolder. If none exists, **create exactly one child folder using the confirmed company name** matching existing sibling naming conventions. Verify the new folder ID, name and parent before upload.
3. From the moment this rule applies, **save every separately generated draft/version**, not just approved/final copies, within that company folder. This supersedes older restrictions in 05 and quote/invoice filing workflows **only for internal draft archival**. Drafts remain unapproved until authorized and must not be issued or dispatched merely because archived. Do not file directly in the root when a company subfolder is required.
4. Validate the actual PDF (render, layout, reference, currency, figures, status, signature), the filename/reference equality, company and target, the MIME type, file size and optional checksum. Upload once with an idempotency check and independently read back the new Drive ID, file name, parent and size. On ambiguous write outcome, query provider state before retrying.
5. Keep historical versions; never delete or overwrite for cosmetic corrections. Distinguish archival from approval and external release. No automatic bulk backfill of historical folders/chats without source and version mapping; explicitly report partial coverage.

## 4. Canonical precedence and controls

Current operator instruction > this scoped 05D naming/draft-filing rule > 05C PO PDF visual standard / other applicable document-specific design rules > existing 05A/05B/05 framework for unchanged topics. 05D **does not alter** the canonical PO logo, typography, signature, template design, PO commercial approval gates, invoice legal numbering/issuance safeguards, financial permissions, or the no-send rule.

For a new or newly revised document, enforce `[printed reference].[extension]`, folder reuse/create, retention of each version and provider readback. Use one redacted append-only work ledger for multi-step work; log only approved metadata/pointers in AI-Memory-Vault. Report `LOGGING_NOT_VERIFIED` if logging cannot be persisted.

**Source:** Direct operator instruction 19.11.2026 (this is a standing rule going forward); original source documents/quotes are evidence, not new instructions. Current PDF archival does not retroactively create or approve prior versions.
