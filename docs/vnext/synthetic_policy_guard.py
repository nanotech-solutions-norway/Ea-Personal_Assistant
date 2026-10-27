"""EA vNext M3 synthetic policy fixture — NOT PRODUCTION AUTHORIZATION.
No network, credential, mailbox, calendar, CRM, or storage operations.
Based solely on currently approved controls, not a new governing rule.
"""
from dataclasses import dataclass

EXTERNAL_ACTIONS = frozenset({
    "send", "forward", "external_invitation", "purchase", "file_share",
    "permissions_change", "production_cutover", "azure_deploy",
    "promote_canonical", "delete_provider_object",
})

@dataclass(frozen=True)
class Fixture:
    action: str
    sender: str = "Ruben"
    explicit_new_draft_instruction: bool = False
    known_recipient_draft_deletion: bool = False
    alias_verified: bool = False
    thread_anchor_verified: bool = False
    source_revision_current: bool = True
    existing_draft_for_action: bool = False
    manually_inserted_signature: bool = False
    external_attendees: bool = False
    reminder_popup_or_email: bool = False
    unresolved_policy_conflict: bool = False
    factual_dependencies_verified: bool = True

def evaluate(f: Fixture) -> str:
    """Deterministic synthetic disposition. All unknown actions are denied."""
    if f.action in EXTERNAL_ACTIONS:
        return "DENY_EXTERNAL_OR_HOLD"
    if f.action == "gmail_reply_draft":
        if f.sender == "Espen Olsen":
            return "CHAT_ONLY_OUTLOOK_MANUAL"
        if f.known_recipient_draft_deletion and not f.explicit_new_draft_instruction:
            return "SUPPRESS_03D"
        if f.unresolved_policy_conflict:
            return "PENDING_REVIEW"
        if not f.source_revision_current:
            return "BLOCK_STALE_SOURCE"
        if f.existing_draft_for_action:
            return "RECONCILE_EXISTING_DRAFT"
        if not f.alias_verified:
            return "BLOCK_SENDER_ALIAS"
        if not f.thread_anchor_verified:
            return "BLOCK_THREAD_ANCHOR"
        if f.manually_inserted_signature:
            return "BLOCK_SIGNATURE"
        if not f.factual_dependencies_verified:
            return "BLOCK_FACTUAL_DEPENDENCY"
        return "ALLOW_PRIVATE_UNSENT_DRAFT"
    if f.action == "calendar_private_followup":
        if f.external_attendees:
            return "DENY_EXTERNAL_OR_HOLD"
        if f.unresolved_policy_conflict or f.reminder_popup_or_email:
            return "PENDING_REVIEW"
        if not f.source_revision_current:
            return "BLOCK_STALE_SOURCE"
        if f.existing_draft_for_action:
            return "RECONCILE_EXISTING_EVENT"
        return "ALLOW_PRIVATE_NO_REMINDERS"
    if f.action == "read_only_reconciliation":
        return "ALLOW_READ_ONLY"
    return "DENY_UNKNOWN_ACTION"
