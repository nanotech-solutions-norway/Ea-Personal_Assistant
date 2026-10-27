"""Synthetic-only tests for Ea vNext proposed policy fixture."""
import unittest
from synthetic_policy_guard import Fixture, evaluate

class PolicyFixtureTests(unittest.TestCase):
    def test_unknown_denied(self):
        self.assertEqual(evaluate(Fixture("unrecognized")), "DENY_UNKNOWN_ACTION")

    def test_all_external_actions_denied(self):
        from synthetic_policy_guard import EXTERNAL_ACTIONS
        for action in EXTERNAL_ACTIONS:
            with self.subTest(action=action):
                self.assertEqual(evaluate(Fixture(action)), "DENY_EXTERNAL_OR_HOLD")

    def test_espen_chat_only(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", sender="Espen Olsen")), "CHAT_ONLY_OUTLOOK_MANUAL")

    def test_recipient_level_deleted_draft_suppressed(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", known_recipient_draft_deletion=True)), "SUPPRESS_03D")

    def test_explicit_specific_request_lifts_suppression_only_for_evaluated_draft(self):
        f = Fixture("gmail_reply_draft", known_recipient_draft_deletion=True,
                    explicit_new_draft_instruction=True, alias_verified=True, thread_anchor_verified=True)
        self.assertEqual(evaluate(f), "ALLOW_PRIVATE_UNSENT_DRAFT")

    def test_unverified_sender_denied(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", thread_anchor_verified=True)), "BLOCK_SENDER_ALIAS")

    def test_missing_thread_anchor_denied(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", alias_verified=True)), "BLOCK_THREAD_ANCHOR")

    def test_stale_revision_blocks(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", source_revision_current=False)), "BLOCK_STALE_SOURCE")

    def test_existing_draft_reconciled_not_recreated(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", existing_draft_for_action=True)), "RECONCILE_EXISTING_DRAFT")

    def test_signature_insertion_blocked(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", alias_verified=True,
                    thread_anchor_verified=True, manually_inserted_signature=True)), "BLOCK_SIGNATURE")

    def test_unverified_factual_dependency_blocks(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", alias_verified=True,
                    thread_anchor_verified=True, factual_dependencies_verified=False)), "BLOCK_FACTUAL_DEPENDENCY")

    def test_private_draft_success_only_for_complete_fixture(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft", alias_verified=True,
                    thread_anchor_verified=True)), "ALLOW_PRIVATE_UNSENT_DRAFT")

    def test_internal_followup_reminder_free(self):
        self.assertEqual(evaluate(Fixture("calendar_private_followup")), "ALLOW_PRIVATE_NO_REMINDERS")

    def test_internal_popup_conflict_is_not_auto_promoted(self):
        self.assertEqual(evaluate(Fixture("calendar_private_followup",
                    reminder_popup_or_email=True)), "PENDING_REVIEW")

    def test_no_external_attendee_in_followup(self):
        self.assertEqual(evaluate(Fixture("calendar_private_followup",
                    external_attendees=True)), "DENY_EXTERNAL_OR_HOLD")

    def test_existing_followup_reconciled(self):
        self.assertEqual(evaluate(Fixture("calendar_private_followup",
                    existing_draft_for_action=True)), "RECONCILE_EXISTING_EVENT")

    def test_unresolved_policy_conflict_holds_new_draft(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft",
                    unresolved_policy_conflict=True)), "PENDING_REVIEW")

    def test_readonly_allowed(self):
        self.assertEqual(evaluate(Fixture("read_only_reconciliation")), "ALLOW_READ_ONLY")

    def test_espen_rule_precedes_recipient_draft_suppression(self):
        self.assertEqual(evaluate(Fixture("gmail_reply_draft",
                    sender="Espen Olsen", known_recipient_draft_deletion=True)), "CHAT_ONLY_OUTLOOK_MANUAL")

if __name__ == "__main__":
    unittest.main(verbosity=2)
