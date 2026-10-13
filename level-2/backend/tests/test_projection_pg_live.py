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
from ea_backend.calendar_staging_worker import AuthorizedCalendarScope, synchronize_calendar_staging
from ea_backend.postcommit_readback import PostgresProjectionVerifier, CommittedStateUnverified

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
                ("005", "005_tenant_rls.sql"),
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
            with conn.cursor() as cur:
                cur.execute("CREATE ROLE ea_ci_scope_reader NOLOGIN")
                cur.execute("GRANT USAGE ON SCHEMA public TO ea_ci_scope_reader")
                cur.execute("GRANT SELECT ON ea_unified_items, ea_unified_links, ea_sync_runs, ea_source_cursors TO ea_ci_scope_reader")
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

    def test_postgresql_rls_restricted_role_blocks_missing_and_foreign_tenant(self):
        self.capture([self.item()])
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SET ROLE ea_ci_scope_reader")
                cur.execute("SELECT COUNT(*) FROM ea_unified_items")
                self.assertEqual(cur.fetchone()[0], 0)
                cur.execute("SELECT set_config('ea.tenant_scope', %s, true)", (self.tenant,))
                cur.execute("SELECT COUNT(*) FROM ea_unified_items WHERE tenant_scope=%s", (self.tenant,))
                self.assertEqual(cur.fetchone()[0], 1)
                cur.execute("SELECT set_config('ea.tenant_scope', %s, true)", (self.tenant + "_other",))
                cur.execute("SELECT COUNT(*) FROM ea_unified_items")
                self.assertEqual(cur.fetchone()[0], 0)
                cur.execute("SELECT COUNT(*) FROM ea_source_cursors")
                self.assertEqual(cur.fetchone()[0], 0)

    def test_tenant_scoped_cursor_saved_with_identity(self):
        self.capture([self.item()])
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT tenant_scope,collection_key FROM ea_source_cursors "
                            "WHERE tenant_scope=%s", (self.tenant,))
                self.assertEqual(cur.fetchone(), (self.tenant, self.collection))

    def restricted_verifier(self):
        def connect_as_reader(dsn):
            conn = self.psycopg.connect(dsn)
            try:
                with conn.cursor() as cur:
                    cur.execute("SET ROLE ea_ci_scope_reader")
                conn.commit()
                return conn
            except Exception:
                conn.close()
                raise
        return PostgresProjectionVerifier(DSN, connect=connect_as_reader)

    def test_calendar_staging_real_db_postcommit_and_idempotent_timezone(self):
        scope = AuthorizedCalendarScope(self.tenant, self.collection, "Europe/Madrid")
        calls = []
        def transport(params):
            calls.append(dict(params))
            return {
                "items": [{
                    "id": "event", "etag": '"rev1"', "status": "confirmed",
                    "summary": "Synthetic", "start": {
                        "dateTime": "2026-10-13T10:00:00+02:00",
                        "timeZone": "Europe/Madrid",
                    }
                }],
                "nextSyncToken": "tok2" if "syncToken" in params else "tok1",
            }
        verifier = self.restricted_verifier()
        first = synchronize_calendar_staging(
            scope=scope, run_id=uuid.uuid4().hex, list_events=transport,
            sink=self.sink, verifier=verifier, expected_cursor=None, mode="full"
        )
        self.assertEqual(first.verified_items, 1)
        self.assertEqual(first.persisted_changes, 1)
        # Repeated provider timestamp in +02:00 must equal PostgreSQL UTC readback.
        second = synchronize_calendar_staging(
            scope=scope, run_id=uuid.uuid4().hex, list_events=transport,
            sink=self.sink, verifier=verifier, expected_cursor="tok1",
            mode="incremental"
        )
        self.assertEqual(second.persisted_changes, 0)
        self.assertEqual(second.verified_items, 1)
        self.assertEqual(calls[1]["syncToken"], "tok1")

    def test_postcommit_drift_is_reported_not_retried(self):
        run = uuid.uuid4().hex
        item = self.item()
        self.capture([item], run=run)
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE ea_source_cursors SET cursor_value=%s WHERE tenant_scope=%s",
                    ("unexpected", self.tenant)
                )
        with self.assertRaises(CommittedStateUnverified):
            self.restricted_verifier().verify(
                run_id=run, tenant_scope=self.tenant,
                source="google_calendar", collection_key=self.collection,
                next_cursor="tok1", pages_fetched=1, changed=1,
                fetched=[item]
            )


if __name__ == "__main__":
    unittest.main()
