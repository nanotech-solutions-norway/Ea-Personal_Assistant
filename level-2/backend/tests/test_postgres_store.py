import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from ea_runtime.events import EventEnvelope
from ea_runtime.postgres_store import PostgresEventStore


class FakeCursor:
    def __init__(self, row):
        self.row = row
        self.executed = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed = (sql, params)

    def fetchone(self):
        return self.row


class FakeConnection:
    def __init__(self, row=("event",), *, fail=False):
        self.cursor_obj = FakeCursor(row)
        self.fail = fail
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self):
        if self.fail:
            raise RuntimeError("db failure")
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


def event():
    return EventEnvelope(
        event_id="e1",
        source="gmail",
        received_at="2026-09-30T00:00:00+00:00",
        cursor="123",
        resource_key="a@example.com",
        event_kind="mailbox_history_changed",
        metadata={"x": "y"},
    )


class PostgresStoreTests(unittest.TestCase):
    def test_insert_returns_true(self):
        conn = FakeConnection(row=("e1",))
        store = PostgresEventStore("dsn", connect=lambda _: conn)
        self.assertTrue(store.put_if_absent(event()))
        self.assertTrue(conn.committed)
        self.assertTrue(conn.closed)

    def test_duplicate_returns_false(self):
        conn = FakeConnection(row=None)
        store = PostgresEventStore("dsn", connect=lambda _: conn)
        self.assertFalse(store.put_if_absent(event()))
        self.assertTrue(conn.committed)

    def test_failure_rolls_back(self):
        conn = FakeConnection(fail=True)
        store = PostgresEventStore("dsn", connect=lambda _: conn)
        with self.assertRaises(RuntimeError):
            store.put_if_absent(event())
        self.assertTrue(conn.rolled_back)
        self.assertTrue(conn.closed)

    def test_healthcheck(self):
        conn = FakeConnection(row=(1,))
        store = PostgresEventStore("dsn", connect=lambda _: conn)
        self.assertTrue(store.healthcheck())


if __name__ == "__main__":
    unittest.main()
