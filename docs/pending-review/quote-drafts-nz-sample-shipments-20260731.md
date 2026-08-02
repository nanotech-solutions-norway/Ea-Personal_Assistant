# Quote and Invoice Register — 11:53, 02.08.2026

**Status:** APPROVED / INVOICED / ARCHIVED  
**Classification:** Commercial workflow metadata only; customer addresses, personal email addresses and correspondence are intentionally excluded because this repository is public.

## Approved commercial documents

| Quotation reference | Quoted items | Total | Invoice | Status |
|---|---|---:|---:|---|
| DP-20260731-01 | Hirec PFS10, 100 ml sample at no charge; FedEx transport EUR 89; processing and handling EUR 49 | EUR 138 | 15160 | Operator approved; quotation filed; invoice prepared and archived |
| ST-20260731-01 | TextileCoat65, 100 ml sample EUR 49; FabricCoat37, 100 ml sample EUR 49; FedEx transport EUR 89; processing and handling EUR 49 | EUR 236 | 15161 | Operator approved; quotation filed; invoice prepared and archived |

## Controls applied

- Currency: EUR.
- Payment terms: in advance.
- Invoice date: 02.08.2026.
- Due date: 05.08.2026.
- Forwarding agent: FedEx.
- VAT treatment: export 0%; final accounting/tax treatment remains subject to the official accounting system and qualified review.
- The approved quotation layout uses the canonical 2026 one-page A4 NanoTech Solutions Norway AS design.
- Neither Gmail draft was sent.

## Quotation Google Drive write-back

Quotation root: `https://drive.google.com/drive/folders/1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR`

| Document | Drive file ID | Parent company folder ID | Write status |
|---|---|---|---|
| Quotation DP-20260731-01 PDF | `1aeIILa2zAjX8M7ZS96vnBuYlhr4J0zBI` | `1Ql3eaM1RXto6SpP12bjk57G9BLirz0xh` | Existing PDF overwritten in place with approved layout; readback verified |
| Quotation ST-20260731-01 PDF | `1DJDQMciXPPuTyXYzo0TUflEvI0RdGlSB` | `18WsrYz_F1YIxn8jqwBNd74_-LSV9fqfd` | Existing PDF overwritten in place with approved layout; readback verified |

## Canonical invoice archive write-back

Invoice root: `https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

| Invoice | Company folder | Company folder ID | Canonical archive file ID | Status |
|---|---|---|---|---|
| Invoice15160.pdf | Mech Eng - Daniel Powley | `1GRwPXG8r2ir8iIUbS3Gq6b3FbXWkrMOB` | `1rZjrn7_zTAmOdOBj1MPLsNG1odyr0n7u` | Folder created; PDF copied; readback verified |
| Invoice15161.pdf | Sapro-Tech | `1zSFlcOAVsIuydMNy58ktX3UfeUIO7Tcw` | `1n0vi_EHi-qaQ1f6MfNuuP7uoBH9T4LaO` | Folder created; PDF copied; readback verified |

Earlier working copies remain in the quotation-company folders. They were not deleted because deletion was not requested. The invoice-root copies above are the canonical invoice archive copies.

## Gmail drafts

Replacement reply drafts were created in the existing correspondence threads with the approved quotation and corresponding invoice attached.

- DP replacement draft ID: `r-6185910603907869569`
- ST replacement draft ID: `r-3998732423201444125`
- External send status: **NOT SENT**

## Future invoice filing rule

After explicit operator approval of an invoice draft, save a PDF copy in the recipient company folder under the invoice root. If the folder does not exist, create it using the confirmed company name and the existing sibling-folder naming style. Do not create the folder or archive the invoice before operator approval. Verify every saved PDF and parent folder through Drive readback.

## Post-approval quotation modification rule

If the operator requests a later quotation modification, overwrite the existing quotation PDF in the quotation company folder, preserving the document reference, filename and Drive file ID where technically possible. Do not create duplicate or version-suffixed files unless explicitly requested.

## Next action

Await payment before arranging the FedEx shipments. External sending of the Gmail drafts requires explicit operator instruction.
