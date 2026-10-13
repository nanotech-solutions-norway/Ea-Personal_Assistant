"""Synthetic CI tests: approved EA staging design remains deployment-blocked."""
import copy
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation"))
from staging_decision_gate import review_decision, StagingDecisionError


class EAStagingDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "deployment" / "EA_STAGING_DECISION_WE_EUR20_20261013.json"
        cls.plan = json.loads(path.read_text(encoding="utf-8"))

    def test_operator_decision_is_valid_and_blocks_deployment(self):
        result = review_decision(self.plan)
        self.assertTrue(result["design_valid"])
        self.assertFalse(result["deployment_authorized"])
        self.assertIn("Azure subscription ownership/RBAC unverified", result["blockers"])
        self.assertIn("Subscription-specific itemized all-in price unverified", result["blockers"])
        self.assertIn("Explicit deployment authorization missing", result["blockers"])

    def test_operator_authorization_does_not_substitute_for_cloud_verification(self):
        self.assertTrue(self.plan["auth"]["operator_deployment_approval"])
        self.assertTrue(self.plan["budget"]["operator_budget_validated_attestation"])
        self.assertTrue(self.plan["subscription_reference"]["operator_provided"])
        self.assertIsNone(self.plan["subscription_id"])
        result = review_decision(self.plan)
        self.assertFalse(result["deployment_authorized"])
        self.assertIn("Azure subscription ownership/RBAC unverified", result["blockers"])
        self.assertIn("Subscription-specific itemized all-in price unverified", result["blockers"])

    def test_public_subscription_identifier_leak_is_rejected(self):
        d = copy.deepcopy(self.plan)
        d["subscription_reference"]["actual_subscription_id_committed"] = True
        with self.assertRaises(StagingDecisionError):
            review_decision(d)

    def test_budget_increase_is_not_implicitly_permitted(self):
        d = copy.deepcopy(self.plan)
        d["budget"]["monthly_ceiling"] = 200
        with self.assertRaises(StagingDecisionError):
            review_decision(d)

    def test_region_change_is_not_implicitly_permitted(self):
        d = copy.deepcopy(self.plan)
        d["region"]["azure_location"] = "eastus"
        with self.assertRaises(StagingDecisionError):
            review_decision(d)

    def test_live_sync_or_paid_creation_cannot_be_enabled(self):
        for flag in ("live_provider_sync_enabled", "paid_resource_creation_enabled",
                     "external_email_send_enabled", "level_2b_enabled"):
            with self.subTest(flag=flag):
                d = copy.deepcopy(self.plan)
                d["safety"][flag] = True
                with self.assertRaises(StagingDecisionError):
                    review_decision(d)

    def test_single_tenant_and_separation_are_mandatory(self):
        d = copy.deepcopy(self.plan)
        d["tenant"]["mode"] = "multi_tenant"
        with self.assertRaises(StagingDecisionError):
            review_decision(d)
        d = copy.deepcopy(self.plan)
        d["tenant"]["family_atlasorbit_reuse_allowed"] = True
        with self.assertRaises(StagingDecisionError):
            review_decision(d)

    def test_budget_alert_does_not_enforce_spend_limit(self):
        d = copy.deepcopy(self.plan)
        d["budget"]["azure_budget_is_hard_stop"] = True
        with self.assertRaises(StagingDecisionError):
            review_decision(d)

    def test_quote_above_ceiling_is_blocker_even_with_other_review_flags(self):
        d = copy.deepcopy(self.plan)
        d["budget"]["subscription_specific_all_in_estimate_eur"] = 31.50
        d["budget"]["estimate_verified"] = True
        out = review_decision(d)
        self.assertIn("Estimated Azure spend exceeds EUR 20/month", out["blockers"])
        self.assertFalse(out["deployment_authorized"])

    def test_even_complete_json_approval_flags_do_not_grant_cloud_authority(self):
        d = copy.deepcopy(self.plan)
        d["subscription_id"] = "00000000-0000-0000-0000-000000000000" # synthetic fixture
        d["region"]["service_sku_availability_verified"] = True
        d["budget"]["estimate_verified"] = True
        d["budget"]["subscription_specific_all_in_estimate_eur"] = 19.00
        d["auth"] = {key: True for key in d["auth"]}
        d["predeploy_gates"] = {key: True for key in d["predeploy_gates"]}
        out = review_decision(d)
        self.assertFalse(out["deployment_authorized"])
        self.assertTrue(out["requires_external_authorization_and_cloud_cost_quote"])


if __name__ == "__main__":
    unittest.main()
