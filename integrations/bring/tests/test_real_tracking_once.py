"""Offline privacy and tenant-binding tests; never use real account identifiers."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_real_tracking_once import valid_input, validate_real_shipment

REQUESTED = "ABC123456789"
COMPANY = "999111222"


def fixture(
    shipment=REQUESTED,
    customer=COMPANY,
    status="IN_TRANSIT",
    include_customer=True,
    logged_in=False,
    use_consignment=False,
):
    record = {
        "consignmentId": shipment if use_consignment else "UNRELATED_CONSIGNMENT",
        "packageSet": [
            {
                "packageNumber": "OTHERPACKAGE987" if use_consignment else shipment,
                "eventSet": [{"status": status}],
            }
        ],
        "isLoggedInSenderOrReceiver": logged_in,
    }
    if include_customer:
        record["senderCustomerNumber"] = customer
    return json.dumps({"apiVersion": "2", "consignmentSet": [record]}).encode()


class TestRealTrackingAcceptance(unittest.TestCase):
    def test_matching_customer_tracking_and_event(self):
        self.assertEqual(validate_real_shipment(fixture(), REQUESTED, COMPANY), "PASS")

    def test_matching_consignment_number(self):
        self.assertEqual(
            validate_real_shipment(fixture(use_consignment=True), REQUESTED, COMPANY),
            "PASS",
        )

    def test_other_customer_rejected(self):
        self.assertEqual(
            validate_real_shipment(fixture(customer="111222333"), REQUESTED, COMPANY),
            "TENANT_UNVERIFIED",
        )

    def test_logged_in_boolean_alone_is_insufficient(self):
        self.assertEqual(
            validate_real_shipment(
                fixture(include_customer=False, logged_in=True), REQUESTED, COMPANY
            ),
            "TENANT_UNVERIFIED",
        )

    def test_wrong_shipment_rejected(self):
        self.assertEqual(
            validate_real_shipment(fixture(shipment="DIFFERENT123"), REQUESTED, COMPANY),
            "NOT_FOUND",
        )

    def test_no_status_not_accepted(self):
        self.assertEqual(
            validate_real_shipment(fixture(status=""), REQUESTED, COMPANY),
            "STATUS_NOT_VERIFIED",
        )

    def test_invalid_version(self):
        payload = b'{"apiVersion":"1","consignmentSet":[]}'
        self.assertEqual(validate_real_shipment(payload, REQUESTED, COMPANY), "INVALID_RESPONSE")

    def test_embedded_bring_error_rejected(self):
        payload = b'{"apiVersion":"2","consignmentSet":[{"error":{"code":404}}]}'
        self.assertEqual(validate_real_shipment(payload, REQUESTED, COMPANY), "API_ERROR")

    def test_duplicate_shipments_ambiguous(self):
        shipment = json.loads(fixture())["consignmentSet"][0]
        payload = json.dumps({"apiVersion": "2", "consignmentSet": [shipment, shipment]}).encode()
        self.assertEqual(
            validate_real_shipment(payload, REQUESTED, COMPANY), "AMBIGUOUS_MATCH"
        )

    def test_block_synthetic_identifier(self):
        self.assertFalse(valid_input("TESTPACKAGEDELIVERED", COMPANY))

    def test_block_untrusted_reference_query(self):
        self.assertFalse(valid_input("ABC12345&extraInfo=true", COMPANY))

    def test_reject_invalid_customer_number(self):
        self.assertFalse(valid_input(REQUESTED, "not-a-number"))

    def test_valid_real_like_inputs(self):
        self.assertTrue(valid_input(REQUESTED, COMPANY))


if __name__ == "__main__":
    unittest.main()
