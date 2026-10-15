"""Adversarial no-cloud teardown and residual cost stress tests."""
import copy
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import teardown_liability_gate as gate

def fixture():
    p = json.loads((HERE / "EA_48H_TEARDOWN_OBLIGATIONS_PROPOSED_20261015.json").read_text())
    q = json.loads((HERE / "EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json").read_text())
    return p,q

class TeardownTests(unittest.TestCase):
    def test_valid_proposal_still_holds_every_authorization(self):
        p,q = fixture()
        result = gate.assess(p,q)
        self.assertEqual("PASS", result["model_validation"], result["model_errors"])
        self.assertEqual(15, result["resource_obligations_count"])
        self.assertEqual("BLOCKED", result["quote_gate"])
        self.assertGreater(len(result["tracked_missing_cost_categories"]),0)
        self.assertEqual("NOT_PERFORMED_NO_CLOUD_RESOURCES",result["teardown_verification"])
        for key in ("all_in_cost_upper_bound_verified", "zero_post_teardown_liability_verified",
                    "independent_arm_resource_deletion_verified", "subscription_specific_billing_verified",
                    "deployment_authorized", "azure_delete_authorized", "live_sync_authorized"):
            self.assertIs(result[key],False,key)

    def test_public_partial_delay_sensitivity_is_not_upper_budget(self):
        p,q = fixture()
        result = gate.assess(p,q)
        values = result["hypothetical_public_subset_delay_sensitivity"]
        self.assertEqual([(0,"5.9632"), (6,"6.2266"), (24,"7.0168"), (48,"8.0704")],
                         [(x["hypothetical_extra_billable_hours"],x["public_subset_illustration_eur"]) for x in values])
        for entry in values:
            self.assertIs(entry["additional_unpriced_charges_unknown"],True)
            self.assertIs(entry["eligible_as_all_in_cost_cap"],False)

    def test_obligation_removed_or_extra_rejected(self):
        p,q=fixture()
        p["obligations"].pop("aca_managed_infrastructure_resource_group")
        self.assertEqual("FAIL",gate.assess(p,q)["model_validation"])
        p,q=fixture()
        p["obligations"]["unknown_managed_rg"]=p["obligations"]["aca_environment"]
        self.assertEqual("FAIL",gate.assess(p,q)["model_validation"])

    def test_fake_deletion_or_billing_clearance_rejected(self):
        changes=[
            ("delete_operation_state","SUCCEEDED"),
            ("independent_arm_post_delete_inventory","EMPTY"),
            ("cost_management_residual_charge_reconciliation","ZERO"),
            ("no_resources_or_tail_billing_asserted",True),
            ("subscription_specific_rates_verified",True),
            ("independent_teardown_approval_recorded",True),
            ("resource_creation_enabled",True),
            ("resource_deletion_enabled",True),
            ("live_provider_sync_enabled",True),
            ("customer_data_allowed",True),
            ("unverified_free_grants_counted",True),
            ("actual_managed_resource_group_name","ME_fabricated")
        ]
        for field,val in changes:
            p,q=fixture()
            p[field]=val
            self.assertEqual("FAIL",gate.assess(p,q)["model_validation"],field)
            self.assertFalse(gate.assess(p,q)["deployment_authorized"])

    def test_fake_arm_inventory_billing_evidence_and_costs_rejected(self):
        for field,val in (
            ("predeploy_resource_inventory","OBSERVED"),
            ("post_delete_arm_get","404"),
            ("billing_tail_hours_verified",True),
            ("estimated_tail_eur_verified",True),
            ("evidence_reference","https://example.com/fabricated"),
            ("actual_resource_id","/subscriptions/fabricated"),
        ):
            p,q=fixture()
            p["obligations"]["aca_managed_standard_load_balancer"][field]=val
            result=gate.assess(p,q)
            self.assertEqual("FAIL",result["model_validation"],field)
            self.assertFalse(result["azure_delete_authorized"])

    def test_missing_fields_and_wrong_types_rejected(self):
        for field,val in (("monthly_cost_ceiling_eur",True),("planned_execution_hours",72),
                          ("region","eastus"),("data_scope","live"),("mode","DEPLOY")):
            p,q=fixture()
            p[field]=val
            self.assertEqual("FAIL",gate.assess(p,q)["model_validation"],field)
        p,q=fixture()
        del p["obligations"]["postgres_flexible_server"]["actual_resource_id"]
        self.assertEqual("FAIL",gate.assess(p,q)["model_validation"])

    def test_public_risk_cannot_be_hidden_by_complete_synthetic_quote(self):
        p,q=fixture()
        for name,c in q["components"].items():
            if c["state"]=="unverified":
                c.update(state="priced",amount_eur="0.001",source="https://example.com/synthetic",
                         evidence_date="2026-10-15",reason="Synthetic only; NOT verified.")
        result=gate.assess(p,q)
        self.assertFalse(result["all_in_cost_upper_bound_verified"])
        self.assertFalse(result["deployment_authorized"])
        self.assertFalse(result["independent_arm_resource_deletion_verified"])

    def test_tampered_known_public_price_does_not_authorize(self):
        p,q=fixture()
        q["components"]["container_apps_managed_load_balancer"]["amount_eur"]="-1"
        result=gate.assess(p,q)
        self.assertEqual("FAIL",result["model_validation"])
        self.assertFalse(result["deployment_authorized"])

    def test_unknown_quote_missing_price_does_not_produce_zero_cost(self):
        p,q=fixture()
        del q["components"]["postgres_compute"]
        result=gate.assess(p,q)
        self.assertEqual("FAIL",result["model_validation"])
        self.assertEqual([],result["hypothetical_public_subset_delay_sensitivity"])

    def test_nonobject_and_unrecognized_fields(self):
        q=fixture()[1]
        self.assertEqual("FAIL",gate.assess(None,q)["model_validation"])
        p,q=fixture()
        p["AzureDeployerContributor"]=True
        self.assertEqual("FAIL",gate.assess(p,q)["model_validation"])
        p,q=fixture()
        p["obligations"]["private_dns_zone"]["unrecognizedOverride"]=True
        self.assertEqual("FAIL",gate.assess(p,q)["model_validation"])

if __name__=="__main__":
    unittest.main()
