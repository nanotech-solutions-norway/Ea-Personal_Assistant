import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ea_backend.projection_sink import PostgresProjectionSink, ConcurrentCursorError, IncompleteObservationError
from ea_backend.unified_sync import SourceItem, SyncContractError

class FakeCursor:
    def __init__(self, connection):
        self.c = connection
        self.single = None
        self.rows = []
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return False
    def execute(self, sql, params=None):
        self.c.queries.append((sql, params))
        if "SELECT cursor_value FROM ea_source_cursors" in sql:
            self.single = (self.c.current_cursor,) if self.c.current_cursor else None
        elif "SELECT source_id,source_revision" in sql:
            self.rows = []
        elif "INSERT INTO ea_unified_items" in sql:
            self.c.changed = (params[5], params[7])
        elif "SELECT source_revision,state FROM ea_unified_items" in sql:
            self.single = self.c.changed if self.c.valid_readback else ("wrong", "active")
        elif "INSERT INTO ea_sync_runs" in sql and self.c.fail_run:
            raise RuntimeError("simulated database failure")
    def fetchone(self):
        return self.single
    def fetchall(self):
        return self.rows

class FakeConnection:
    def __init__(self, cursor_value=None, fail_run=False, valid_readback=True):
        self.current_cursor = cursor_value
        self.fail_run = fail_run
        self.valid_readback = valid_readback
        self.changed = None
        self.queries = []
        self.committed = False
        self.rolled_back = False
        self.closed = False
    def cursor(self):
        return FakeCursor(self)
    def commit(self):
        self.committed = True
    def rollback(self):
        self.rolled_back = True
    def close(self):
        self.closed = True

def kwargs():
    return dict(run_id="synthetic-run-01", tenant_scope="business", source="google_calendar",
                collection_key="calendar-a", mode="full",
                fetched=[SourceItem("business", "google_calendar", "event-1", "rev-1",
                                    collection_key="calendar-a")],
                expected_cursor=None, next_cursor="cursor-1",
                pages_fetched=1, all_pages_fetched=True)

class ProjectionSinkTests(unittest.TestCase):
    def test_atomic_upsert_cursor_and_run(self):
        conn = FakeConnection()
        sink = PostgresProjectionSink("synthetic-dsn", connect=lambda _: conn)
        self.assertEqual(sink.capture(**kwargs()), 1)
        self.assertTrue(conn.committed)
        self.assertFalse(conn.rolled_back)
        self.assertTrue(conn.closed)
        self.assertTrue(any("INSERT INTO ea_source_cursors" in q[0] for q in conn.queries))
        self.assertTrue(any("INSERT INTO ea_sync_runs" in q[0] for q in conn.queries))
    def test_stale_cursor_rolls_back(self):
        conn = FakeConnection(cursor_value="other")
        with self.assertRaises(ConcurrentCursorError):
            PostgresProjectionSink("synthetic", connect=lambda _: conn).capture(**kwargs())
        self.assertTrue(conn.rolled_back)
        self.assertFalse(conn.committed)
    def test_partial_page_rejected_before_connection(self):
        values = kwargs()
        values["all_pages_fetched"] = False
        with self.assertRaises(IncompleteObservationError):
            PostgresProjectionSink("synthetic", connect=lambda _: self.fail("must not connect")).capture(**values)
    def test_cross_collection_item_rejected(self):
        conn = FakeConnection()
        values = kwargs()
        values["fetched"] = [SourceItem("business", "google_calendar", "event-1", "rev-1",
                                        collection_key="calendar-b")]
        with self.assertRaises(SyncContractError):
            PostgresProjectionSink("synthetic", connect=lambda _: conn).capture(**values)
        self.assertTrue(conn.rolled_back)
    def test_readback_mismatch_rolls_back(self):
        conn = FakeConnection(valid_readback=False)
        with self.assertRaises(SyncContractError):
            PostgresProjectionSink("synthetic", connect=lambda _: conn).capture(**kwargs())
        self.assertTrue(conn.rolled_back)
    def test_failure_after_cursor_sql_rolls_back_all(self):
        conn = FakeConnection(fail_run=True)
        with self.assertRaises(RuntimeError):
            PostgresProjectionSink("synthetic", connect=lambda _: conn).capture(**kwargs())
        self.assertTrue(conn.rolled_back)
        self.assertFalse(conn.committed)

if __name__ == "__main__":
    unittest.main()
