# Ea Knowledge Source and Update Protocol

Status: DRAFT  
Priority: Critical

## Purpose

Define how Ea knowledge is captured, reviewed, stored, approved, updated and deprecated.

## Storage model

| Knowledge type | Primary storage | Notes |
|---|---|---|
| Approved structured knowledge | GitHub `knowledge/` | Version-controlled |
| Active compact summaries | Ea Project | Operational use |
| Stable sanitized knowledge | Custom GPT | Runtime reference |
| Evidence/source material | Gmail, Drive, Calendar, Contacts, GitHub, web | Not automatically canonical |
| Generated reports/memos | Drive and/or GitHub validation folders | Output/evidence |

## Update process

1. Capture evidence.
2. Extract proposed knowledge.
3. Classify sensitivity.
4. Classify status: DRAFT, AUTO_APPROVED, PENDING_REVIEW, APPROVED, CANONICAL or DEPRECATED.
5. Validate against source authority.
6. Update relevant knowledge file.
7. Update validation register.
8. Update changelog.
9. Request approval for high-risk knowledge.

## Source authority

1. Current explicit user instruction.
2. Approved/CANONICAL Ea protocol and knowledge files.
3. Approved Ea learning logs and decision registers.
4. Current verified evidence from Gmail, Drive, Calendar, Contacts, GitHub and web.
5. Older chats/files as supporting context only.

## Always PENDING_REVIEW

- Pricing.
- Warranty.
- Delivery commitments.
- Legal interpretations.
- Tax/accounting rules.
- Product performance claims.
- Public marketing claims.
- Customer confidentiality rules.
- Supplier exclusivity terms.
- Discount rules.
- Compliance content.
- New high-risk skills.

## Deprecation rule

When knowledge is replaced, mark the old entry DEPRECATED, keep a source note, and add the change to `12_EA_KNOWLEDGE_CHANGELOG.md`.
