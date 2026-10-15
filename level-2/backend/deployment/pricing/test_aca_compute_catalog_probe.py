"""Synthetic adversarial unit tests: retail discovery is never a spending approval."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aca_compute_catalog_probe as p

def row(kind="cpu", price=0, region="westeurope", source_type="Consumption"):
    name, unit = ("Standard vCPU Active Usage", "1 Second") if kind == "cpu" else ("Standard Memory Active Usage", "1 GiB Second")
    return {
        "serviceName": "Azure Container Apps", "productName": "Azure Container Apps",
        "skuName": "Standard", "meterName": name, "meterId": "SYNTHETIC-ID",
        "skuId": "SYNTHETIC-SKU", "retailPrice": price,
        "unitOfMeasure": unit, "tierMinimumUnits": 0,
        "armRegionName": region, "effectiveStartDate": "2026-01-01T00:00:00Z",
        "isPrimaryMeterRegion": True, "type": source_type,
    }

class DiscoveryTests(unittest.TestCase):
    def test_zero_only_is_not_an_eligible_free_grant(self):
        result = p.inspect([row("cpu"), row("memory")], True)
        self.assertEqual("NO_POSITIVE_ACTIVE_CANDIDATE_FOUND", result["compute_meter_groups"]["cpu"]["classification"])
        self.assertEqual(0, result["compute_meter_groups"]["memory"]["observed_positive_rows"])
        self.assertFalse(result["subscription_tariff_verified"])
        self.assertFalse(result["free_grant_balance_verified"])
        self.assertFalse(result["all_in_cost_quote_verified"])
        self.assertFalse(result["deployment_authorized"])
        self.assertFalse(result["live_sync_authorized"])

    def test_positive_row_still_does_not_authorize_anything(self):
        result = p.inspect([row("cpu", 0), row("cpu", "0.000020"), row("memory", "0.000005")], True)
        self.assertEqual(1, result["compute_meter_groups"]["cpu"]["observed_positive_rows"])
        self.assertEqual(1, result["compute_meter_groups"]["cpu"]["observed_zero_rows"])
        self.assertEqual("PUBLIC_POSITIVE_CANDIDATES_REQUIRE_SKU_REVIEW", result["compute_meter_groups"]["memory"]["classification"])
        self.assertFalse(result["subscription_tariff_verified"])
        self.assertFalse(result["deployment_authorized"])

    def test_billing_context_kept_not_cherry_picked(self):
        alternative = row("cpu", 0.00001, source_type="SavingsPlan")
        alternative["skuName"] = "Some Savings Plan"
        result = p.inspect([alternative], True)
        self.assertEqual("SavingsPlan", result["compute_meter_groups"]["cpu"]["rows"][0]["type"])
        self.assertEqual("Some Savings Plan", result["compute_meter_groups"]["cpu"]["rows"][0]["skuName"])

    def test_wrong_region_service_unit_or_state_are_excluded(self):
        others = [row("cpu", 0.0002, region="eastus"), row("cpu", 0.0003),
                  row("cpu", 0.0004), row("memory", 0.0005)]
        others[1]["serviceName"] = "Different Service"
        others[2]["unitOfMeasure"] = "1 Hour"
        others[3]["meterName"] = "Memory Idle Usage"
        result = p.inspect(others, True)
        self.assertEqual([], result["compute_meter_groups"]["cpu"]["rows"])
        self.assertEqual([], result["compute_meter_groups"]["memory"]["rows"])

    def test_fail_closed_missing_or_broken_pagination(self):
        for rows, complete in ((None, True), ([row()], False)):
            result = p.inspect(rows, complete)
            self.assertEqual("INCOMPLETE", result["evidence_status"])
            self.assertFalse(result["deployment_authorized"])

    def test_reject_nan_infinite_negative_and_boolean_rates(self):
        for price in ("NaN", "Infinity", "-0.001", True, None):
            result = p.inspect([row(price=price)], True)
            self.assertEqual("INCOMPLETE", result["evidence_status"], price)
            self.assertEqual(0, result["compute_meter_groups"]["cpu"]["observed_positive_rows"])

    def test_ignore_high_volume_tier_for_small_pilot(self):
        high_tier = row("cpu", "0.000001")
        high_tier["tierMinimumUnits"] = 1000000
        result = p.inspect([high_tier], True)
        self.assertEqual([], result["compute_meter_groups"]["cpu"]["rows"])

    def test_do_not_claim_full_account_quote_for_any_catalog_data(self):
        result = p.inspect([row("cpu", 0.00003), row("memory", 0.000006)], True)
        for flag in ("subscription_tariff_verified", "free_grant_balance_verified",
                     "all_in_cost_quote_verified", "deployment_authorized", "live_sync_authorized"):
            self.assertIs(result[flag], False)

if __name__ == "__main__":
    unittest.main()
