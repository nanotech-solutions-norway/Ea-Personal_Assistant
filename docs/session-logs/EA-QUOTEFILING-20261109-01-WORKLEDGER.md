# EA quotation draft filing — event ledger

Work ID: `EA-QUOTEFILING-20261109-01`  
Classification: Internal, redacted; customer details, commercial values and PDF payloads excluded.  
Authority: Operator's explicit request on 09.11.2026 to place two attached quotation PDFs in correct Google Drive folder and create folders if necessary. Filing does not approve commercial content.  
Policy: `docs/approved/EA_QUOTATION_TEMPLATE_AND_DRIVE_FILING_WORKFLOW_1120_02082026.md` (APPROVED/CANONICAL); `docs/approved/EA_QUOTATION_GENERATION_WORKFLOW_1111_05082026.md` (APPROVED/CANONICAL); global `protocols/operational_event_logging_rollback_CURRENT.md` (20.10.2026).  
Google Drive account: NTSN business connection; destination workspace root `1hkq3P-zfEutnwev9cduc1SQGshil3iN8`; customer archive `1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR` must not be used for drafts in customer subfolders.  

| Event | Phase | Actor/tool | Precondition / before | Planned effect / idempotency | Evidence/status | Next action |
|---|---|---|---|---|---|---|
| E001 | PREPARED | Ea / GitHub and Drive read | Both PDF originals marked pending review; business Drive quote archive and approved workflow verified; no matching Drive quote references found by exact search | Stage two exact-reference PDFs in a distinct draft-only folder; no external disclosure or commercial approval; key `EA-QUOTEFILING-20261109-01/PREPARED` | Source PDFs SHA-256: `22c032216558319e883c0d7616fe7857a5b1896625b6084e100eff76bc7560fa`, `0083df2be30f693d1f4464429e53bc06074f8d6b98a464bcd7f7a688ef2653da`; no Drive write yet | Create draft folder if absent, upload two copies with exact filenames, provider metadata readback |
| E002 | AUTHORIZED | Operator request | Explicit instruction permits Drive filing and necessary folder creation only | Upload/stage drafts; do not mark approved, create customer archive folders, share, email, invoice, or promote approval; attempt 1 | Scoped authorization confirmed; approvals on PDFs remain pending | Await provider output and log events |

| E003 | ATTEMPTED | Google Drive create_folder | No draft-only folder under verified `Quote & Invoice` parent | Created `00_Pending_Review_Quotation_Drafts`, ID `1YX9JAJIg3gqVoeh3yXRO89rz3vbsdtnb`; key `EA-QUOTEFILING-20261109-01/FOLDER`; attempt 1 | Connector success followed by folder metadata readback: parent `1hkq3P-zfEutnwev9cduc1SQGshil3iN8`; PASS | Upload only pending drafts |
| E004 | VERIFIED | Google Drive upload_file / get_file_metadata | Ref A absent via quote exact-reference search; local source SHA noted in E001 | Created `AA-20261108-01.pdf` ID `16bl-_acN7USQNEYMX2z89c95JUCNmBKa`; key `EA-QUOTEFILING-20261109-01/AA`; attempt 1 | Provider metadata size 491041 bytes, exact filename and destination parent `1YX9JAJIg3gqVoeh3yXRO89rz3vbsdtnb`; PASS | Preserve pending approval |
| E005 | VERIFIED | Google Drive upload_file / get_file_metadata | Ref S absent via quote exact-reference search; local source SHA noted in E001 | Created `SN-20261104-01.pdf` ID `1wFukRtUmNPi5e4-azjZxjFTXQO-F4ktx`; key `EA-QUOTEFILING-20261109-01/SN`; attempt 1 | Provider metadata size 359304 bytes, exact filename and destination parent `1YX9JAJIg3gqVoeh3yXRO89rz3vbsdtnb`; PASS | Preserve pending approval |
| E006 | READBACK | Google Drive list_folder | Before: folder newly created | After: exactly the two intended reference-only PDFs in folder; sizes 491041 and 359304 bytes | Full folder readback PASS, no other files; external sends/shares N/A | File approved quotation later only after operator's separate commercial approval |

## Closure
- **Google Drive staging: VERIFIED**, 2/2 raw PDFs filed under the separate draft-only working folder. This is not an approval of quoted content, transportation, DG, tax or claims.
- **Security:** NTSN business Drive account, no public sharing or customer file content in GitHub.
- **Rollback reference:** Drive file IDs and parent above; no rollback requested or performed. 
- **Open action:** Commercial approval remains pending for both quotes. No company archive folder was created.  
