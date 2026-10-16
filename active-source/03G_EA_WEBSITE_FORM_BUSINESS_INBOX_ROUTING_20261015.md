# 03G — Ea Website-Form Enquiry to Business-Mailbox Routing
Status: OPERATOR_INSTRUCTED / APPROVED_RULE; automated cross-account delivery PENDING_IMPLEMENTATION_VALIDATION
Instruction date: 15.10.2026
Scope: New incoming website-form notifications on an operator-connected personal Gmail inbox that belong to NanoTech Solutions Norway AS.

## Classification trigger
- When a new notification arrives in the configured personal Gmail INBOX with a verified company website-form notification identity (e.g. display name "NanoTech Solutions Norway" and sender mail@nanotech-solutions.com) and a recognizable new-form-submission subject (e.g. "Hirec fikk en ny innlevering" or equivalent product/form-specific variants), classify its substance as a business enquiry for NanoTech Solutions Norway AS, not as personal correspondence.
- Do not trust display name or superficial subject similarity alone. Inspect origin, content, actual form fields, Reply-To, and any inconsistencies; suspicious/ambiguous messages are flagged for operator review.
- Do not classify ordinary direct customer messages or third-party spoofed emails as this notification type merely on partial sender/subject similarity.

## Reply and business account
- Extract the *actual enquirer* from the authenticated Reply-To header or website-form E-mail field. Do not reply to the notification system address unless the operator expressly directs it.
- Prepare the customer-facing reply in the connected NTSN business Gmail account using the configured authorized Ruben business send-as alias. Verify the resulting draft's actual From identity in Gmail after creation. If the alias is not verifiable, flag SENDER_ALIAS_UNVERIFIED and do not claim it is send-ready.
- Search related customer/technical correspondence, consult current approved source evidence, preserve latest sender-specific drafting, suppression and Gmail draft-hygiene rules. Draft only; never send without separate explicit approval.
- Since the originating message is in a different Gmail account, an external customer reply may start a new business-account thread with a descriptive subject. Do not falsely claim cross-account native reply threading.

## Dual-inbox routing
- Preserve the original website notification in the originating personal Gmail mailbox. Maintain a copy in the configured NTSN business Gmail INBOX, preserving the original notification text and customer submission fields.
- Current connector-supported one-time method: explicitly authorized forward of the original website notification from the source mailbox to the NTSN business inbox; verify receipt on the destination mailbox. This is a forwarded *copy*, not a Gmail-native move across accounts.
- Avoid forwarding loops and duplicates: reconcile by source message ID, date, submitter address and subject. Do not repeat forwarding when the same submission already exists in the business mailbox.
- General autonomous forwarding/filter creation, background routing and unattended cross-account writes are PENDING_IMPLEMENTATION_VALIDATION, not proven active by documentation. Only run one-time forwards upon explicit operator authorization or under a separately approved and technically verified routing mechanism.
- Do not archive, trash or modify original evidence without authorization.

## Security and provenance
- Do not store the private/personal email account mapping or private customer form content in a public repository. Exact mailbox addresses and routing configuration belong in access-controlled operator records, not this policy text.
- Never conflate the notifying website sender with the actual customer. Keep customer communications under NTSN's business records; do not expose private-account metadata to unrelated parties.
- Log routing decision, source reference, destination inbox readback, draft identity, draft sender verification, and any unverified automation steps.

## Acceptance
1. Correctly identify genuine website form inquiry and actual Reply-To customer, rejecting near-match spoofing.
2. Preserve original and independently verify the single business-inbox copy.
3. Save at most one unsent Gmail draft to the actual enquirer with business From identity confirmed by readback; comply with clean-body, no-signature and deletion-suppression policies.
4. Never assert continuous automation until a supported always-on Gmail rule/workflow is explicitly configured and tested.
5. Stop when these acceptance criteria are met; new work only for material gap, new operator requirement or justified recommendation.
