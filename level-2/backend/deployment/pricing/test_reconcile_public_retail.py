"""Synthetic adversarial tests: PUBLIC rate signals never approve Azure usage."""
import copy
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reconcile_public_retail as meter

NOW = date(2026, 10, 15)
RATES = {
    "aca_managed_egress_ip": 0.0044,
    "aca_managed_lb_rules": 0.022,
    "aca_managed_lb_data": 0.0044,
    "aca_cpu_active": 0.0,
    "aca_memory_active": 0.0,
    "aca_requests": 0.4928,
    "private_dns_zone": 0.44,
    "private_dns_queries": 0.352,
}

def fixture():
    services = {name: {"query_ok": True, "pagination_complete": True, "matched": []}
                for name in meter.REQUIRED_GROUPS}
    for name, (group, service, product, meter_id, meter_name, unit) in meter.METERS.items():
        row = {
            "armRegionName": "westeurope" if name.startswith("aca_") else "Global",
            "effectiveStartDate": "2022-06-01T00:00:00Z",
            "isPrimaryMeterRegion": True,
            "meterId": meter_id,
            "meterName": meter_name,
            "productName": product,
            "retailPrice": RATES[name],
            "serviceName": service,
            "skuId": "synthetic-only",
            "skuName": "Private" if name.startswith("private_dns") else "Standard",
            "tierMinimumUnits": 0,
            "unitOfMeasure": unit,
        }
        services[group]["matched"].append(row)
    # Lower-price higher-tier Private DNS meter must not be selected.
    services["Azure DNS"]["matched"].append({
        **services["Azure DNS"]["matched"][0],
        "retailPrice": 0.088,
        "tierMinimumUnits": 25,
    })
    # Separate free load-balancer meter ID must never override billed base meter.
    free = copy.deepcopy(services["Load Balancer"]["matched"][0])
    free["meterId"] = "d2e60e35-f1c9-5911-a280-ec45d2f6f5e3"
    free["retailPrice"] = 0
    services["Load Balancer"]["matched"].append(free)
    return {"source": meter.CATALOG_SOURCE, "timestamp_utc": "2026-10-15T11:38:55+00:00",
            "currency": "EUR", "region": "westeurope", "cost_authorized": False,
            "services": services}

class PublicMeterTests(unittest.TestCase):
    def assess(self, c):
        return meter.reconcile(c, NOW)

    def test_catalogue_candidate_list_but_zero_cpu_memory_unresolved(self):
        r = self.assess(fixture())
        self.assertEqual("VALID_PUBLIC_CANDIDATES_NOT_ACCOUNT_QUOTE", r["reconciliation_status"], r["errors"])
        self.assertEqual(["aca_cpu_active", "aca_memory_active"], r["unresolved_meter_categories"])
        self.assertEqual("0.0044", r["meters"]["aca_managed_egress_ip"]["public_rate_eur"])
        self.assertEqual("0.022", r["meters"]["aca_managed_lb_rules"]["public_rate_eur"])
        self.assertEqual("0.44", r["meters"]["private_dns_zone"]["public_rate_eur"])
        self.assertEqual("0.352", r["meters"]["private_dns_queries"]["public_rate_eur"])
        self.assertEqual("0.4928", r["meters"]["aca_requests"]["public_rate_eur"])
        self.assertEqual("0.0", r["meters"]["aca_cpu_active"]["public_rate_eur"])
        self.assertEqual("ZERO_PUBLIC_RATE_NOT_A_VERIFIED_FREE_BENEFIT", r["meters"]["aca_cpu_active"]["classification"])
        self.assertFalse(r["zero_meter_safe_to_assume_free"])
        self.assertFalse(r["account_specific_pricing_verified"])
        self.assertFalse(r["deployment_authorized"])
        self.assertFalse(r["live_sync_authorized"])

    def test_missing_public_meter_blocks_evidence(self):
        c = fixture()
        c["services"]["Azure DNS"]["matched"] = []
        self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"])

    def test_ambiguous_equal_preference_meter_rates_fail_closed(self):
        c = fixture()
        src = c["services"]["Azure Container Apps"]["matched"][0]
        c["services"]["Azure Container Apps"]["matched"].append({**src, "retailPrice": 0.12345})
        self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"])

    def test_wrong_product_sku_or_meter_cannot_substitute(self):
        for field, value in (("skuName", "Premium"), ("productName", "OTHER"), ("unitOfMeasure", "1 GB")):
            c = fixture()
            row = next(x for x in c["services"]["Load Balancer"]["matched"] if x["meterId"] == meter.METERS["aca_managed_lb_rules"][3])
            row[field] = value
            self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"], field)

    def test_higher_tier_does_not_create_false_cheap_private_zone(self):
        c = fixture()
        c["services"]["Azure DNS"]["matched"] = [
            x for x in c["services"]["Azure DNS"]["matched"]
            if not (x["meterId"] == meter.METERS["private_dns_zone"][3] and x["tierMinimumUnits"] == 0)
        ]
        self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"])

    def test_fail_closed_invalid_values(self):
        for value in (None, True, "-1", "Infinity", "NaN"):
            c = fixture()
            c["services"]["Azure DNS"]["matched"][0]["retailPrice"] = value
            self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"], value)

    def test_reject_stale_future_untrusted_headers_and_truncation(self):
        for field, value in (("timestamp_utc", "2026-08-01T00:00:00Z"),
                             ("timestamp_utc", "2026-10-16T00:00:00Z"),
                             ("currency", "USD"), ("region", "eastus"),
                             ("source", "https://example.invalid"),
                             ("cost_authorized", True)):
            c = fixture()
            c[field] = value
            self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"], field)
        c = fixture()
        c["services"]["Azure Container Apps"]["pagination_complete"] = False
        self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"])
        c = fixture()
        c["services"]["Azure DNS"]["query_ok"] = False
        self.assertEqual("EVIDENCE_INCOMPLETE", self.assess(c)["reconciliation_status"])

    def test_region_specific_rate_preferred_over_global(self):
        c = fixture()
        row = next(x for x in c["services"]["Public IP Meter Discovery"]["matched"]
                   if x["meterId"] == meter.METERS["aca_managed_egress_ip"][3])
        c["services"]["Public IP Meter Discovery"]["matched"].append(
            {**row, "armRegionName": "Global", "retailPrice": 0.0066}
        )
        self.assertEqual("0.0044", self.assess(c)["meters"]["aca_managed_egress_ip"]["public_rate_eur"])

    def test_zeroed_hourly_meters_are_not_automatically_free(self):
        c = fixture()
        row = next(x for x in c["services"]["Load Balancer"]["matched"]
                   if x["meterId"] == meter.METERS["aca_managed_lb_rules"][3])
        row["retailPrice"] = 0
        report = self.assess(c)
        self.assertIn("aca_managed_lb_rules", report["unresolved_meter_categories"])
        self.assertFalse(report["all_in_cost_verified"])

if __name__ == "__main__":
    unittest.main()
