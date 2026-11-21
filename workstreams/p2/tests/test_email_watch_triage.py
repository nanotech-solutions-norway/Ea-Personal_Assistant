"""Synthetic, nonconfidential regression tests; never call live providers."""
import unittest
from dataclasses import replace

from workstreams.p2.email_watch_triage import (
    Candidate, DraftExpected, Preflight, choose_cases, draft_readback,
    draft_sender, inventory_state, preflight_disposition, private_followup_state,
)


def base_preflight():
    return Preflight(
        operator_deleted_recipient=False, explicit_recipient_override=False,
        sender_is_espen=False, thread_complete=True, sent_checked=True,
        latest_sent_after_inbound=False, reply_required=True,
        reply_anchor_verified=True, actual_reply_to_verified=True,
        correct_account_verified=True, selected_from_alias_verified=True,
        existing_draft_checked=True, facts_verified=True,
        approval_required=False,
    )


def expected():
    return DraftExpected("draft-A", "thread-A", "r@example.test",
                         ("client@example.test",), ("cc@example.test",),
                         "Re: Test", "Clean reply only")


def provider():
    entry = {
        "draft_id": "draft-A", "thread_id": "thread-A", "message_id": "msg-2",
        "from_": "r@example.test", "labels": ["DRAFT"],
    }
    stored = {
        "id": "msg-2", "thread_id": "thread-A", "from": "r@example.test",
        "to": ["client@example.test"], "cc": ["cc@example.test"],
        "subject": "Re: Test", "body": "Clean reply only",
        "labels": ["DRAFT"], "attachments": [],
    }
    return [entry], stored


class EmailWatchTriageTests(unittest.TestCase):
    def test_sender_alias_key_variants_are_null_safe(self):
        self.assertEqual(draft_sender({"from_": "R <R@EXAMPLE.TEST>"}), "r@example.test")
        self.assertEqual(draft_sender({"from": "r@example.test"}), "r@example.test")
        self.assertEqual(draft_sender({}), "")
        self.assertEqual(draft_sender({"from_": None}), "")

    def test_provider_error_cannot_be_reported_as_zero_drafts(self):
        self.assertEqual(inventory_state(call_completed=False, items=[]),
                         "DRAFT_INVENTORY_NOT_VERIFIED")
        self.assertEqual(inventory_state(call_completed=True, items=None),
                         "DRAFT_INVENTORY_NOT_VERIFIED")
        self.assertEqual(inventory_state(call_completed=True, items=[]),
                         "DRAFT_INVENTORY_VERIFIED")

    def test_selects_two_oldest_overdue_when_room(self):
        cases = [
            Candidate("oldest", 1, True, 30, False),
            Candidate("second", 1, True, 25, False),
            Candidate("third", 1, True, 15, False),
            Candidate("fresh", 2, False, 0, True),
        ]
        selected = choose_cases(cases, limit=3)
        self.assertEqual({c.case_key for c in selected}, {"oldest", "second", "fresh"})

    def test_high_severity_displaces_backlog(self):
        cases = [Candidate("old", 0, True, 50, False)]
        cases.extend(Candidate(f"urgent-{i}", 3, False, 0, True)
                     for i in range(5))
        selected = choose_cases(cases)
        self.assertEqual(len(selected), 5)
        self.assertNotIn("old", [x.case_key for x in selected])

    def test_stable_case_identity_is_deduplicated(self):
        selected = choose_cases([
            Candidate("same", 0, True, 1, False),
            Candidate("same", 2, True, 4, True),
        ])
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].severity, 2)

    def test_invalid_case_key_blocks(self):
        with self.assertRaises(ValueError):
            choose_cases([Candidate("", 1, False, 0, False)])

    def test_suppressed_recipient_overrides_every_other_gate(self):
        p = replace(base_preflight(), operator_deleted_recipient=True,
                    thread_complete=False)
        self.assertEqual(preflight_disposition(p),
                         "OPERATOR_DELETED_SUPPRESS_RECREATE")

    def test_outlook_author_never_enters_gmail_gate(self):
        self.assertEqual(preflight_disposition(
            replace(base_preflight(), sender_is_espen=True)),
            "PENDING_OPERATOR_CHAT_DRAFT")

    def test_inventory_only_is_not_thread_preflight(self):
        p = replace(base_preflight(), thread_complete=False)
        self.assertEqual(preflight_disposition(p), "PENDING_COVERAGE")

    def test_existing_draft_must_be_inspected(self):
        p = replace(base_preflight(), existing_draft_checked=False)
        self.assertEqual(preflight_disposition(p), "PENDING_COVERAGE")

    def test_sent_after_inbound_prevents_duplicate(self):
        p = replace(base_preflight(), latest_sent_after_inbound=True)
        self.assertEqual(preflight_disposition(p), "ALREADY_SENT")

    def test_sender_selector_missing_blocks_new_gmail_draft(self):
        p = replace(base_preflight(), selected_from_alias_verified=False)
        self.assertEqual(preflight_disposition(p), "SENDER_ALIAS_UNVERIFIED")

    def test_unverified_commercial_truth_blocks(self):
        p = replace(base_preflight(), facts_verified=False)
        self.assertEqual(preflight_disposition(p), "BLOCKED_FACTUAL_DEPENDENCY")

    def test_verified_provider_readback_is_required(self):
        self.assertEqual(preflight_disposition(base_preflight()),
                         "READY_TO_ATTEMPT_INTERNAL_UNSENT_DRAFT")
        self.assertEqual(draft_readback(expected(), None, None,
                                        body_hygiene_verified=True),
                         "DRAFT_QA_FAILED")

    def test_exact_draft_current_message_and_body_pass(self):
        items, stored = provider()
        self.assertEqual(draft_readback(expected(), items, stored,
                                        body_hygiene_verified=True),
                         "DRAFT_VERIFIED")

    def test_wrong_sender_and_unsafe_body_fail(self):
        items, stored = provider()
        items[0]["from_"] = "wrong@example.test"
        self.assertEqual(draft_readback(expected(), items, stored,
                                        body_hygiene_verified=True),
                         "DRAFT_QA_FAILED")
        items, stored = provider()
        self.assertEqual(draft_readback(expected(), items, stored,
                                        body_hygiene_verified=False),
                         "DRAFT_QA_FAILED")

    def test_changed_message_id_and_duplicate_draft_fail(self):
        items, stored = provider()
        stored["id"] = "stale-msg-1"
        self.assertEqual(draft_readback(expected(), items, stored,
                                        body_hygiene_verified=True),
                         "DRAFT_QA_FAILED")
        items, stored = provider()
        items.append({**items[0], "draft_id": "draft-B"})
        self.assertEqual(draft_readback(expected(), items, stored,
                                        body_hygiene_verified=True),
                         "DRAFT_QA_FAILED")

    def test_attachment_discrepancy_fails(self):
        items, stored = provider()
        stored["attachments"] = [{"filename": "unverified.pdf"}]
        self.assertEqual(draft_readback(expected(), items, stored,
                                        body_hygiene_verified=True),
                         "DRAFT_QA_FAILED")

    def test_followup_event_reminder_compliance(self):
        event = {"status": "confirmed", "visibility": "private",
                 "attendees": [], "hangout_link": None,
                 "reminders": {"use_default": False, "overrides": []}}
        self.assertEqual(private_followup_state(event),
                         "FOLLOWUP_REMINDERS_OFF_BY_POLICY")
        bad = {**event, "reminders": {"use_default": True, "overrides": []}}
        self.assertEqual(private_followup_state(bad),
                         "FOLLOWUP_REMINDER_POLICY_MISMATCH")
        self.assertEqual(private_followup_state(None), "CALENDAR_NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
