# Security Policy — 23:59, 27.07.2026

## Scope

This repository stores Ea model configuration, operating protocols, validation evidence and future managed-automation design. It is not an approved store for mailbox contents, calendar data, customer records, CRM exports, personal correspondence or credentials.

## Prohibited content

Do not commit Gmail/Calendar/Drive tokens, passwords, private keys, customer or supplier confidential data, bank/accounting data, raw email bodies or attachments, personal schedules, sensitive personal data, production connector payloads or unredacted CRM records.

## Reporting and response

Do not report secrets or private correspondence in a public issue. Contact the owner through an established private channel. For suspected exposure: disable affected automation, revoke/rotate credentials outside GitHub, preserve minimal evidence, remove unsafe artifacts, inspect history/logs, assess privacy/contractual duties and restore only after validation.

Changes affecting external communications, calendar writes, CRM write-back, connector permissions or Level 2 automation require controlled pull-request review and explicit approval boundaries. Repository transfer remains on hold.
