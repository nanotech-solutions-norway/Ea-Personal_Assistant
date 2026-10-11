# Ea Email Draft Hygiene Protocol v1.0 — 11:27, 11.10.2026

**Status:** APPROVED / CANONICAL / OPERATOR-INSTRUCTED  
**Approved by:** Explicit operator instruction, 11.10.2026  
**Scope:** All new or materially updated Ea-generated Gmail drafts (manual, follow-up, hourly and scheduled), including NTSN sender aliases; internal test drafts  
**Effective authority:** Current instruction > this 03F rule for formatting/draft hygiene > 03D for operator-deleted draft suppression > 07B for current hourly execution > other approved rules.  
**Operational boundary:** Level 1 / Level 2A controlled internal drafts only; Level 2B and Level 2C HOLD; NO SEND.

## Eight binding rules

1. **Native threading without copied quotations.** Read the full relevant conversation and historical sent replies for context. For a reply, use a valid Gmail `reply_message_id` from the active thread and preserve intended recipients/CC and Re: subject. Do **not** paste earlier messages, `On ... wrote:`, `>` quotation prefixes, headers or nested previous replies into Ea's new body. For newly composed messages, no artificial thread. If native threaded draft creation fails, classify `WRITE_FAILED` and notify operator; never create a misleading unthreaded customer reply.
2. **Exactly one outgoing signature.** Keep historical signatures only inside existing original messages. In the *new draft*, use a single approved sender-specific signature when required for a ready-to-send draft. Prefer the existing Gmail account/alias signature if its insertion is verified. Connector-created drafts may not receive Gmail UI auto-signatures: if so, insert exactly one validated signature in the draft body and verify readback. Do not append two, and do not copy signatures out of quoted history. When Gmail signature insertion/alias configuration cannot be inspected, treat exact visual fidelity as `SIGNATURE_UI_UNVERIFIED`, use the most recently verified sender-specific signature text, and do not claim the UI will never add another.
3. **Normalize spacing.** Standard Gmail text styling. No stray `>` lines, markdown source syntax, excessive blank lines, broken wrapped lines or repeated salutations/closings. Use exactly one blank line between logical paragraphs, short clear prose, and minimal purposeful formatting. Normal hyperlinks may be preserved; avoid copied markdown link syntax if unsupported in Gmail.
4. **No historical legal/disclaimer footer in newly authored body.** Omit quoted confidentiality statements (including third-party disclaimers) and earlier legal notices from the newly composed body. Do not alter or delete the originating Gmail message. If an explicitly approved NTSN outbound legal footer is mandatory, add only the correct footer once, distinct from copied third-party material.
5. **Sender-specific profiles.** Validate selected From/send-as account before any draft and correct salutation/signature: Ruben A. Meyer for NTSN/NTT-AT, Espen Olsen for Inster/Oesía per latest operator sender rule. **Do not impersonate Espen from an account/connector that cannot select his sender alias.** In such cases, prepare a clearly blocked draft in chat or flag `SENDER_ALIAS_UNVERIFIED` instead of asserting it is ready to send. Gmail is the default draft channel unless an explicit instruction for the specific thread overrides it; the older blanket Inster chat-only exception is superseded.
6. **Post-write readback QA.** Before creation/update: verify original thread, latest reply anchor, recipient(s), CC/BCC, subject, language, attachments, exact sender/alias, active existing draft, known suppression state, and no unsupported commitments. After save: independently read back using Gmail draft listing and where supported draft-message read; verify draft/thread identity, addressing, subject, composed-body content, paragraph formatting, single signature, absence of copied quotation/disclaimer, attachments, no duplicate draft and DRAFT/not SENT state. Mark `DRAFT_VERIFIED` only for actually confirmed fields; mark partial/unverified items explicitly. Do not claim full readback without examining saved body.
7. **Deleted-draft suppression retained.** Apply current 03D exactly: known operator-manually-deleted drafts trigger `OPERATOR_DELETED_SUPPRESS_RECREATE` at **recipient level** until an explicit new instruction authorizes that specific draft. Missing draft alone is *not* evidence of manual deletion. Hygiene maintenance does not override suppression or authorize bulk draft recreation.
8. **Preserve original correspondence.** Never edit, replace, delete, archive or rewrite received/sent historical Gmail messages during draft hygiene operations. Do not strip evidence from originals, disclose third-party legal content, or repurpose confidential email quotations.

## Deterministic Gmail composing sequence

- Preflight: 03D suppression → read full thread/history → current source/fact/disclosure checks → identity/send-as alias validation → existing-draft reconciliation → attachment checks.
- Compose **only new response text** and one validated signature when applicable; no historical quote block. Use short paragraphs and a format-safe MIME body.
- Save exactly one draft in the original thread using native reply anchor; no send or forward.
- Read back independently and reconcile against expected `threadId + draftId`, recipient, CC, subject, new body and signature count; check `DRAFT` label when supported and confirm no `SENT`.
- On failure: record `WRITE_FAILED`, `DRAFT_QA_PARTIAL`, `SENDER_ALIAS_UNVERIFIED` or `SIGNATURE_UI_UNVERIFIED` as applicable. Do not report success for unverified fields or create a fallback unthreaded customer message.

## Reconciliation with prior rules

- 03D manual deletion/recipient-level suppression remains controlling and unchanged.
- 07B hourly full-thread review, draft deduplication, source checks, Level 2A boundary and readback remain controlling. Its “no unnecessary signature block” means no duplicate or redundant hand-added signature, not “never include the authorized outgoing signature”.
- Earlier 03 / 03A Espen chat-only defaults are superseded by newer Gmail-as-default guidance; **sender identity remains Espen for Inster** and must be technically verified before Gmail drafts are treated as send-ready.
- Earlier suggestions to omit signatures in chat-only drafting do not control ready-to-send Gmail draft signature handling.
- No automatic retroactive changes to operator-edited existing drafts; audit/report first. No autonomous send, permission change, file deletion or external commitment authority is introduced.

## QA matrix and release status

| Check | Acceptance |
|---|---|
| Native reply | Draft thread ID equals anchor thread ID |
| New body | No raw quoted previous messages, `>` blocks, prior disclaimer or prior signatures |
| Signature | Exactly one validated sender-specific signature in ready-to-send draft; visual/UI behavior independently tested or qualified |
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

## Live sender/signature audit — 12:50, 11.10.2026

A non-destructive audit of NTSN connected Gmail found a past `SENT` message whose `From` was Espen Olsen (`e.olsen@nanotech-solutions.com`) addressed to Inster/Oesía, but **its body contained both Espen and Ruben outgoing signature blocks**. This is evidence of a **historical two-signature formatting defect**, not proof of the correct approved Espen signature profile or currently configured Gmail send-as alias. Do not copy that entire signature body into new drafts. Current Gmail connector `create_draft`/`update_draft` surfaces do not expose a `From`/send-as selector or Gmail signature-settings read. Therefore classify new Inster draft requests `SENDER_ALIAS_UNVERIFIED` unless separately verifiable by an authorized interface; do not claim ready-to-send and do not send. Signature UI/mobile/desktop auto-insertion remains `SIGNATURE_UI_UNVERIFIED` until operator-verified.

The existing NTT-AT reply draft was audited read-only. It was correctly in-thread, labeled `DRAFT`, had no copied quote history and contained **no signature**. Classify it `EXISTING_DRAFT_SIGNATURE_REVIEW`; never silently rewrite existing customer drafts during global hygiene rollout. If it is explicitly approved for modification, revalidate live thread/source context, append only the correct single sender signature, and read back. No customer draft or historical original correspondence was changed during this audit.

03D suppression remains statically verified only; a destructive simulation of manually deleted drafts is NOT approved and is unnecessary for implementation. UI verification and sender-identity signoff are PENDING_REVIEW, not a failure of approved 03F governance.
