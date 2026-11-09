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
