import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.calendar_source import CalendarTokenExpired, collect_calendar_events, normalize_event
from ea_backend.unified_sync import SyncContractError


def event(uid="e1", rev='"tag1"', status="confirmed", start=None):
    return {"id": uid, "etag": rev, "status": status, "summary": "Synthetic meeting",
            "start": start or {"dateTime": "2026-10-12T10:00:00+02:00"}}


class CalendarSourceTests(unittest.TestCase):
    def args(self):
        return dict(tenant_scope="business", calendar_id="cal-1",
                    calendar_timezone="Europe/Madrid")

    def test_full_pagination_returns_only_final_sync_token(self):
        observed = []
        def transport(params):
            observed.append(dict(params))
            if len(observed) == 1:
                return {"items": [event()], "nextPageToken": "page-2"}
            return {"items": [event("e2", '"tag2"')], "nextSyncToken": "sync-101"}
        res = collect_calendar_events(list_events=transport, **self.args())
        self.assertEqual(res.pages_fetched, 2)
        self.assertEqual(len(res.items), 2)
        self.assertEqual(res.source_cursor, "sync-101")
        self.assertEqual(observed[1]["pageToken"], "page-2")
        self.assertFalse(any("timeMin" in p or "timeMax" in p for p in observed))
        self.assertTrue(all(p["showDeleted"] == "true" for p in observed))

    def test_incremental_uses_sync_token_without_time_filter(self):
        seen = []
        def transport(params):
            seen.append(dict(params))
            return {"items": [event(status="cancelled")], "nextSyncToken": "sync-102"}
        obs = collect_calendar_events(list_events=transport, sync_token="sync-101", **self.args())
        self.assertEqual(seen[0]["syncToken"], "sync-101")
        self.assertEqual(obs.items[0].state, "deleted")
        self.assertEqual(obs.items[0].collection_key, "cal-1")

    def test_all_day_midnight_resolves_calendar_timezone(self):
        item = normalize_event(event(start={"date": "2026-10-12"}), **self.args())
        self.assertEqual(item.due_at, "2026-10-12T00:00:00+02:00")
        self.assertEqual(item.timezone, "Europe/Madrid")

    def test_missing_etag_fails_without_silent_skip(self):
        record = event()
        record.pop("etag")
        with self.assertRaises(SyncContractError):
            collect_calendar_events(list_events=lambda _: {"items": [record],
                                                            "nextSyncToken": "t"}, **self.args())

    def test_pagination_incomplete_fails_closed(self):
        with self.assertRaises(SyncContractError):
            collect_calendar_events(list_events=lambda _: {"items": [event()],
                                                            "nextPageToken": "p"}, max_pages=1,
                                    **self.args())

    def test_expired_token_is_reported_for_upstream_resync(self):
        def expired(_):
            raise CalendarTokenExpired("HTTP 410")
        with self.assertRaises(CalendarTokenExpired):
            collect_calendar_events(list_events=expired, sync_token="invalid",
                                    **self.args())

    def test_dual_page_and_sync_tokens_fail_closed(self):
        with self.assertRaises(SyncContractError):
            collect_calendar_events(list_events=lambda _: {"items": [], "nextPageToken": "p",
                                                            "nextSyncToken": "s"}, **self.args())


if __name__ == "__main__":
    unittest.main()
