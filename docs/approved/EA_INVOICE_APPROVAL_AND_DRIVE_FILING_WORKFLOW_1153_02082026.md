# Ea Invoice Approval and Drive Filing Workflow — 11:53, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Invoices / Google Drive

## Approval boundary

An invoice remains a draft until the operator explicitly approves its commercial content. Approval of the related quotation does not automatically approve the invoice unless the operator explicitly confirms the invoice draft.

## Approved invoice archive root

`https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

## Filing workflow

After explicit operator approval of an invoice draft:

1. Search the invoice archive root for the recipient company folder.
2. Save a PDF copy of the approved invoice in the existing company folder.
3. If no company folder exists, create one under the invoice archive root using the confirmed company name and the naming style of the existing sibling folders.
4. Use the approved invoice number and filename, normally `Invoice[Number].pdf`.
5. Verify the saved PDF, file size and parent folder through Google Drive readback.

Do not create a customer folder or save an invoice PDF in this archive merely because an invoice draft exists.

## Current migration record

The following operator-approved invoices were copied into newly created company folders under the approved invoice archive root on 02.08.2026:

| Invoice | Company folder | Canonical archive file ID | Status |
|---|---|---|---|
| Invoice15160.pdf | Mech Eng - Daniel Powley | `1rZjrn7_zTAmOdOBj1MPLsNG1odyr0n7u` | Copied and readback verified |
| Invoice15161.pdf | Sapro-Tech | `1n0vi_EHi-qaQ1f6MfNuuP7uoBH9T4LaO` | Copied and readback verified |

## Confidentiality

Public GitHub records must exclude customer addresses, personal email addresses, banking details and confidential correspondence. Approved invoice PDFs belong in the access-controlled Google Drive company folders.
