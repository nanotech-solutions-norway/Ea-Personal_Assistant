# 08 — Ea QA, Validation and Release Gate

Status: READY_FOR_LEVEL_1_VALIDATION  
Authority: Active-source framework  
Level: Level 1 active

## Purpose
Ea is not production-ready until the Level 1 validation gate passes.

## Release status definitions
| Status | Meaning |
|---|---|
| DRAFT | Files exist but are not validated |
| READY_FOR_VALIDATION | Configuration complete enough to test |
| VALIDATED | Test gate passed |
| APPROVED | User approved release |
| CANONICAL | Binding active version |
| HOLD | Not active until prerequisite complete |

## Required Level 1 tests

### Core governance
- Role and scope test.
- Approval matrix test.
- Confidentiality test.
- Source-authority test.
- Dynamic skill acquisition test.

### Email
- Related-thread search by sender.
- Related-thread search by domain.
- CC-recipient cross-check.
- External-safe draft reply.
- Approval-before-send test.

### Calendar
- Availability check.
- Invitation draft.
- Google Meet handling where supported.
- Teams link handling where supplied.
- Reschedule and cancellation approval test.

### Meeting
- Meeting memo generation.
- Transcript or notes summary.
- Decision and action extraction.
- Live written advice from manual transcript chunk.

### Due diligence
- Company identity review.
- Internal correspondence search.
- Risk rating.
- Business fit assessment.
- No final legal or compliance clearance claim.

### Legal and financial
- NDA or contract risk table.
- Clause suggestion marked non-final.
- Budget, cost and margin calculation.
- Tax or VAT note with verification caveat.
- No final legal, tax or accounting advice.

### Files
- Attachment summary.
- Storage index update draft.
- ZIP/RAR handling limits documented.
- Confidential file handling.

## Pass gate
Ea Level 1 may be released only if:

- no Critical failures;
- no unresolved Major failures;
- no approval-control failure;
- no confidentiality failure;
- no source-authority failure;
- no final legal, tax or accounting advice;
- no uncontrolled skill promotion;
- Level 2 remains on HOLD unless separately validated.

## Severity model
| Severity | Meaning |
|---|---|
| Critical | Approval, confidentiality or professional-boundary failure |
| Major | Core workflow wrong or misleading |
| Minor | Formatting, wording or recoverable process issue |
| Observation | Improvement suggestion |

## Validation matrix template
| Test ID | Category | Scenario | Expected behavior | Severity | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|

## Release checklist
- [ ] Active-source files uploaded.
- [ ] Project instruction block inserted.
- [ ] Custom GPT instruction block configured.
- [ ] Apps connected.
- [ ] Scheduled routines configured if desired.
- [ ] Level 1 QA passed.
- [ ] User approval recorded.
- [ ] Release manifest updated.
