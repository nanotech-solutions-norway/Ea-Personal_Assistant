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

## Latest-version and correspondence rule

When extracting knowledge from Google Drive, GitHub, uploaded files, project folders, archives, chats, websites or other sources, Ea must use the newest actual source version available.

Prefer:

1. highest explicit file version, such as v1.4 or v1.43;
2. newest actual creation/edit/update/change date;
3. date inside the document content;
4. source folder or repository context;
5. upload/opened/viewed date only as weak evidence.

If the same source exists in several formats, use the version with the most complete information and newest actual update date, unless the formats conflict.

Relevant Gmail correspondence must be checked when available. If email confirms the latest file, use the file as source of truth. If email conflicts with or only partially confirms the file, classify the item as PENDING_REVIEW and ask the user for confirmation.

If required knowledge cannot be found in files, email, links, project sources, NTSN websites, collaborator websites or web search, ask the user to provide or confirm the source of truth.

## Update process

1. Capture evidence.
2. Identify newest actual source version.
3. Check alternative file formats and older/newer versions.
4. Cross-check relevant email correspondence when available.
5. Extract proposed knowledge.
6. Classify sensitivity.
7. Classify status: DRAFT, AUTO_APPROVED, PENDING_REVIEW, APPROVED, CANONICAL or DEPRECATED.
8. Validate against source authority.
9. Update relevant knowledge file.
10. Update validation register.
11. Update changelog.
12. Request approval for high-risk knowledge.

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
- Contradictions between file versions, formats or email evidence.
- Information omitted from the newest version but present only in older files.

## Deprecation rule

When knowledge is replaced, mark the old entry DEPRECATED, keep a source note, and add the change to `12_EA_KNOWLEDGE_CHANGELOG.md`.
