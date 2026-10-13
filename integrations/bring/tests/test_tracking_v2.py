"""Synthetic Tracking v2 contract tests. No external requests, credentials or PII."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_tracking_v2 import (
    TEST_TRACKING_NUMBER,
    TRACKING_URL,
    validate_synthetic_delivery,
)


def synthetic_response(*, status="DELIVERED", package_number=TEST_TRACKING_NUMBER):
    return json.dumps(
        {
            "apiVersion": "2",
            "consignmentSet": [
                {
                    "consignmentId": "SYNTHETIC",
                    "packageSet": [
                        {
                            "packageNumber": package_number,
                            "eventSet": [{"status": status}],
                        }
                    ],
                }
            ],
        }
    ).encode("utf-8")


class TrackingV2Contract(unittest.TestCase):
    def test_only_official_fixed_test_identifier_is_used(self):
        self.assertIn("q=TESTPACKAGEDELIVERED", TRACKING_URL)
        self.assertEqual(TEST_TRACKING_NUMBER, "TESTPACKAGEDELIVERED")

    def test_delivered_test_number_passes(self):
        self.assertEqual(validate_synthetic_delivery(synthetic_response()), "PASS")

    def test_not_delivered_is_not_a_pass(self):
        self.assertEqual(
            validate_synthetic_delivery(synthetic_response(status="IN_TRANSIT")),
            "TEST_STATUS_MISMATCH",
        )

    def test_unrelated_package_is_not_a_pass(self):
        self.assertEqual(
            validate_synthetic_delivery(
                synthetic_response(package_number="UNRELATED_SYNTHETIC")
            ),
            "TEST_PACKAGE_MISSING",
        )

    def test_http200_nested_error_is_not_a_pass(self):
        error = {"apiVersion": "2", "consignmentSet": [{"error": {"code": 404}}]}
        self.assertEqual(
            validate_synthetic_delivery(json.dumps(error).encode("utf-8")),
            "API_ERROR",
        )

    def test_invalid_version_is_not_a_pass(self):
        self.assertEqual(
            validate_synthetic_delivery(b'{"apiVersion":"1","consignmentSet":[{}]}'),
            "INVALID_RESPONSE",
        )

    def test_empty_consignment_is_not_a_pass(self):
        self.assertEqual(
            validate_synthetic_delivery(b'{"apiVersion":"2","consignmentSet":[]}'),
            "INVALID_RESPONSE",
        )

    def test_malformed_json_rejected(self):
        with self.assertRaises(ValueError):
            validate_synthetic_delivery(b"not json")


if __name__ == "__main__":
    unittest.main()
