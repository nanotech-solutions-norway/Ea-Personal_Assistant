import hashlib
import hmac
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.gmail_history_source import (
    GmailHistoryExpired, collect_gmail_history
)
from ea_backend.drive_changes_source import collect_drive_changes
from ea_backend.github_delivery import verify_github_delivery
from ea_backend.unified_sync import SyncContractError


class GmailHistorySourceTests(unittest.TestCase):
    def test_two_pages_and_deduplicated_dirty_threads(self):
        calls = []
        def read(args):
            calls.append(dict(args))
            if len(calls) == 1:
                return {
                    "history": [{"id": "102", "messagesAdded": [
                        {"message": {"id": "m1", "threadId": "t1"}}]}],
                    "nextPageToken": "more"
                }
            return {
                "history": [{"id": "103", "labelsRemoved": [
                    {"message": {"id": "m2", "threadId": "t1"}},
                    {"message": {"id": "m3", "threadId": "t2"}}]}],
                "historyId": "110",
            }
        data = collect_gmail_history(start_history_id="100", list_history=read)
        self.assertEqual(data.dirty_thread_ids, ("t1", "t2"))
        self.assertEqual(data.next_history_id, "110")
        self.assertEqual(data.pages_fetched, 2)
        self.assertEqual(calls[1]["pageToken"], "more")
        self.assertEqual(calls[1]["startHistoryId"], "100")

    def test_no_events_can_have_new_mailbox_cursor(self):
        result = collect_gmail_history(
            start_history_id="100",
            list_history=lambda _: {"historyId": "115"}
        )
        self.assertEqual(result.dirty_thread_ids, ())
        self.assertEqual(result.next_history_id, "115")

    def test_expired_history_is_not_swallowed(self):
        def expired(_):
            raise GmailHistoryExpired("HTTP 404")
        with self.assertRaises(GmailHistoryExpired):
            collect_gmail_history(start_history_id="101", list_history=expired)

    def test_incomplete_and_cyclic_pages_fail(self):
        with self.assertRaises(SyncContractError):
            collect_gmail_history(start_history_id="100",
                                  list_history=lambda _: {"nextPageToken": "p"},
                                  max_pages=2)

    def test_missing_final_history_id_fails(self):
        with self.assertRaises(SyncContractError):
            collect_gmail_history(start_history_id="100",
                                  list_history=lambda _: {"history": []})


class DriveChangesSourceTests(unittest.TestCase):
    def test_multi_page_and_latest_removal_wins(self):
        calls = []
        def read(args):
            calls.append(dict(args))
            if len(calls) == 1:
                return {"changes": [
                    {"fileId": "f1", "removed": False},
                    {"fileId": "f2", "removed": False}
                ], "nextPageToken": "p2"}
            return {"changes": [
                {"fileId": "f2", "removed": True}
            ], "newStartPageToken": "new-cursor"}
        result = collect_drive_changes(start_page_token="old-cursor", list_changes=read)
        self.assertEqual(result.changed_file_ids, ("f1",))
        self.assertEqual(result.potentially_removed_file_ids, ("f2",))
        self.assertEqual(result.next_start_page_token, "new-cursor")
        self.assertEqual(calls[1]["pageToken"], "p2")

    def test_empty_change_feed_valid(self):
        result = collect_drive_changes(start_page_token="x", list_changes=lambda _:
                                       {"changes": [], "newStartPageToken": "x"})
        self.assertEqual(result.pages_fetched, 1)
        self.assertEqual(result.changed_file_ids, ())

    def test_partial_drive_response_cannot_advance(self):
        with self.assertRaises(SyncContractError):
            collect_drive_changes(start_page_token="a",
                                  list_changes=lambda _: {"changes": [], "nextPageToken": "b"},
                                  max_pages=2)

    def test_drive_wide_event_is_rejected_for_separate_handler(self):
        with self.assertRaises(SyncContractError):
            collect_drive_changes(start_page_token="a", list_changes=lambda _: {
                "changes": [{"changeType": "drive", "driveId": "d1"}],
                "newStartPageToken": "c"
            })


class GithubWebhookTests(unittest.TestCase):
    SECRET = "ci-only-fixture-secret"

    def signed(self, payload=None, event="issues"):
        if payload is None:
            payload = {"repository": {"full_name": "example/ea"},
                       "installation": {"id": 77}, "action": "opened",
                       "issue": {"title": "sensitive fixture", "updated_at": "2026-10-11T12:00:00Z"}}
        raw = json.dumps(payload).encode()
        signed = "sha256=" + hmac.new(self.SECRET.encode(), raw, hashlib.sha256).hexdigest()
        args = dict(raw_payload=raw, webhook_secret=self.SECRET,
                    headers={"X-Hub-Signature-256": signed,
                             "X-GitHub-Event": event,
                             "X-GitHub-Delivery": "synthetic-delivery-1"},
                    allowed_repositories=frozenset({"example/ea"}),
                    allowed_installation_ids=frozenset({77}))
        return args

    def test_valid_signature_and_sanitized_result(self):
        result = verify_github_delivery(**self.signed())
        self.assertEqual(result.repository_full_name, "example/ea")
        self.assertEqual(result.installation_id, 77)
        self.assertNotIn("sensitive", repr(result))

    def test_tampered_payload_rejected(self):
        args = self.signed()
        args["raw_payload"] += b" "
        with self.assertRaises(SyncContractError):
            verify_github_delivery(**args)

    def test_unexpected_installation_rejected(self):
        args = self.signed()
        args["allowed_installation_ids"] = frozenset({99})
        with self.assertRaises(SyncContractError):
            verify_github_delivery(**args)

    def test_unapproved_event_rejected(self):
        with self.assertRaises(SyncContractError):
            verify_github_delivery(**self.signed(event="deployment"))


if __name__ == "__main__":
    unittest.main()
