# Ea Project Learning Log — Invoice Approval and Filing — 11:53, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Category:** Decision / Workflow / Validation  
**Subsystem:** Documents / Files / Google Drive

## Decision

Approved invoice PDFs are archived separately from quotations.

## Canonical rule

After explicit operator approval of an invoice draft, save a PDF copy in the recipient company folder under:

`https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

If the company folder does not exist, create it using the confirmed company name and the naming style of the existing sibling folders. Do not create a folder or archive an invoice before operator approval. Verify the file and parent folder through Drive readback.

## Action taken

- Created invoice folder `Mech Eng - Daniel Powley` and archived `Invoice15160.pdf`.
- Created invoice folder `Sapro-Tech` and archived `Invoice15161.pdf`.
- Retained earlier working copies in quotation folders because deletion was not requested.
- Updated GitHub active-source and approved workflow records.

## Confidentiality check

No customer addresses, personal email addresses, bank information or confidential correspondence are stored in this workflow log.
