"""Deterministic, synthetic, offline tests for EA staging price gate."""
import copy
from datetime import date
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("timebox", HERE / "timeboxed_cost_gate.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
TODAY = date(2026,10,15)

def synthetic_quote():
    # All entries are fake prices/sources: NOT cloud rate evidence.
    costs = {k: {"state": "priced", "amount_eur": "0.50",
                 "source": "https://example.invalid/synthetic-test",
                 "evidence_date": "2026-10-15"} for k in mod.REQUIRED}
    return {"schema_version":"1.0", "region":"westeurope", "currency":"EUR",
            "budget_ceiling_eur":20, "planned_runtime_hours":48, "data_scope":"synthetic_only",
            "count_unverified_free_benefits":False, "resource_creation_enabled":False,
            "live_provider_sync_enabled":False, "components":costs}

class StageCostGateTests(unittest.TestCase):
    def check_blocked(self, quote):
        res = mod.assess(quote, TODAY)
        self.assertEqual("BLOCKED", res["status"])
        self.assertFalse(res["quote_complete_and_within_budget"])
        self.assertFalse(res["deployment_authorized"])

    def test_even_complete_synthetic_quote_never_authorizes_azure(self):
        x = mod.assess(synthetic_quote(), TODAY)
        self.assertEqual(x["status"],"QUOTE_WITHIN_CAP_PENDING_INDEPENDENT_GATES")
        self.assertEqual(x["estimated_eur"],str((__import__("decimal").Decimal("0.5")*len(mod.REQUIRED)).quantize(__import__("decimal").Decimal("0.001"))))
        self.assertFalse(x["deployment_authorized"])

    def test_public_incomplete_template_holds(self):
        x = json.loads((HERE/"EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json").read_text())
        self.check_blocked(x)
        self.assertIsNone(mod.assess(x,TODAY)["estimated_eur"])

    def test_managed_container_apps_resources_must_all_be_accounted_for(self):
        for component in ('container_apps_managed_public_ip','container_apps_managed_load_balancer','container_apps_managed_auxiliary_resources'):
            q=synthetic_quote()
            del q['components'][component]
            self.check_blocked(q)

    def test_missing_categories_holds(self):
        x=synthetic_quote()
        del x["components"]["private_dns"]
        self.check_blocked(x)

    def test_unverified_cost_holds(self):
        x=synthetic_quote()
        x["components"]["private_link"]={"state":"unverified","amount_eur":None}
        self.check_blocked(x)

    def test_price_total_over_cap_holds(self):
        x=synthetic_quote()
        x["components"]["postgres_compute"]["amount_eur"]="25.00"
        self.check_blocked(x)

    def test_no_deployment_if_free_credit_assumed(self):
        x=synthetic_quote()
        x["count_unverified_free_benefits"]=True
        self.check_blocked(x)

    def test_resource_create_and_live_sync_must_remain_disabled(self):
        for flag in ("resource_creation_enabled","live_provider_sync_enabled"):
            x=synthetic_quote()
            x[flag]=True
            self.check_blocked(x)

    def test_negative_and_unbounded_amounts_rejected(self):
        for n in ("-1","NaN","Infinity",None,True):
            x=synthetic_quote()
            x["components"]["data_egress"]["amount_eur"]=n
            self.check_blocked(x)

    def test_stale_evidence_holds(self):
        x=synthetic_quote()
        x["components"]["key_vault"]["evidence_date"]="2026-08-01"
        self.check_blocked(x)

    def test_no_false_zero_without_evidence(self):
        x=synthetic_quote()
        x["components"]["container_registry"]["amount_eur"]="0"
        x["components"]["container_registry"]["source"]=None
        self.check_blocked(x)

    def test_exclusion_requires_reason_and_reference(self):
        x=synthetic_quote()
        x["components"]["container_apps_private_endpoint"]={
            "state":"excluded", "amount_eur":None, "source":"https://example.invalid/architecture",
            "evidence_date":"2026-10-15","reason":"vnet integration used; managed env private endpoint not enabled"}
        self.assertTrue(mod.assess(x,TODAY)["quote_complete_and_within_budget"])
        del x["components"]["container_apps_private_endpoint"]["reason"]
        self.check_blocked(x)

    def test_region_duration_and_budget_cannot_expand(self):
        for key,value in [("region","eastus"),("planned_runtime_hours",49),
                          ("budget_ceiling_eur",100),("data_scope","live_provider")]:
            x=synthetic_quote()
            x[key]=value
            self.check_blocked(x)

    def test_unrecognized_cost_category_holds(self):
        x=synthetic_quote()
        x["components"]["shadow_fee"]={"state":"priced","amount_eur":"1","source":"https://example.invalid","evidence_date":"2026-10-15"}
        self.check_blocked(x)

if __name__=="__main__":
    unittest.main()
