"""Adversarial offline validation of proposed non-deployable EA private topology."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("ea_vnet",HERE/"validate_private_topology.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
BASE=json.loads((HERE/"EA_48H_PRIVATE_TOPOLOGY_PROPOSED_20261015.json").read_text(encoding="utf8"))
class TopologyTest(unittest.TestCase):
    def test_expected_proposal_passes_static_only(self):
        r=mod.assess(BASE)
        self.assertEqual("PASS",r["topology_static_checks"],r["errors"])
        self.assertFalse(r["deployment_authorized"])
        self.assertFalse(r["all_in_cost_verified"])
    def fail_key(self,keys,value):
        data=copy.deepcopy(BASE)
        loc=data
        for key in keys[:-1]:loc=loc[key]
        loc[keys[-1]]=value
        result=mod.assess(data)
        self.assertEqual("FAIL",result["topology_static_checks"],keys)
        self.assertFalse(result["deployment_authorized"])
    def test_reject_public_database_or_credentials(self):
        for path,value in [
            (["network","public_database_endpoint"],True),
            (["network","public_database_firewall_allow_azure_services"],True),
            (["network","postgres_private_vnet_injection"],False),
            (["runtime","external_secrets_enabled"],True),
            (["production_data_enabled"],True),
            (["provider_sync_enabled"],True),
            (["azure_resource_create_enabled"],True),
            (["existing_readonly_oidc_identity_reused_for_deployment"],True),
        ]:self.fail_key(path,value)
    def test_subnet_overlap_invalid_and_wrong_cidr(self):
        self.fail_key(["network","subnets","container_apps","cidr"],"10.88.0.0/27")
        self.fail_key(["network","subnets","postgres","cidr"],"10.88.0.32/29")
        self.fail_key(["network","subnets","container_apps","cidr"],"10.88.0.64/28")
        self.fail_key(["network","subnets","container_apps","cidr"],"0.0.0.0/0")
    def test_no_unbilled_lb_static_ip_or_managed_resource_group(self):
        self.fail_key(["network","aca_standard_load_balancer_required"],False)
        self.fail_key(["network","aca_static_public_ip_for_egress_required"],False)
        self.fail_key(["network","aca_managed_resource_group_must_be_included_in_inventory_and_teardown"],False)
    def test_no_premium_features_stealth(self):
        for k in ("aca_env_private_endpoint_enabled","aca_dedicated_workload_profile_enabled",
                  "aca_planned_maintenance_enabled","nat_gateway_enabled"):
            self.fail_key(["network",k],True)
    def test_no_unreviewed_spend_or_credit_assumptions(self):
        for k in BASE["cost_assumptions"]:
            self.fail_key(["cost_assumptions",k],True)
    def test_timebox_and_teardown_gates(self):
        self.fail_key(["runtime_hours"],49)
        self.fail_key(["cost_ceiling_eur"],50)
        self.fail_key(["teardown","independent_managed_rg_inventory_required"],False)
        self.fail_key(["teardown","independent_empty_inventory_readback_required"],False)
        self.fail_key(["teardown","deadline_hours"],72)
    def test_invalid_delegations(self):
        self.fail_key(["network","subnets","postgres","delegation"],"Microsoft.Web/serverFarms")
        self.fail_key(["network","subnets","container_apps","delegation"],"")
if __name__=="__main__":unittest.main()
