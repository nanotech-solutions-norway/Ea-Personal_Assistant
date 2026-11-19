"""Ea P1 workstream contracts — pure, synthetic, NON-DEPLOYED planning.

No connector/network I/O, storage writes, external action methods or approval grants.
Source authority remains current APPROVED/CANONICAL Ea rules, not this module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from pathlib import PurePath
from typing import Mapping, Sequence

KNOWN_KEYS = frozenset({
    "case_id", "crm_lead_id", "crm_opportunity_id", "order_case_id",
    "gmail_thread_key", "form_response_key", "quote_reference",
    "customer_po_reference", "shipment_id",
})
WORKSTREAM_EVENTS = frozenset({"NEW_LEAD", "INBOUND_REPLY", "RFQ_RECEIVED"})
OPERATOR_CHOICES = frozenset({"VERIFY", "PREPARE", "HOLD"})
PROHIBITED_AUTOMATION = frozenset({
    "SEND_EMAIL", "FORWARD_EMAIL", "SEND_INVITATION", "ISSUE_QUOTE",
    "DISPATCH_PURCHASE_ORDER", "RELEASE_GOODS", "POST_INVOICE",
    "MAKE_PAYMENT", "APPROVE_PRODUCT_CLAIM", "PROMOTE_CANONICAL",
    "DEPLOY_RUNTIME", "SHARE_CONFIDENTIAL", "DELETE_PROVIDER_OBJECT",
})


@dataclass(frozen=True)
class Case:
    case_id: str
    keys: Mapping[str, str]


@dataclass(frozen=True)
class Match:
    status: str
    case_id: str | None
    matched_by: tuple[str, ...] = ()


def correlate_case(evidence_keys: Mapping[str, str], cases: Sequence[Case]) -> Match:
    """Match only exact, verified external IDs. A name/domain is never a join key.

    gmail_thread_key must contain mailbox/account + thread, not thread alone.
    Multiple matching cases, or incompatible strong identifiers, fail closed.
    No match is only a *candidate*, never permission to write a new record.
    """
    supplied = {k: v for k, v in evidence_keys.items()
                if k in KNOWN_KEYS and isinstance(v, str) and v.strip()}
    if not supplied:
        return Match("INSUFFICIENT_IDENTITY", None)
    if "gmail_thread_key" in supplied and ":" not in supplied["gmail_thread_key"]:
        return Match("INVALID_THREAD_KEY", None)
    hits: list[tuple[Case, tuple[str, ...]]] = []
    for case in cases:
        keys = tuple(k for k, v in supplied.items() if case.keys.get(k) == v)
        if case.case_id == supplied.get("case_id") and "case_id" not in keys:
            keys = ("case_id",) + keys
        if keys:
            hits.append((case, keys))
    if len(hits) > 1:
        return Match("AMBIGUOUS_CASE", None)
    if not hits:
        if "case_id" in supplied:
            return Match("UNKNOWN_EXPLICIT_CASE", None)
        return Match("NEW_CANDIDATE_REVIEW", None)
    case, matched = hits[0]
    for k, v in supplied.items():
        old = case.keys.get(k)
        if old and old != v:
            return Match("CONFLICTING_CASE_IDENTIFIERS", None)
    return Match("EXACT_MATCH", case.case_id, matched)


def event_key(mailbox: str, provider_message_id: str, event_type: str,
              case_id: str) -> str:
    """Stable idempotency key; never use mutable email subject or AI similarity."""
    values = (mailbox, provider_message_id, event_type, case_id)
    if not all(isinstance(v, str) and v.strip() for v in values):
        raise ValueError("immutable source identifiers and case ID required")
    wire = "\x1f".join(values)
    return "EA-EV-" + sha256(wire.encode("utf-8")).hexdigest()[:28]


@dataclass(frozen=True)
class Source:
    source_id: str
    variant: str
    scope: str
    revision: str
    approval: str
    fingerprint: str
    recipient_fit: bool = True


def source_gate(variant: str, scope: str, candidates: Sequence[Source]) -> str:
    """Never equate newest file timestamp with APPROVED product truth."""
    exact = [x for x in candidates if x.variant == variant and x.scope == scope]
    if not exact:
        return "SOURCE_MISSING"
    qualified = [x for x in exact if x.approval in {"APPROVED", "CANONICAL"}
                 and x.source_id and x.revision and x.fingerprint
                 and x.recipient_fit]
    if not qualified:
        return "SOURCE_UNAPPROVED_OR_RECIPIENT_MISMATCH"
    # Multiple approved, non-identical versions require current-authority resolution.
    signatures = {(x.revision, x.fingerprint) for x in qualified}
    if len(signatures) != 1:
        return "SOURCE_CONFLICT_PENDING_REVIEW"
    return "SOURCE_READY"


@dataclass(frozen=True)
class Attachment:
    file_id: str
    filename: str
    revision: str
    fingerprint: str
    recipient_fit: bool
    approval: str


def attachment_gate(expected: Sequence[Attachment],
                    observed: Sequence[Attachment]) -> str:
    """Checks evidence of actually attached draft files, not a prose claim."""
    if not expected:
        return "PASS" if not observed else "UNEXPECTED_ATTACHMENT"
    if len(expected) != len(observed):
        return "ATTACHMENT_COUNT_MISMATCH"
    for planned, saved in zip(expected, observed):
        if planned.approval not in {"APPROVED", "CANONICAL", "OPERATOR_AUTHORIZED"}:
            return "ATTACHMENT_UNAPPROVED"
        if not planned.recipient_fit or not saved.recipient_fit:
            return "ATTACHMENT_DISCLOSURE_BLOCK"
        fields = ("file_id", "filename", "revision", "fingerprint")
        if not all(getattr(planned, k) and getattr(saved, k) for k in fields):
            return "ATTACHMENT_EVIDENCE_MISSING"
        if any(getattr(planned, k) != getattr(saved, k) for k in fields):
            return "ATTACHMENT_VERSION_MISMATCH"
    return "PASS"


def quote_reference_gate(reference: str, filename: str, printed_reference: str,
                         email_reference: str) -> str:
    """05D: filename stem, printed reference and draft text agree exactly."""
    if not all([reference, filename, printed_reference, email_reference]):
        return "QUOTE_REFERENCE_MISSING"
    if (PurePath(filename).suffix.lower() != ".pdf"
            or PurePath(filename).stem != reference
            or reference != printed_reference
            or reference != email_reference):
        return "QUOTE_REFERENCE_MISMATCH"
    return "PASS"


def quote_arithmetic_gate(line_totals: Sequence[str], subtotal: str,
                          discount: str, freight: str, tax: str,
                          grand_total: str) -> str:
    """Independent arithmetic reconciliation, not tax/rate authorization."""
    try:
        amounts = [Decimal(str(x)) for x in line_totals]
        vals = [Decimal(str(x)) for x in
                (subtotal, discount, freight, tax, grand_total)]
        if not amounts or any(not n.is_finite() for n in amounts + vals):
            return "QUOTE_ARITHMETIC_INVALID"
        subtotal_d, discount_d, freight_d, tax_d, total_d = vals
        if (any(n < 0 for n in amounts)
                or any(n < 0 for n in (subtotal_d, discount_d, freight_d, tax_d, total_d))
                or discount_d > subtotal_d):
            return "QUOTE_ARITHMETIC_INVALID"
        if abs(sum(amounts) - subtotal_d) > Decimal("0.01"):
            return "QUOTE_SUBTOTAL_MISMATCH"
        if abs(subtotal_d - discount_d + freight_d + tax_d - total_d) > Decimal("0.01"):
            return "QUOTE_TOTAL_MISMATCH"
    except (InvalidOperation, ValueError, TypeError):
        return "QUOTE_ARITHMETIC_INVALID"
    return "PASS"


@dataclass(frozen=True)
class StageInput:
    event_type: str
    case_id: str
    sender_profile: str = "Ruben"
    identity_verified: bool = False
    full_thread_and_sent_checked: bool = False
    source_gate_passed: bool = False
    alias_verified: bool = False
    reply_anchor_verified: bool = False
    suppressed_recipient: bool = False
    explicit_new_draft_instruction: bool = False
    draft_revision_current: bool = False
    customer_disclosure_safe: bool = False
    existing_draft_with_attachments: bool = False
    quote_source_price_verified: bool = False
    quote_reference_qa_passed: bool = False
    quote_arithmetic_qa_passed: bool = False
    attachment_readback_passed: bool = False
    quote_layout_qa_passed: bool = False
    policies_conflict: bool = False


@dataclass(frozen=True)
class Plan:
    disposition: str
    actions: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    operator_gate: str = "EXTERNAL_ACTIONS_REQUIRE_NEW_APPROVAL"


def internal_plan(value: StageInput) -> Plan:
    """Plan internal work; this function cannot execute anything externally."""
    if value.event_type not in WORKSTREAM_EVENTS:
        return Plan("HOLD", blockers=("UNKNOWN_TRIGGER",))
    if not value.case_id:
        return Plan("HOLD", blockers=("CASE_ID_REQUIRED",))
    if value.sender_profile == "Espen Olsen":
        return Plan("CHAT_ONLY_OUTLOOK", actions=("PREPARE_CHAT_COPY_ONLY",))
    if value.suppressed_recipient and not value.explicit_new_draft_instruction:
        return Plan("SUPPRESSED_03D", blockers=("OPERATOR_DELETED_RECIPIENT_DRAFT",))
    prerequisites = (
        ("AUTHORITY_CONFLICT", value.policies_conflict),
        ("IDENTITY_UNVERIFIED", not value.identity_verified),
        ("HISTORICAL_SENT_OR_THREAD_MISSING", not value.full_thread_and_sent_checked),
        ("SOURCE_UNVERIFIED", not value.source_gate_passed),
        ("SENDER_ALIAS_UNVERIFIED", not value.alias_verified),
        ("THREAD_ANCHOR_UNVERIFIED", not value.reply_anchor_verified),
        ("STALE_DRAFT_OR_THREAD", not value.draft_revision_current),
        ("CUSTOMER_DISCLOSURE_UNVERIFIED", not value.customer_disclosure_safe),
    )
    blockers = tuple(key for key, failed in prerequisites if failed)
    if value.existing_draft_with_attachments:
        blockers += ("EXISTING_ATTACHMENT_DRAFT_REPLACEMENT_REQUIRES_RECONCILIATION",)
    if value.event_type == "RFQ_RECEIVED":
        blockers += tuple(k for k, fail in (
            ("PRICE_SOURCE_UNVERIFIED", not value.quote_source_price_verified),
            ("QUOTE_REFERENCE_FAILED", not value.quote_reference_qa_passed),
            ("QUOTE_ARITHMETIC_FAILED", not value.quote_arithmetic_qa_passed),
            ("QUOTE_LAYOUT_UNVERIFIED", not value.quote_layout_qa_passed),
            ("ATTACHMENT_READBACK_UNVERIFIED", not value.attachment_readback_passed),
        ) if fail)
    if blockers:
        return Plan("BLOCKED_INTERNAL_PREPARATION", blockers=blockers)
    shared = ("PREPARE_IN_THREAD_UNSENT_DRAFT", "VERIFY_GMAIL_DRAFT",
              "PROPOSE_CRM_ACTIVITY_PROJECTION")
    if value.event_type == "RFQ_RECEIVED":
        return Plan("INTERNAL_PLAN_READY", actions=(
            "PREPARE_INTERNAL_QUOTE", "VERIFY_QUOTE_REFERENCE_AND_ARITHMETIC",
            "RENDER_AND_VERIFY_QUOTE_PDF", "RECONCILE_ACTUAL_DRAFT_ATTACHMENT",
        ) + shared + ("PROPOSE_ORDER_BOOK_DOCUMENT_INDEX_PROJECTION",))
    return Plan("INTERNAL_PLAN_READY", actions=shared)


def allowed_operator_choices(selection: Mapping[str, tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    """Optional per-work-ID notes are not executable instructions or approval."""
    result = []
    for work_id, (choice, _note) in selection.items():
        if not work_id.strip() or choice not in OPERATOR_CHOICES:
            raise ValueError("unknown work ID/choice")
        if choice != "HOLD":
            result.append((work_id, choice))
    return tuple(result)


def projection_preflight(owner: str, expected_owner: str,
                         source_readback_verified: bool,
                         target_before_verified: bool,
                         idempotency_exists: bool,
                         ledger_write_ahead_verified: bool) -> str:
    """No provider write here; returns the exact prerequisite disposition."""
    if owner != expected_owner:
        return "FIELD_OWNERSHIP_CONFLICT"
    if not source_readback_verified or not target_before_verified:
        return "SOURCE_OR_TARGET_NOT_VERIFIED"
    if idempotency_exists:
        return "NO_OP_ALREADY_RECORDED"
    if not ledger_write_ahead_verified:
        return "LOGGING_NOT_VERIFIED"
    return "PREPARE_WRITE_UNDER_EXISTING_APPROVED_SCOPE"
