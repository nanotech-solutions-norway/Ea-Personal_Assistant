"""Regression tests: public price arithmetic != complete subscription bill evidence."""
import copy
from datetime import date
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import all_in_meter_coverage as mod

TODAY = date(2026, 10, 15)

def fixtures():
    p = json.loads((HERE / "EA_ALL_IN_BILLABLE_METER_MATRIX_PROPOSED_20261015.json").read_text())
    q = json.loads((HERE / "EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json").read_text())
    return p, q

class MeterCoverageTests(unittest.TestCase):
    def run_case(self, p, q):
        return mod.evaluate(p, q, TODAY)

    def test_complete_inventory_is_still_unverified_invoice(self):
        p,q = fixtures()
        r = self.run_case(p,q)
        self.assertEqual("PASS",r["model_validation"], r["model_errors"])
        self.assertEqual(20,r["required_parent_categories"])
        self.assertEqual(37,r["required_meter_dimensions"])
        self.assertEqual(4,r["public_partial_dimensions"])
        self.assertEqual(33,r["unresolved_meter_dimensions"])
        self.assertEqual("BLOCKED",r["legacy_arithmetic_quote_state"])
        self.assertIn("container_apps_managed_load_balancer", r["parent_marked_priced_but_child_meters_unverified"])
        self.assertIn("postgres_storage", r["parent_marked_priced_but_child_meters_unverified"])
        for key in ("complete_meter_evidence_verified","all_in_eur20_upper_bound_verified",
                    "deployment_authorized","live_calendar_sync_authorized"):
            self.assertIs(r[key],False,key)

    def test_claimed_private_subscription_validation_rejected(self):
        for key in ("billing_agreement_independently_verified",
                    "subscription_specific_rates_verified","tax_inclusive_total_verified",
                    "tail_liability_verified","independent_reviewer_approved"):
            p,q=fixtures()
            p[key]=True
            r=self.run_case(p,q)
            self.assertEqual("FAIL",r["model_validation"],key)
            self.assertFalse(r["deployment_authorized"])

    def test_unapproved_scope_or_writer_rejected(self):
        for key,value in (("region","eastus"),("project","AtlasOrbit"),("hours",49),
                          ("data_scope","production"),("resource_creation_enabled",True),
                          ("live_provider_sync_enabled",True),("scope_state","APPROVED")):
            p,q=fixtures()
            p[key]=value
            self.assertEqual("FAIL",self.run_case(p,q)["model_validation"],key)

    def test_unknown_or_missing_parent_and_sub_meter_rejected(self):
        p,q=fixtures()
        del p["meters"]["container_apps_usage"]
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])
        p,q=fixtures()
        del p["meters"]["container_apps_managed_load_balancer"]["aca_standard_lb_processed_gb"]
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])
        p,q=fixtures()
        p["meters"]["private_dns"]["unreviewed_dns_query"]={"state":"UNKNOWN","source_url":None,"scope_explanation":"Unpriced."}
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])

    def test_cannot_fabricate_public_rate_for_unknown_meter(self):
        p,q=fixtures()
        row=p["meters"]["container_apps_usage"]["aca_active_vcpu_seconds"]
        row["state"]="PUBLIC_RETAIL_PARTIAL_UNVERIFIED"
        row["source_url"]="https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38725912112"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])

    def test_zero_public_rate_cannot_substitute_known_price(self):
        for key in ("postgres_compute","postgres_storage","container_apps_managed_public_ip",
                    "container_apps_managed_load_balancer"):
            p,q=fixtures()
            q["components"][key]["amount_eur"]="0"
            self.assertEqual("FAIL",self.run_case(p,q)["model_validation"],key)

    def test_public_meter_substitution_and_source_tamper_rejected(self):
        p,q=fixtures()
        q["components"]["container_apps_managed_load_balancer"]["source"]="https://example.invalid/false-receipt"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])
        p,q=fixtures()
        p["meters"]["container_apps_managed_public_ip"]["aca_managed_static_ip_hours"]["source_url"]="https://example.invalid/receipt"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])

    def test_hypothetical_complete_fake_quote_cannot_prove_budget(self):
        p,q=fixtures()
        for key,component in q["components"].items():
            if component["state"]=="unverified":
                component.update(state="priced",amount_eur="0.001",source="https://example.invalid/synthetic",
                                 evidence_date="2026-10-15",reason="fake for tests only")
        r=self.run_case(p,q)
        self.assertEqual("PASS",r["model_validation"])
        self.assertEqual("QUOTE_WITHIN_CAP_PENDING_INDEPENDENT_GATES",r["legacy_arithmetic_quote_state"])
        self.assertFalse(r["complete_meter_evidence_verified"])
        self.assertFalse(r["all_in_eur20_upper_bound_verified"])
        self.assertFalse(r["deployment_authorized"])

    def test_exclusion_is_only_unverified_hypothesis(self):
        p,q=fixtures()
        row=p["meters"]["container_apps_environment_fee"]["aca_environment_management_fee"]
        self.assertEqual("PROPOSED_EXCLUSION_NOT_ACCEPTED",row["state"])
        row["source_url"]="https://example.invalid/asserted-exclusion"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])
        p,q=fixtures()
        row=p["meters"]["container_apps_environment_fee"]["aca_environment_management_fee"]
        row["state"]="INDEPENDENTLY_VERIFIED_FREE"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])

    def test_no_numeric_quote_or_false_status_upload(self):
        p,q=fixtures()
        p["customerSubscriptionId"]="FAKE_SUBSCRIPTION"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])
        p,q=fixtures()
        row=p["meters"]["private_dns"]["private_dns_queries"]
        row["source_url"]="https://example.invalid"
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])
        p,q=fixtures()
        row=p["meters"]["private_dns"]["private_dns_queries"]
        del row["state"]
        self.assertEqual("FAIL",self.run_case(p,q)["model_validation"])

    def test_wrong_row_types_fail_closed(self):
        p,q=fixtures()
        p["meters"]["taxes"]["applicable_vat"]["state"]=["APPROVED"]
        result=self.run_case(p,q)
        self.assertEqual("FAIL",result["model_validation"])
        self.assertFalse(result["deployment_authorized"])

if __name__=="__main__":
    unittest.main()
