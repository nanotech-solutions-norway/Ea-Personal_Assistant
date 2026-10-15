"""Adversarial offline tests: no live provider or Azure action is possible."""
import copy
from datetime import date
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenario_envelope_gate as mod

def evidence():
    envelope = json.loads((HERE / "EA_48H_SYNTHETIC_USAGE_ENVELOPE_PROPOSED_20261015.json").read_text(encoding="utf-8"))
    quote = json.loads((HERE / "EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json").read_text(encoding="utf-8"))
    return envelope, quote

class EnvelopeTests(unittest.TestCase):
    def verify(self, e, q):
        return mod.assess(e, q, date(2026, 10, 15))

    def test_baseline_is_valid_model_but_blocked_for_deployment(self):
        e, q = evidence()
        result = self.verify(e, q)
        self.assertEqual(result["model_validation"], "PASS", result["model_errors"])
        self.assertEqual(result["bounded_usage"]["aca_vcpu_seconds_max"], "1800.00")
        self.assertEqual(result["bounded_usage"]["aca_gib_seconds_max"], "3600.0")
        self.assertEqual(result["recorded_public_retail_partial_eur"], "5.9632")
        self.assertIn("taxes", result["unpriced_categories"])
        self.assertIn("container_apps_usage", result["unpriced_categories"])
        self.assertIn("container_apps_managed_auxiliary_resources", result["unpriced_categories"])
        self.assertEqual(result["existing_quote_gate"], "BLOCKED")
        self.assertFalse(result["deployment_authorized"])
        self.assertFalse(result["live_sync_authorized"])
        self.assertFalse(result["subscription_specific_all_in_quote_verified"])
        self.assertFalse(result["teardown_tail_cost_verified"])

    def test_refuse_resource_write_and_provider_sync(self):
        for flag in ("resource_creation_enabled", "live_provider_sync_enabled", "count_unverified_free_benefits"):
            e, q = evidence()
            e[flag] = True
            self.assertEqual(self.verify(e, q)["model_validation"], "FAIL", flag)

    def test_no_runtime_or_private_tenant_expansion(self):
        for field, value in [
            ("hours", 49), ("region", "eastus"), ("data_scope", "production"),
            ("proposal_state", "APPROVED"), ("project", "AtlasOrbit"),
        ]:
            e, q = evidence()
            e[field] = value
            self.assertEqual(self.verify(e, q)["model_validation"], "FAIL", field)

    def test_no_scaleout_or_extra_managed_resources(self):
        for field in ("aca_peak_replicas", "static_public_ip_count", "standard_lb_rule_bundle_count"):
            e, q = evidence()
            e["caps"][field] = 2
            self.assertEqual(self.verify(e, q)["model_validation"], "FAIL", field)

    def test_reject_nonfinite_negative_boolean_fractional_and_out_of_window(self):
        for field, value in [
            ("aca_vcpu_per_replica", "NaN"),
            ("egress_gb", "-0.1"),
            ("log_ingested_gb", "Infinity"),
            ("aca_http_requests", True),
            ("dns_queries", "1.5"),
            ("aca_active_seconds_per_replica", 172801),
        ]:
            e, q = evidence()
            e["caps"][field] = value
            self.assertEqual(self.verify(e, q)["model_validation"], "FAIL", (field, value))

    def test_missing_or_unknown_coverage_fails(self):
        e, q = evidence()
        del e["caps"]["lb_processed_gb"]
        self.assertEqual(self.verify(e, q)["model_validation"], "FAIL")
        e, q = evidence()
        e["caps"]["unreviewed_service"] = 100
        self.assertEqual(self.verify(e, q)["model_validation"], "FAIL")

    def test_unsupported_claim_of_verified_teardown_fails(self):
        e, q = evidence()
        e["teardown_tail_subscription_evidence_verified"] = True
        self.assertEqual(self.verify(e, q)["model_validation"], "FAIL")

    def test_incomplete_or_fake_quote_cannot_authorize_deployment(self):
        e, q = evidence()
        q["components"]["taxes"] = {
            "state": "priced", "amount_eur": "0", "source": "https://example.invalid/fake",
            "evidence_date": "2026-10-15"
        }
        report = self.verify(e, q)
        self.assertFalse(report["deployment_authorized"])
        self.assertFalse(report["subscription_specific_all_in_quote_verified"])

if __name__ == "__main__":
    unittest.main()
