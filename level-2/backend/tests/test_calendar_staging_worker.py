"""No-provider staging worker tests: fake transport and fake sinks only."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.calendar_source import CalendarTokenExpired
from ea_backend.calendar_staging_worker import AuthorizedCalendarScope, synchronize_calendar_staging
from ea_backend.postcommit_readback import CommittedStateUnverified, ReadbackReceipt
from ea_backend.unified_sync import SyncContractError


SCOPE = AuthorizedCalendarScope("ci-tenant", "calendar-1", "Europe/Madrid")


def event(uid="event1", revision='"revision1"'):
    return {
        "id": uid, "etag": revision, "status": "confirmed",
        "summary": "Synthetic", "start": {
            "dateTime": "2026-10-13T10:00:00+02:00",
            "timeZone": "Europe/Madrid"
        }
    }


class RecordingSink:
    def __init__(self):
        self.calls = []

    def capture(self, **kwargs):
        self.calls.append(kwargs)
        return len(kwargs["fetched"])


class RecordingVerifier:
    def __init__(self, *, fail=False):
        self.calls = []
        self.fail = fail

    def verify(self, **kwargs):
        self.calls.append(kwargs)
        if self.fail:
            raise CommittedStateUnverified("Simulated post-commit mismatch")
        return ReadbackReceipt(
            kwargs["run_id"], kwargs["tenant_scope"], kwargs["source"],
            kwargs["collection_key"], len(kwargs["fetched"]), kwargs["changed"]
        )


class CalendarStagingWorkerTests(unittest.TestCase):
    def test_full_scan_commits_after_all_pages_and_readback(self):
        sink, verifier = RecordingSink(), RecordingVerifier()
        seen = []
        def transport(params):
            seen.append(dict(params))
            return ({"items": [event()], "nextPageToken": "page-2"} if len(seen) == 1
                    else {"items": [event("event2", '"rev2"')], "nextSyncToken": "token-1"})
        receipt = synchronize_calendar_staging(
            scope=SCOPE, run_id="run1", list_events=transport,
            sink=sink, verifier=verifier, expected_cursor=None, mode="full"
        )
        self.assertEqual(receipt.verified_items, 2)
        self.assertEqual(sink.calls[0]["pages_fetched"], 2)
        self.assertEqual(sink.calls[0]["next_cursor"], "token-1")
        self.assertFalse(sink.calls[0]["complete_full_inventory"])
        self.assertEqual(verifier.calls[0]["run_id"], "run1")
        self.assertNotIn("syncToken", seen[0])

    def test_incremental_requires_trusted_previous_cursor(self):
        sink, verifier = RecordingSink(), RecordingVerifier()
        with self.assertRaises(SyncContractError):
            synchronize_calendar_staging(
                scope=SCOPE, run_id="run2", list_events=lambda p: {},
                sink=sink, verifier=verifier, expected_cursor=None, mode="incremental"
            )
        self.assertFalse(sink.calls)

    def test_expired_google_cursor_does_not_call_sink(self):
        sink, verifier = RecordingSink(), RecordingVerifier()
        def expired(_):
            raise CalendarTokenExpired("HTTP 410")
        with self.assertRaises(CalendarTokenExpired):
            synchronize_calendar_staging(
                scope=SCOPE, run_id="run3", list_events=expired,
                sink=sink, verifier=verifier, expected_cursor="expired", mode="incremental"
            )
        self.assertFalse(sink.calls)
        self.assertFalse(verifier.calls)

    def test_partial_paging_fails_closed_before_commit(self):
        sink, verifier = RecordingSink(), RecordingVerifier()
        with self.assertRaises(SyncContractError):
            synchronize_calendar_staging(
                scope=SCOPE, run_id="run4",
                list_events=lambda p: {"items": [], "nextPageToken": "stuck"},
                sink=sink, verifier=verifier, expected_cursor=None, mode="full",
                max_pages=2
            )
        self.assertFalse(sink.calls)

    def test_readback_failure_does_not_trigger_automatic_replay(self):
        sink, verifier = RecordingSink(), RecordingVerifier(fail=True)
        with self.assertRaises(CommittedStateUnverified):
            synchronize_calendar_staging(
                scope=SCOPE, run_id="run5",
                list_events=lambda p: {"items": [event()], "nextSyncToken": "tok"},
                sink=sink, verifier=verifier, expected_cursor=None, mode="full"
            )
        self.assertEqual(len(sink.calls), 1)
        self.assertEqual(len(verifier.calls), 1)


if __name__ == "__main__":
    unittest.main()
