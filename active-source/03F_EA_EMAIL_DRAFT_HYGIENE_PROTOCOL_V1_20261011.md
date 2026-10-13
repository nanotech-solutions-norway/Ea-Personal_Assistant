# Ea Email Draft Hygiene Protocol v1.0 — 11:27, 11.10.2026

**Status:** APPROVED / CANONICAL / OPERATOR-INSTRUCTED  
**Approved by:** Explicit operator instruction, 11.10.2026  
**Scope:** All new or materially updated Ea-generated Gmail drafts (manual, follow-up, hourly and scheduled), including NTSN sender aliases; internal test drafts  
**Effective authority:** Current instruction > this 03F rule for formatting/draft hygiene > 03D for operator-deleted draft suppression > 07B for current hourly execution > other approved rules.  
**Operational boundary:** Level 1 / Level 2A controlled internal drafts only; Level 2B and Level 2C HOLD; NO SEND.

## Latest explicit operator override — Gmail signature omission — 12.10.2026

**APPROVED/CANONICAL upon operator instruction; implementation through protected-branch PR.** Never insert a signature into ANY Gmail draft body. Gmail's standard signature is configured to be applied automatically by Gmail; Ea must not append sign-off name, job title, company address, contacts, legal footer or recreated signature block, even if the API readback does not show a Gmail UI signature. Validate **zero Ea-authored signatures in saved text and HTML**, without asserting that Gmail UI rendering can be proven by API readback. Retain native threading, same-draft quote removal and stored-body QA; historical audits and test results describe earlier behavior, not the new rule. Espen uses chat code blocks for manual Outlook copy, also without a hand-added signature by default. This explicitly supersedes all contrary “exactly one signature in the saved draft body” or “insert if not visible” wording below. 03D suppression and no-send/governance restrictions remain in force.

## Latest operator override — Espen Olsen / Outlook manual-copy workflow — 11.10.2026

**Status:** APPROVED / CANONICAL / latest explicit operator instruction. **Precedence:** This sender-specific rule supersedes all older Gmail-by-default, Inster relationship, send-as verification and signature-insertion instructions when Ea drafts an email **on behalf of Espen Olsen**.

- Draft every outbound message written on behalf of **Espen Olsen** **only in the ChatGPT conversation**, with the **complete email body in a fenced plain-text code block** suitable for copying manually to **Outlook**. Provide the **Subject:** clearly outside the code block for Outlook's separate subject field, plus optional recipient/CC outside the block when verified. Do not create or update a Gmail draft, and do not send or forward anything for Espen.
- Preserve salutation, paragraph spacing, natural closing and the correct sender-specific language/tone. **Omit Espen's signature block from the copied email body by default** to avoid duplication with Outlook's user-managed signature; include a specified signature only if the operator explicitly asks. Do not paste historical quotations or third-party legal disclaimers.
- Read available original Gmail correspondence and supporting evidence for context **read-only**, preserve recipient/CC/source provenance, verify facts and commitments, and perform **pre-output text QA**. Gmail draft IDs, native reply threading, post-save Gmail readback and Gmail send-as alias verification are **not applicable** to this manual Outlook drafting channel; do not report a Gmail draft as created or verified. Outlook message creation, actual send-as selection, signature insertion and sending are manual operator actions, not performed by Ea.
- **Sender-based, not recipient-based**: this rule applies whenever the email is authored on behalf of Espen, regardless of recipient/company (including Inster/Grupo Oesía/Tecnobit). If Ruben is the authorized sender in an Inster-related thread, apply the ordinary current workflow for Ruben unless the operator directs otherwise. The historical 03A recipient-based Inster chat-only exception does not govern Ruben's current default.
- Retain 03D **recipient-level manual-deletion suppression** for any automated Gmail-draft proposals; never treat a deleted draft as permission to recreate it. If an unsent Espen message is needed, provide the text in chat only. No retrospective rewriting of existing Gmail drafts or historical correspondence.
- No email sending, commercial/technical/regulatory commitments or confidentiality disclosures without separate approval. A later explicit instruction can supersede this sender-specific channel choice.

## Eight binding rules

1. **Native threading without copied quotations.** Read the full relevant conversation and historical sent replies for context. For a reply, use a valid Gmail `reply_message_id` from the active thread and preserve intended recipients/CC and Re: subject. Do **not** paste earlier messages, `On ... wrote:`, `>` quotation prefixes, headers or nested previous replies into Ea's new body. For newly composed messages, no artificial thread. If native threaded draft creation fails, classify `WRITE_FAILED` and notify operator; never create a misleading unthreaded customer reply.
2. **No manual signature in Gmail drafts.** Never author or inject a signature block into the stored Gmail draft. Gmail manages its standard signature automatically; do not compensate for its absence in the API output. Validate zero Ea-added signatures in saved body.
3. **Normalize spacing.** Standard Gmail text styling. No stray `>` lines, markdown source syntax, excessive blank lines, broken wrapped lines or repeated salutations/closings. Use exactly one blank line between logical paragraphs, short clear prose, and minimal purposeful formatting. Normal hyperlinks may be preserved; avoid copied markdown link syntax if unsupported in Gmail.
4. **No historical legal/disclaimer footer in newly authored body.** Omit quoted confidentiality statements (including third-party disclaimers) and earlier legal notices from the newly composed body. Do not alter or delete the originating Gmail message. If an explicitly approved NTSN outbound legal footer is mandatory, add only the correct footer once, distinct from copied third-party material.
5. **Sender-specific profiles and channels.** For **Ruben** and other approved non-Espen identities, validate the From/send-as account before any Gmail draft. For **Espen**, always use the latest sender-specific *chat-only code-block → manual Outlook copy* rule above: do not create Gmail drafts, do not claim Gmail send-as status, and do not include an Outlook-managed signature in the copy text by default. Sender-based Espen exception overrides older Gmail-by-default and recipient-based Inster routing.
6. **Post-write readback QA.** Before creation/update: verify original thread, latest reply anchor, recipient(s), CC/BCC, subject, language, attachments, exact sender/alias, active existing draft, known suppression state, and no unsupported commitments. After save: independently read back using Gmail draft listing and where supported draft-message read; verify draft/thread identity, addressing, subject, composed-body content, paragraph formatting, zero Ea-added signature, absence of copied quotation/disclaimer, attachments, no duplicate draft and DRAFT/not SENT state. Mark `DRAFT_VERIFIED` only for actually confirmed fields; mark partial/unverified items explicitly. Do not claim full readback without examining saved body.
7. **Deleted-draft suppression retained.** Apply current 03D exactly: known operator-manually-deleted drafts trigger `OPERATOR_DELETED_SUPPRESS_RECREATE` at **recipient level** until an explicit new instruction authorizes that specific draft. Missing draft alone is *not* evidence of manual deletion. Hygiene maintenance does not override suppression or authorize bulk draft recreation.
8. **Preserve original correspondence.** Never edit, replace, delete, archive or rewrite received/sent historical Gmail messages during draft hygiene operations. Do not strip evidence from originals, disclose third-party legal content, or repurpose confidential email quotations.

## Deterministic Gmail composing sequence

- Preflight: 03D suppression → read full thread/history → current source/fact/disclosure checks → identity/send-as alias validation → existing-draft reconciliation → attachment checks.
- Compose **only new response text**, without any signature block; no historical quote block. Use short paragraphs and a format-safe MIME body.
- Save exactly one draft in the original thread using native reply anchor; no send or forward.
- Read back independently and reconcile against expected `threadId + draftId`, recipient, CC, subject, new body and no Ea-authored signature block; check `DRAFT` label when supported and confirm no `SENT`.
- On failure: record `WRITE_FAILED`, `DRAFT_QA_PARTIAL`, `SENDER_ALIAS_UNVERIFIED` or `SIGNATURE_UI_UNVERIFIED` as applicable. Do not report success for unverified fields or create a fallback unthreaded customer message.

## Reconciliation with prior rules

- 03D manual deletion/recipient-level suppression remains controlling and unchanged.
- 07B hourly full-thread review, draft deduplication, source checks, Level 2A boundary and readback remain controlling. Its “no unnecessary signature block” means no duplicate or redundant hand-added signature, not “never include the authorized outgoing signature”.
- **Latest 11.10.2026 override controls:** all Espen-authored drafts are chat-only plain-text code blocks for manual Outlook copy. The prior Gmail-as-default/recipient-based Inster exception and Espen Gmail send-as gating are historical, not controlling for Espen.
- For Espen's manual Outlook copy, omit the sender's full signature because Outlook manages it; for Gmail drafts from other identities also omit the signature because Gmail manages it.
- No automatic retroactive changes to operator-edited existing drafts; audit/report first. No autonomous send, permission change, file deletion or external commitment authority is introduced.

## QA matrix and release status

| Check | Acceptance |
|---|---|
| Native reply | Draft thread ID equals anchor thread ID |
| New body | No raw quoted previous messages, `>` blocks, prior disclaimer or prior signatures |
| Signature | Zero signatures authored in draft body; standard Gmail signature controlled by Gmail UI (not proven by connector readback) |
| Formatting | Clear paragraphs, no redundant spacing or raw markdown artefacts |
| Recipients | Expected To/CC, subject and From identity; unsupported aliases block send-ready status |
| Suppression | Known operator deletion prevents unrequested recreation |
| Preservation | Historical messages unchanged |
| No-send | Draft exists under DRAFT; no outbound send |
| Readback | No false positives; partial validation recorded |

**Approval scope:** protocol/rule adoption and approved GitHub/Drive source updates and one safe *unsent* internal Gmail draft only. Gmail sending is expressly prohibited.  
**Promotion note:** This approved governance rule is immediately controlling, but operational connector/UI compliance must be separately validated; no passing test is presumed by this document.

## Live Gmail connector hardening — validated 11.10.2026

**Observed:** `create_draft(reply_message_id=...)` returned a valid threaded DRAFT but **automatically appended previous quoted correspondence**, despite supplying a clean text and HTML body. Initial saved-body readback therefore **FAILED** the no-quotation and one-signature checks. Creation success alone is insufficient.

**Validated remediation:** Immediately call `update_draft` on that same returned `draft_id`, supplying the exact clean `body` and `html_body` **without creating a new draft**. On the internal self-addressed test, this preserved the original `thread_id` and RFC `In-Reply-To` / `References` headers, retained `DRAFT`, removed quoted history, and yielded exactly one outgoing signature. The underlying `message_id` changed; draft identity stayed stable.

**Mandatory workflow for this connector:** for replies, create a threaded draft, then always perform the in-place body replacement/removal of auto-quoted history **before** marking the draft as ready; read back the current draft `message_id` and independently verify the full stored body. If update/readback fails, leave `DRAFT_QA_FAILED`, do not assert compliant formatting and do not send. Avoid recreating the draft to repair it. Preserve native thread identity. This connector behavior was verified in a single internal test; visual presentation and alias handling in other mailbox clients require separate checks.

**Gmail test evidence (internal, unsent):** thread `1a120bbf280383be`; draft `r6604447729229144822`; latest readback message `1a12a528a5f366b3`. Do not reuse the diagnostic anchor for customer correspondence.

## Live sender/signature audit — 12:44, 11.10.2026

A non-destructive audit of NTSN connected Gmail found a past `SENT` message whose `From` was Espen Olsen (`e.olsen@nanotech-solutions.com`) addressed to Inster/Oesía, but **its body contained both Espen and Ruben outgoing signature blocks**. This is evidence of a **historical two-signature formatting defect**, not proof of the correct approved Espen signature profile or currently configured Gmail send-as alias. Do not copy that entire signature body into new drafts. Current Gmail connector `create_draft`/`update_draft` surfaces do not expose a `From`/send-as selector or Gmail signature-settings read. Therefore classify new Inster draft requests `SENDER_ALIAS_UNVERIFIED` unless separately verifiable by an authorized interface; do not claim ready-to-send and do not send. Signature UI/mobile/desktop auto-insertion remains `SIGNATURE_UI_UNVERIFIED` until operator-verified.

The existing NTT-AT reply draft was audited read-only. It was correctly in-thread, labeled `DRAFT`, had no copied quote history and contained **no signature**. Classify it `EXISTING_DRAFT_SIGNATURE_REVIEW`; never silently rewrite existing customer drafts during global hygiene rollout. If it is explicitly approved for modification, revalidate live thread/source context, append only the correct single sender signature, and read back. No customer draft or historical original correspondence was changed during this audit.

03D suppression remains statically verified only; a destructive simulation of manually deleted drafts is NOT approved and is unnecessary for implementation. UI verification and sender-identity signoff are PENDING_REVIEW, not a failure of approved 03F governance.
