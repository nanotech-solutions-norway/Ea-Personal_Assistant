import json
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from workstreams.ea_crm_ops.runtime_controls import (
    CheckResult,
    DurableEventLog,
    EventConflict,
    LeaseBusy,
    StaleLease,
    UnsafeEvent,
    provider_first_preflight,
)


ROOT = Path(__file__).resolve().parents[3]
MAPPING_PATH = ROOT / "workstreams" / "ea_crm_ops" / "field_mapping.json"


def event(**overrides):
    value = {
        "event_id": "EA-CRM-OPS:test:1",
        "work_id": "EA-CRM-OPS",
        "timestamp_utc": "2026-11-25T00:00:00Z",
        "phase": "PREPARED",
        "action_tier": "A1",
        "source_sha": "synthetic",
        "target_reference": "test-only",
        "attempt": 1,
        "idempotency_key": "test-event-1",
        "event_status": "PASS",
    }
    value.update(overrides)
    return value


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))

    def test_candidate_crosswalk_has_exactly_81_unique_references(self):
        fields = self.mapping["fields"]
        self.assertEqual(len(fields), 81)
        self.assertEqual(len({(x["tab"], x["column"]) for x in fields}), 81)

    def test_identity_columns_are_immutable_and_disabled(self):
        identities = [x for x in self.mapping["fields"] if x["role"] == "identity"]
        self.assertEqual(len(identities), 14)
        self.assertTrue(all(x["write_mode"] == "IMMUTABLE" and not x["enabled"] for x in identities))

    def test_all_candidate_writes_are_disabled(self):
        self.assertTrue(all(not x["enabled"] for x in self.mapping["fields"]))
        self.assertNotEqual(self.mapping["classification"], "APPROVED")

    def test_private_provider_identity_is_not_embedded(self):
        self.assertEqual(self.mapping["provider_reference"], "OMITTED_PRIVATE_PROVIDER_ID")

    def test_81_candidate_names_match_current_provider_header_readback(self):
        snapshot = json.loads((MAPPING_PATH.parent / "header_schema_readback.json").read_text(encoding="utf-8"))
        for field in self.mapping["fields"]:
            columns = snapshot["tabs"][field["tab"]]["headers"]
            index = _column_index(field["column"])
            self.assertEqual(columns[index], field["name"], f"{field['tab']}!{field['column']}")


class DurableLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.log = DurableEventLog(Path(self.temp.name) / "events.sqlite3")

    def tearDown(self):
        self.temp.cleanup()

    def test_append_is_durable_and_idempotent(self):
        created, first_hash = self.log.append(event())
        duplicate, second_hash = self.log.append(event())
        self.assertTrue(created)
        self.assertFalse(duplicate)
        self.assertEqual(first_hash, second_hash)
        self.assertEqual(self.log.event_count(), 1)

    def test_reused_idempotency_key_with_changed_content_fails(self):
        self.log.append(event())
        with self.assertRaises(EventConflict):
            self.log.append(event(phase="VERIFIED"))

    def test_event_rows_cannot_be_updated_or_deleted(self):
        self.log.append(event())
        with sqlite3_connect(self.log.path) as db:
            with self.assertRaises(sqlite3_error()):
                db.execute("UPDATE events SET payload='{}'")
            with self.assertRaises(sqlite3_error()):
                db.execute("DELETE FROM events")

    def test_hash_chain_verifies_after_append(self):
        self.log.append(event())
        self.log.append(event(event_id="EA-CRM-OPS:test:2", idempotency_key="test-event-2"))
        self.assertTrue(self.log.verify_chain())

    def test_prohibited_customer_or_secret_fields_are_rejected(self):
        with self.assertRaises(UnsafeEvent):
            self.log.append(event(customer_email="synthetic@example.invalid"))
        with self.assertRaises(UnsafeEvent):
            self.log.append(event(token="not-a-real-token"))

    def test_concurrent_log_writes_preserve_unique_idempotency(self):
        barrier = threading.Barrier(12)

        def append_same():
            barrier.wait()
            return self.log.append(event())

        with ThreadPoolExecutor(max_workers=12) as pool:
            outcomes = list(pool.map(lambda _: append_same(), range(12)))
        self.assertEqual(sum(int(created) for created, _ in outcomes), 1)
        self.assertEqual(self.log.event_count(), 1)

    def test_only_one_concurrent_lease_wins(self):
        barrier = threading.Barrier(12)

        def acquire(index):
            barrier.wait()
            try:
                return self.log.acquire("EA-CRM-OPS", f"worker-{index}", now=1000)
            except LeaseBusy:
                return None

        with ThreadPoolExecutor(max_workers=12) as pool:
            outcomes = list(pool.map(acquire, range(12)))
        self.assertEqual(sum(token is not None for token in outcomes), 1)

    def test_expired_lease_can_be_recovered_but_stale_owner_cannot_release(self):
        old = self.log.acquire("EA-CRM-OPS", "worker-old", ttl_seconds=5, now=1000)
        new = self.log.acquire("EA-CRM-OPS", "worker-new", ttl_seconds=5, now=1006)
        with self.assertRaises(StaleLease):
            self.log.release("EA-CRM-OPS", old)
        self.log.release("EA-CRM-OPS", new)


class ProviderFirstTests(unittest.TestCase):
    def test_provider_evidence_precedes_authority_lookup(self):
        order = []
        result = provider_first_preflight(
            [("gmail-a", lambda: order.append("gmail-a") or CheckResult(True, "read-a")),
             ("gmail-b", lambda: order.append("gmail-b") or CheckResult(True, "read-b"))],
            lambda: order.append("authority") or CheckResult(True, "authority-sha"),
        )
        self.assertEqual(order, ["gmail-a", "gmail-b", "authority"])
        self.assertEqual(result.status, "PREFLIGHT_VERIFIED")

    def test_failed_provider_check_stops_before_authority(self):
        order = []
        result = provider_first_preflight(
            [("gmail-a", lambda: order.append("gmail-a") or CheckResult(False, "unavailable")),
             ("gmail-b", lambda: order.append("gmail-b") or CheckResult(True, "read-b"))],
            lambda: order.append("authority") or CheckResult(True, "authority-sha"),
        )
        self.assertEqual(order, ["gmail-a"])
        self.assertEqual(result.status, "BLOCKED")


def sqlite3_connect(path):
    import sqlite3
    return sqlite3.connect(path)


def sqlite3_error():
    import sqlite3
    return sqlite3.IntegrityError


def _column_index(column):
    result = 0
    for character in column:
        result = result * 26 + ord(character.upper()) - ord("A") + 1
    return result - 1


if __name__ == "__main__":
    unittest.main()
