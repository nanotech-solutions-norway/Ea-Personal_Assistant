import base64
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from ea_runtime.events import EventValidationError, parse_calendar_headers, parse_gmail_pubsub


class EventTests(unittest.TestCase):
    def test_gmail_pubsub_parses_and_is_stable(self):
        notice = {"emailAddress": "NTSN@example.com", "historyId": "12345"}
        payload = {
            "message": {
                "messageId": "pubsub-1",
                "data": base64.b64encode(json.dumps(notice).encode()).decode(),
            }
        }
        a = parse_gmail_pubsub(payload, received_at="2026-09-30T00:00:00+00:00")
        b = parse_gmail_pubsub(payload, received_at="2026-09-30T00:00:01+00:00")
        self.assertEqual(a.event_id, b.event_id)
        self.assertEqual(a.cursor, "12345")
        self.assertEqual(a.resource_key, "ntsn@example.com")

    def test_gmail_invalid_history_rejected(self):
        notice = {"emailAddress": "a@example.com", "historyId": "not-a-number"}
        payload = {"message": {"messageId": "x", "data": base64.b64encode(json.dumps(notice).encode()).decode()}}
        with self.assertRaises(EventValidationError):
            parse_gmail_pubsub(payload)

    def test_calendar_headers_parse(self):
        event = parse_calendar_headers({
            "X-Goog-Channel-ID": "channel-1",
            "X-Goog-Resource-ID": "resource-1",
            "X-Goog-Resource-State": "exists",
            "X-Goog-Message-Number": "42",
        }, received_at="2026-09-30T00:00:00+00:00")
        self.assertEqual(event.source, "google_calendar")
        self.assertEqual(event.cursor, "42")
        self.assertEqual(event.event_kind, "exists")

    def test_calendar_missing_channel_rejected(self):
        with self.assertRaises(EventValidationError):
            parse_calendar_headers({
                "X-Goog-Resource-ID": "resource-1",
                "X-Goog-Resource-State": "exists",
                "X-Goog-Message-Number": "42",
            })


if __name__ == "__main__":
    unittest.main()
