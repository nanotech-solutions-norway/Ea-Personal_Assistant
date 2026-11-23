"""Synthetic-only Ea Email Watch gates: NO provider I/O, credentials or deployment.

APPROVED/CANONICAL 07B/03A-D/03F/03I are the authority, not this module.
All inputs must be supplied from current, independently verified provider reads.
"""
from __future__ import annotations

from dataclasses import dataclass
from email.utils import parseaddr
from typing import Mapping, Sequence


def _field(value: Mapping[str, object], *names: str) -> object | None:
    """Support connector spelling variations without crashing on missing fields."""
    for name in names:
        candidate = value.get(name)
        if candidate is not None:
            return candidate
    return None


def _address(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return parseaddr(value)[1].strip().casefold()


def _addresses(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, (tuple, list)):
        return ()
    return tuple(x for x in (_address(v) for v in value) if x)


def draft_sender(summary: Mapping[str, object]) -> str:
    """Gmail wrappers can expose 'from' or 'from_'; absence is UNKNOWN."""
    return _address(_field(summary, "from", "from_"))


def inventory_state(*, call_completed: bool,
                    items: Sequence[Mapping[str, object]] | None) -> str:
    """A connector exception or missing result is never reported as zero drafts."""
    if not call_completed or items is None:
        return "DRAFT_INVENTORY_NOT_VERIFIED"
    return "DRAFT_INVENTORY_VERIFIED"


@dataclass(frozen=True)
class Candidate:
    case_key: str  # Stable, independently verified case/thread key
    severity: int  # Verified 0..3; 3 = immediate high-severity issue
    overdue: bool
    overdue_days: int
    inbound_action: bool


def choose_cases(candidates: Sequence[Candidate], limit: int = 5) -> tuple[Candidate, ...]:
    """Bounded, deterministic work queue; do not treat unselected items as reviewed."""
    if limit < 1 or limit > 5:
        raise ValueError("case limit must be 1..5")
    unique: dict[str, Candidate] = {}
    for c in candidates:
        if not c.case_key or c.severity not in range(4) or c.overdue_days < 0:
            raise ValueError("verified key, severity and nonnegative overdue age required")
        old = unique.get(c.case_key)
        if old is None or (c.severity, c.inbound_action, c.overdue_days) > (
                old.severity, old.inbound_action, old.overdue_days):
            unique[c.case_key] = c
    ranked = sorted(unique.values(), key=lambda c: (
        -c.severity, -int(c.inbound_action), -c.overdue_days, c.case_key))
    urgent = [c for c in ranked if c.severity == 3]
    chosen = urgent[:limit]
    # Preserve two oldest overdue cases when there is room after urgent clients.
    overdue = sorted((c for c in ranked if c.overdue and c not in chosen),
                     key=lambda c: (-c.overdue_days, c.case_key))
    for c in overdue[:max(0, min(2, limit - len(chosen)))]:
        chosen.append(c)
    for c in ranked:
        if len(chosen) == limit:
            break
        if c not in chosen:
            chosen.append(c)
    return tuple(chosen)


@dataclass(frozen=True)
class Preflight:
    operator_deleted_recipient: bool
    explicit_recipient_override: bool
    sender_is_espen: bool
    thread_complete: bool
    sent_checked: bool
    latest_sent_after_inbound: bool
    reply_required: bool
    reply_anchor_verified: bool
    actual_reply_to_verified: bool
    correct_account_verified: bool
    selected_from_alias_verified: bool
    existing_draft_checked: bool
    facts_verified: bool
    approval_required: bool


def preflight_disposition(p: Preflight) -> str:
    """Observation/permission gate only. Never claims a draft was written."""
    if p.operator_deleted_recipient and not p.explicit_recipient_override:
        return "OPERATOR_DELETED_SUPPRESS_RECREATE"
    if p.sender_is_espen:
        return "PENDING_OPERATOR_CHAT_DRAFT"
    if not p.thread_complete or not p.sent_checked or not p.existing_draft_checked:
        return "PENDING_COVERAGE"
    if p.latest_sent_after_inbound:
        return "ALREADY_SENT"
    if not p.reply_required:
        return "WAITING_EXTERNAL"
    if not p.facts_verified:
        return "BLOCKED_FACTUAL_DEPENDENCY"
    if p.approval_required:
        return "PENDING_APPROVAL"
    if not p.correct_account_verified or not p.selected_from_alias_verified:
        return "SENDER_ALIAS_UNVERIFIED"
    if not p.reply_anchor_verified or not p.actual_reply_to_verified:
        return "PENDING_COVERAGE"
    return "READY_TO_ATTEMPT_INTERNAL_UNSENT_DRAFT"


@dataclass(frozen=True)
class DraftExpected:
    draft_id: str
    thread_id: str
    sender: str
    to: tuple[str, ...]
    cc: tuple[str, ...]
    subject: str
    response_body: str
    attachment_filenames: tuple[str, ...] = ()


def draft_readback(expected: DraftExpected,
                   listed: Sequence[Mapping[str, object]] | None,
                   stored: Mapping[str, object] | None,
                   *, body_hygiene_verified: bool) -> str:
    """Only independent provider readback can certify a saved draft."""
    if listed is None or stored is None:
        return "DRAFT_QA_FAILED"
    matched = [x for x in listed if x.get("draft_id") == expected.draft_id]
    if len(matched) != 1:
        return "DRAFT_QA_FAILED"
    entry = matched[0]
    fields = (
        entry.get("thread_id") == expected.thread_id,
        stored.get("thread_id") == expected.thread_id,
        stored.get("id") == entry.get("message_id"),
        "DRAFT" in (stored.get("labels") or ()),
        "DRAFT" in (entry.get("labels") or ()),
        draft_sender(entry) == _address(expected.sender),
        _address(_field(stored, "from", "from_")) == _address(expected.sender),
        _addresses(stored.get("to")) == _addresses(expected.to),
        _addresses(stored.get("cc")) == _addresses(expected.cc),
        stored.get("subject") == expected.subject,
        stored.get("body") == expected.response_body,
        body_hygiene_verified,
    )
    if not all(fields):
        return "DRAFT_QA_FAILED"
    attached = tuple(x.get("filename") for x in stored.get("attachments", ()) or ())
    if attached != expected.attachment_filenames:
        return "DRAFT_QA_FAILED"
    if len([x for x in listed if x.get("thread_id") == expected.thread_id]) != 1:
        return "DRAFT_QA_FAILED"
    return "DRAFT_VERIFIED"


def private_followup_state(event: Mapping[str, object] | None) -> str:
    """Check one existing Calendar event without authorizing any mutation."""
    if event is None:
        return "CALENDAR_NOT_VERIFIED"
    if event.get("status") == "cancelled":
        return "CALENDAR_EVENT_CANCELLED"
    reminders = event.get("reminders")
    if not isinstance(reminders, Mapping):
        return "FOLLOWUP_REMINDERS_NOT_VERIFIED"
    if reminders.get("use_default") is not False or (reminders.get("overrides") or []) != []:
        return "FOLLOWUP_REMINDER_POLICY_MISMATCH"
    if event.get("visibility") != "private" or event.get("attendees"):
        return "FOLLOWUP_PRIVACY_POLICY_MISMATCH"
    if event.get("hangout_link"):
        return "FOLLOWUP_PRIVACY_POLICY_MISMATCH"
    return "FOLLOWUP_REMINDERS_OFF_BY_POLICY"

@dataclass(frozen=True)
class OneTimeDraftAuthorization:
    """Explicit operator evidence for exactly one already identified reply.

    Approval is an external assertion supplied by the operator workflow, not
    inferred from a send-as selector, existing drafts, or another case.
    This record is not persistent runtime authority or reusable authorization.
    """
    case_key: str
    account: str
    original_message_id: str
    intended_sender: str
    explicit_operator_approval: bool
    already_consumed: bool = False


def one_time_draft_gate(authorization: OneTimeDraftAuthorization | None,
                        *, case_key: str, account: str,
                        original_message_id: str, intended_sender: str,
                        suppression_clear: bool, espens_outlook_only: bool,
                        complete_preflight: bool) -> str:
    """Manual exception only: still require independent post-write Gmail QA.

    NEVER treat this result as DRAFT_VERIFIED or permission to send.
    Ordinary unattended preflight_disposition keeps the alias gate unchanged.
    """
    if not suppression_clear:
        return "OPERATOR_DELETED_SUPPRESS_RECREATE"
    if espens_outlook_only:
        return "PENDING_OPERATOR_CHAT_DRAFT"
    if not complete_preflight:
        return "PENDING_COVERAGE"
    if (authorization is None or not authorization.explicit_operator_approval
            or authorization.already_consumed):
        return "SENDER_ALIAS_UNVERIFIED"
    if not all((case_key, account, original_message_id, intended_sender)):
        return "SENDER_ALIAS_UNVERIFIED"
    if (authorization.case_key != case_key
            or authorization.account.casefold() != account.casefold()
            or authorization.original_message_id != original_message_id
            or _address(authorization.intended_sender) != _address(intended_sender)):
        return "SENDER_ALIAS_UNVERIFIED"
    return "ONE_TIME_DRAFT_WRITE_ALLOWED_QA_REQUIRED"


def same_draft_cleanup_status(*, original_draft_id: str,
                              updated_draft_id: str,
                              original_thread_id: str,
                              updated_thread_id: str,
                              stored_body: str | None,
                              expected_clean_body: str,
                              current_message_read: bool) -> str:
    """Model provider's automatic reply quotation; no unthreaded fallback."""
    if (not original_draft_id or original_draft_id != updated_draft_id
            or not original_thread_id or original_thread_id != updated_thread_id
            or not current_message_read or stored_body is None):
        return "DRAFT_QA_FAILED"
    if stored_body != expected_clean_body:
        return "DRAFT_QA_FAILED"
    return "SAME_DRAFT_CLEAN_BODY_VERIFIED"
