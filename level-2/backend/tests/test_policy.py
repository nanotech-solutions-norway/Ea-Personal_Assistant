import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.idempotency import action_revision, idempotency_key, approval_payload_hash
from ea_backend.policy import Decision, evaluate, assert_executable


class PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads((ROOT / "policy" / "policy-matrix.v1.json").read_text())

    def test_level2a_draft_allowed(self):
        result = evaluate(self.matrix, action="gmail.create_draft", level="level_2a")
        self.assertEqual(result.decision, Decision.ALLOW)
        assert_executable(result)

    def test_level2a_send_prohibited(self):
        result = evaluate(self.matrix, action="gmail.send_existing_draft", level="level_2a")
        self.assertEqual(result.decision, Decision.PROHIBIT)
        with self.assertRaises(PermissionError):
            assert_executable(result, approval_present=True)

    def test_level2b_send_requires_approval(self):
        result = evaluate(self.matrix, action="gmail.send_existing_draft", level="level_2b")
        self.assertEqual(result.decision, Decision.REQUIRE_APPROVAL)
        with self.assertRaises(PermissionError):
            assert_executable(result)
        assert_executable(result, approval_present=True)

    def test_unknown_action_fails_closed(self):
        result = evaluate(self.matrix, action="unknown.operation", level="level_2a")
        self.assertEqual(result.decision, Decision.PROHIBIT)

    def test_idempotency_stable(self):
        payload = {"draft_id": "d1", "body": "same"}
        rev = action_revision(payload)
        a = idempotency_key(case_id="c1", action_type="gmail.update_draft", source_id="m1", action_revision_value=rev)
        b = idempotency_key(case_id="c1", action_type="gmail.update_draft", source_id="m1", action_revision_value=rev)
        self.assertEqual(a, b)

    def test_approval_hash_changes_on_mutation(self):
        base = approval_payload_hash(
            action_type="gmail.send_existing_draft",
            recipients=["a@example.com"],
            subject="S",
            body="A",
            attachment_hashes=[],
            source_revision="r1",
        )
        changed = approval_payload_hash(
            action_type="gmail.send_existing_draft",
            recipients=["a@example.com"],
            subject="S",
            body="B",
            attachment_hashes=[],
            source_revision="r1",
        )
        self.assertNotEqual(base, changed)


if __name__ == "__main__":
    unittest.main()
