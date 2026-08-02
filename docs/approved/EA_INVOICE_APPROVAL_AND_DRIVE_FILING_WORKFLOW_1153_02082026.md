# Ea Invoice Approval and Drive Filing Workflow — 12:35, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Invoices / Google Drive / Gmail

## Approval boundary

An invoice remains a draft until the operator explicitly approves its commercial content. Approval of the related quotation does not automatically approve the invoice unless the operator explicitly confirms the invoice draft.

## Approved invoice archive root

`https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

## Canonical invoice naming

- Use the approved invoice reference and established language prefix as the complete filename.
- English: `Invoice[Number].pdf`, for example `Invoice15160.pdf`.
- Norwegian: `Faktura[Number].pdf`, for example `Faktura15160.pdf`.
- Do not add customer names, dates, `FINAL`, `APPROVED`, revision labels or other descriptive text.
- Use the same exact filename in Gmail attachments, working folders and the canonical invoice archive.
- A replacement that requires a new invoice must receive the next accounting-controlled invoice number. Do not create `_v2`, `REVISED` or arbitrary sequence suffixes.

## Filing workflow

After explicit operator approval of an invoice draft:

1. Search the invoice archive root for the recipient company folder.
2. Save a PDF copy of the approved invoice in the existing company folder.
3. If no company folder exists, create one under the invoice archive root using the confirmed company name and the naming style of the existing sibling folders.
4. Use only the canonical invoice filename.
5. Verify the saved PDF, filename, file size and parent folder through Google Drive readback.

Do not create a customer folder or save an invoice PDF in this archive merely because an invoice draft exists.

## Current archive record

| Invoice | Company folder | Canonical archive file ID | Status |
|---|---|---|---|
| Invoice15160.pdf | Mech Eng - Daniel Powley | `1rZjrn7_zTAmOdOBj1MPLsNG1odyr0n7u` | Filename compliant; readback verified |
| Invoice15161.pdf | Sapro-Tech | `1n0vi_EHi-qaQ1f6MfNuuP7uoBH9T4LaO` | Filename compliant; readback verified |

## Gmail attachment control

When an invoice is attached to a Gmail draft, use the same canonical invoice filename. Discard superseded drafts when instructed, recreate the draft in the existing customer thread, verify the attachment filename and leave the draft unsent until explicitly approved for sending.

## Confidentiality

Public GitHub records must exclude customer addresses, personal email addresses, banking details and confidential correspondence. Approved invoice PDFs belong in the access-controlled Google Drive company folders.
