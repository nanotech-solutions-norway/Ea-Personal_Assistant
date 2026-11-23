"""Ea P2 read-only case reconciliation — deterministic synthetic adapter.

No external clients, credentials, network, provider actions, scheduler, persistence,
email body storage, price data, or permission escalation. A returned finding is
not a permit to update a business record. See APPROVED/CANONICAL owning rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

EXPECTED_COVERAGE = frozenset({"BOUNDED_PARTIAL", "BOUNDED_COMPLETE", "UNKNOWN"})
NEXT_ACTORS = frozenset({"NTSN", "EXTERNAL", "INTERNAL_REVIEW", "UNKNOWN"})
FINDING_CODES = frozenset({
    "MISSING_TYPED_CASE_CROSSWALK", "CONFLICTING_CASE_CROSSWALK",
    "SENT_AFTER_LATEST_INBOUND", "CRM_DRAFT_STATE_STALE",
    "CRM_ACTION_OWNER_STALE", "ORDER_ACTION_OWNER_STALE",
    "CRM_SOURCE_POINTER_STALE", "ORDER_SOURCE_POINTER_STALE",
    "LATEST_QUOTE_NOT_DOCUMENT_INDEXED", "PRESERVE_OLDER_QUOTE_VERSION",
    "QUOTE_ATTACHMENT_METADATA_ONLY", "SENT_QUOTE_REFERENCE_UNVERIFIED",
    "NO_GMAIL_SENT_EVIDENCE", "SOURCE_TIME_UNVERIFIED",
    "SOURCE_ACCOUNT_KEY_UNVERIFIED", "SOURCE_COVERAGE_PARTIAL",
    "GMAIL_THREAD_INCOMPLETE", "NEWER_INBOUND_REQUIRES_REVIEW",
})


@dataclass(frozen=True)
class Message:
    """Normalized *metadata only* from a verified mailbox read."""
    account_key: str
    thread_id: str
    message_id: str
    direction: str
    observed_at_utc: str
    attachment_filenames: tuple[str, ...] = ()
    attachment_contents_verified: bool = False
    quote_reference_verified: str = ""


@dataclass(frozen=True)
class CaseState:
    """One existing case; CRM and Order Book not treated as competing owners."""
    pilot_id: str  # synthetic pseudonym; never real legal entity
    crm_key: str
    order_key: str
    order_record_crm_link: str = ""
    crm_next_actor: str = "UNKNOWN"
    order_next_actor: str = "UNKNOWN"
    crm_claims_unsent_draft: bool = False
    crm_last_source_message: str = ""
    order_last_source_message: str = ""
    order_quote_ref: str = ""
    document_index_quote_refs: tuple[str, ...] = ()
    sent: tuple[Message, ...] = ()
    inbound: tuple[Message, ...] = ()
    source_coverage: str = "UNKNOWN"
    full_customer_thread_checked: bool = False


@dataclass(frozen=True)
class Finding:
    code: str
    owner: str
    effect: str
    evidence_kind: str


@dataclass(frozen=True)
class Disposition:
    pilot_id: str
    status: str
    findings: tuple[Finding, ...]
    next_actor: str
    business_writes: tuple[str, ...] = ()
    external_actions: tuple[str, ...] = ()
    logging_state: str = "NO_BUSINESS_WRITES_TO_LOG"


def _parse_aware(value: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError, AttributeError):
        return None
    return dt.astimezone(timezone.utc) if dt.tzinfo else None


def _latest(messages: Sequence[Message]) -> Message | None:
    candidates = [m for m in messages if _parse_aware(m.observed_at_utc)]
    return max(candidates, key=lambda x: _parse_aware(x.observed_at_utc)) if candidates else None


def reconcile_read_only(state: CaseState) -> Disposition:
    """Return non-executing findings. All source IDs must have prior provider readback."""
    if not state.pilot_id or not state.crm_key or not state.order_key:
        return Disposition(state.pilot_id, "SOURCE_IDENTITY_UNVERIFIED",
                           (Finding("SOURCE_ACCOUNT_KEY_UNVERIFIED", "SOURCE", "HOLD",
                                    "case source keys"),), "INTERNAL_REVIEW")
    if state.source_coverage not in EXPECTED_COVERAGE:
        return Disposition(state.pilot_id, "SOURCE_IDENTITY_UNVERIFIED",
                           (Finding("SOURCE_COVERAGE_PARTIAL", "SOURCE", "HOLD",
                                    "unexpected coverage claim"),), "INTERNAL_REVIEW")
    if (state.crm_next_actor not in NEXT_ACTORS
            or state.order_next_actor not in NEXT_ACTORS):
        return Disposition(state.pilot_id, "SOURCE_IDENTITY_UNVERIFIED",
                           (Finding("SOURCE_ACCOUNT_KEY_UNVERIFIED", "SOURCE", "HOLD",
                                    "unrecognized actor"),), "INTERNAL_REVIEW")

    findings: list[Finding] = []

    def add(code: str, owner: str, evidence_kind: str, effect="REVIEW_ONLY") -> None:
        if code not in FINDING_CODES:
            raise ValueError("finding not allowed")
        if code not in {x.code for x in findings}:
            findings.append(Finding(code, owner, effect, evidence_kind))

    if not state.order_record_crm_link:
        add("MISSING_TYPED_CASE_CROSSWALK", "CRM_AND_ORDER", "native register keys")
    elif state.order_record_crm_link != state.crm_key:
        add("CONFLICTING_CASE_CROSSWALK", "CRM_AND_ORDER", "native register keys", "HOLD")

    all_messages = (*state.sent, *state.inbound)
    if any(not m.account_key or not m.thread_id or not m.message_id for m in all_messages):
        add("SOURCE_ACCOUNT_KEY_UNVERIFIED", "GMAIL", "native account/thread/message ID", "HOLD")
    if (not all_messages or any(_parse_aware(m.observed_at_utc) is None
                                for m in all_messages)):
        add("SOURCE_TIME_UNVERIFIED", "GMAIL", "message timestamp", "HOLD")
    if any(m.direction != "SENT" for m in state.sent) or any(
            m.direction != "INBOUND" for m in state.inbound):
        add("SOURCE_ACCOUNT_KEY_UNVERIFIED", "GMAIL", "Gmail label direction", "HOLD")

    most_recent_sent = _latest(state.sent)
    most_recent_inbound = _latest(state.inbound)
    if not most_recent_sent:
        add("NO_GMAIL_SENT_EVIDENCE", "GMAIL", "SENT query")
    if (most_recent_sent and most_recent_inbound
            and _parse_aware(most_recent_sent.observed_at_utc)
            > _parse_aware(most_recent_inbound.observed_at_utc)):
        if (state.crm_claims_unsent_draft or state.crm_next_actor == "NTSN"
                or state.order_next_actor == "NTSN"):
            add("SENT_AFTER_LATEST_INBOUND", "GMAIL", "source timestamp ordering")
        if state.crm_claims_unsent_draft:
            add("CRM_DRAFT_STATE_STALE", "CRM", "CRM action vs Gmail SENT")
        if state.crm_next_actor == "NTSN":
            add("CRM_ACTION_OWNER_STALE", "CRM", "CRM next action vs Gmail SENT")
        if state.order_next_actor == "NTSN":
            add("ORDER_ACTION_OWNER_STALE", "ORDER_BOOK", "Order Book vs Gmail SENT")
    elif (most_recent_sent and most_recent_inbound
          and _parse_aware(most_recent_inbound.observed_at_utc)
          > _parse_aware(most_recent_sent.observed_at_utc)):
        add("NEWER_INBOUND_REQUIRES_REVIEW", "GMAIL", "source timestamp ordering")

    if most_recent_sent and state.crm_last_source_message and (
            state.crm_last_source_message != most_recent_sent.message_id):
        add("CRM_SOURCE_POINTER_STALE", "CRM", "CRM last-source vs latest Gmail SENT")
    if most_recent_sent and state.order_last_source_message and (
            state.order_last_source_message != most_recent_sent.message_id):
        add("ORDER_SOURCE_POINTER_STALE", "ORDER_BOOK",
            "Order Book last-source vs latest Gmail SENT")

    # A changed quotation is a new immutable document version, not an overwrite.
    if most_recent_sent and most_recent_sent.quote_reference_verified:
        ref = most_recent_sent.quote_reference_verified
        if ref not in state.document_index_quote_refs:
            add("LATEST_QUOTE_NOT_DOCUMENT_INDEXED", "ORDER_BOOK", "Document_Index refs")
        if state.order_quote_ref and state.order_quote_ref != ref:
            add("PRESERVE_OLDER_QUOTE_VERSION", "ORDER_BOOK", "distinct issued document refs")
        if most_recent_sent.attachment_filenames and not most_recent_sent.attachment_contents_verified:
            add("QUOTE_ATTACHMENT_METADATA_ONLY", "DOCUMENT_QA",
                "Gmail attachment metadata not independently opened")
    elif most_recent_sent and most_recent_sent.attachment_filenames:
        add("SENT_QUOTE_REFERENCE_UNVERIFIED", "DOCUMENT_QA",
            "attached file without verified quote identity")

    if not state.full_customer_thread_checked:
        add("GMAIL_THREAD_INCOMPLETE", "GMAIL", "bounded thread history")
    if state.source_coverage != "BOUNDED_COMPLETE":
        add("SOURCE_COVERAGE_PARTIAL", "SOURCE", "declared bounded source window")

    if not findings:
        return Disposition(state.pilot_id, "READ_ONLY_NO_DISCREPANCY",
                           (), "UNKNOWN")
    # All findings are corrective suggestions. No A1 writes and no A2 sends.
    blocking = any(x.effect == "HOLD" for x in findings)
    return Disposition(
        state.pilot_id, "BLOCKED_SOURCE_IDENTITY" if blocking else "RECONCILIATION_PROPOSED",
        tuple(findings), "INTERNAL_REVIEW",
    )


def summarize_codes(result: Disposition) -> tuple[str, ...]:
    """Safe view for redacted audit: only enum codes, no provider payloads."""
    return tuple(x.code for x in result.findings)
