"""Real PostgreSQL integration tests, using only synthetic data.

Enabled only when EA_TEST_DATABASE_URL points to a disposable CI database.
No production or personal data. This suite intentionally checks the actual
PostgreSQL transaction and cursor commit behavior, not provider OAuth.
"""
import os
import pathlib
import sys
import unittest
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.projection_sink import PostgresProjectionSink, ConcurrentCursorError
from ea_backend.unified_sync import SourceItem, SyncContractError, source_key

DSN = os.getenv("EA_TEST_DATABASE_URL", "")


@unittest.skipUnless(DSN, "Needs disposable EA_TEST_DATABASE_URL")
class RealPostgresProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import psycopg
        cls.psycopg = psycopg
        with psycopg.connect(DSN) as conn:
            for number, name in (
                ("001", "001_initial_schema.sql"),
                ("002", "002_ingestion_events.sql"),
                ("003", "003_unified_calendar_projection.sql"),
                ("004", "004_collection_scoped_projection.sql"),
            ):
                contents = (ROOT / "sql" / name).read_text(encoding="utf-8")
                contents = "\n".join(
                    line for line in contents.splitlines()
                    if not line.lstrip().startswith("--")
                )
                with conn.cursor() as cur:
                    for command in contents.split(";"):
                        if command.strip():
                            cur.execute(command.strip())
        cls.sink = PostgresProjectionSink.from_dsn(DSN)

    def setUp(self):
        self.tenant = "ci_" + uuid.uuid4().hex
        self.collection = "synthetic-calendar-" + uuid.uuid4().hex

    def item(self, ident="event", revision="rev1", state="active", collection=None):
        return SourceItem(
            tenant_scope=self.tenant, source="google_calendar",
            source_id=ident, revision=revision, state=state,
            collection_key=collection if collection is not None else self.collection
        )

    def capture(self, fetched, run=None, mode="full", expected=None, next_cursor="tok1",
                collection=None, complete=False):
        return self.sink.capture(
            run_id=run or uuid.uuid4().hex,
            tenant_scope=self.tenant, source="google_calendar",
            collection_key=collection or self.collection, mode=mode,
            fetched=fetched, expected_cursor=expected, next_cursor=next_cursor,
            pages_fetched=1, all_pages_fetched=True, complete_full_inventory=complete
        )

    def verify_row(self, ident="event", collection=None):
        coll = collection or self.collection
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT source_revision, state, collection_key FROM ea_unified_items "
                    "WHERE item_key=%s",
                    (source_key(self.tenant, "google_calendar", ident, coll),),
                )
                return cur.fetchone()

    def test_initial_capture_and_incremental_replay(self):
        first = self.item()
        self.assertEqual(self.capture([first]), 1)
        self.assertEqual(self.verify_row(), ("rev1", "active", self.collection))
        self.assertEqual(
            self.capture([first], mode="incremental",
                         expected="tok1", next_cursor="tok2"), 0
        )
        self.assertEqual(
            self.capture([self.item(revision="rev2")], mode="incremental",
                         expected="tok2", next_cursor="tok3"), 1
        )
        self.assertEqual(self.verify_row()[0], "rev2")

    def test_stale_cursor_cannot_mutate_record(self):
        self.capture([self.item()])
        with self.assertRaises(ConcurrentCursorError):
            self.capture([self.item(revision="wrong")],
                         mode="incremental", expected=None,
                         next_cursor="bad")
        self.assertEqual(self.verify_row()[0], "rev1")

    def test_collection_isolation_with_identical_provider_ids(self):
        second = self.collection + "-other"
        self.capture([self.item()])
        self.capture([self.item(collection=second)], collection=second)
        self.assertEqual(self.verify_row()[2], self.collection)
        self.assertEqual(self.verify_row(collection=second)[2], second)

    def test_explicit_tombstone_persists(self):
        self.capture([self.item()])
        self.capture([self.item(revision="rev2", state="deleted")],
                     mode="incremental", expected="tok1", next_cursor="tok2")
        self.assertEqual(self.verify_row()[1], "deleted")

    def test_cursor_rolls_back_on_bad_source_collection(self):
        bad = self.item(collection=self.collection + "-foreign")
        with self.assertRaises(SyncContractError):
            self.capture([bad])
        self.assertIsNone(self.verify_row())
        scope = "ea:sync:" + __import__("hashlib").sha256(
            "\x1f".join((self.tenant, "google_calendar", self.collection)).encode()
        ).hexdigest()
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT cursor_value FROM ea_source_cursors WHERE source=%s", (scope,))
                self.assertIsNone(cur.fetchone())

    def test_empty_partial_inventory_never_deletes(self):
        self.capture([self.item()])
        self.capture([], mode="incremental", expected="tok1", next_cursor="tok2")
        self.assertEqual(self.verify_row()[1], "active")


if __name__ == "__main__":
    unittest.main()
