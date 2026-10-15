#!/usr/bin/env python3
"""Fail-closed *design-only* EA 48h Azure VNet topology static validator.

No Azure APIs, no provision/deletion code. Passing design lint does not
establish Azure pricing, service availability, or permission to deploy.
"""
import ipaddress
import json
import sys

def assess(obj):
    errors=[]
    if not isinstance(obj,dict):
        return {"topology_static_checks":"FAIL","errors":["not an object"],"deployment_authorized":False}
    required_static={
      "schema_version":"1.0","region":"westeurope","runtime_hours":48,
      "cost_ceiling_eur":20,"production_data_enabled":False,
      "provider_sync_enabled":False,"azure_resource_create_enabled":False,
      "existing_readonly_oidc_identity_reused_for_deployment":False}
    for k,v in required_static.items():
        if type(obj.get(k)) is not type(v) or obj.get(k)!=v:
            errors.append("invalid safety invariant: "+k)
    net=obj.get("network") or {}
    db=obj.get("db") or {}
    app=obj.get("runtime") or {}
    cost=obj.get("cost_assumptions") or {}
    deletion=obj.get("teardown") or {}
    expected_net={
       "private_dns_link_to_vnet":True,
       "public_database_endpoint":False,
       "public_database_firewall_allow_azure_services":False,
       "postgres_private_vnet_injection":True,
       "aca_workload_profiles_environment":True,
       "aca_profile":"Consumption",
       "aca_environment_internal":True,
       "aca_ingress":"internal",
       "aca_env_private_endpoint_enabled":False,
       "aca_dedicated_workload_profile_enabled":False,
       "aca_planned_maintenance_enabled":False,
       "aca_static_public_ip_for_egress_required":True,
       "aca_standard_load_balancer_required":True,
       "aca_managed_resource_group_must_be_included_in_inventory_and_teardown":True,
       "nat_gateway_enabled":False,
       "managed_dns_private_resolver_enabled":False,
       "public_webhooks_enabled":False,
    }
    for k,v in expected_net.items():
        if type(net.get(k)) is not type(v) or net.get(k)!=v:
            errors.append("network invariant violated: "+k)
    if not str(net.get("private_dns_zone","")).endswith(".postgres.database.azure.com"):
        errors.append("private zone must be under postgres.database.azure.com")
    if not isinstance(net.get("subnets"),dict):
        errors.append("missing VNet subnet mapping")
    else:
        try:
            vnet=ipaddress.ip_network(net["vnet_cidr"],strict=True)
            pg=ipaddress.ip_network(net["subnets"]["postgres"]["cidr"],strict=True)
            ca=ipaddress.ip_network(net["subnets"]["container_apps"]["cidr"],strict=True)
            if vnet.version!=4 or pg.version!=4 or ca.version!=4:
                errors.append("IPv4 private VNet required")
            if not vnet.is_private or not pg.is_private or not ca.is_private:
                errors.append("all CIDRs must be RFC1918 private")
            if not pg.subnet_of(vnet) or not ca.subnet_of(vnet) or pg.overlaps(ca):
                errors.append("subnets must be separate and inside VNet")
            if pg.prefixlen>28: errors.append("PostgreSQL private delegated subnet must be /28 or larger")
            if ca.prefixlen>27: errors.append("Container Apps workload profile subnet must be /27 or larger")
            if net["subnets"]["postgres"].get("delegation")!="Microsoft.DBforPostgreSQL/flexibleServers":
                errors.append("incorrect PostgreSQL subnet delegation")
            if net["subnets"]["container_apps"].get("delegation")!="Microsoft.App/environments":
                errors.append("incorrect Container Apps subnet delegation")
        except (KeyError,ValueError,TypeError,AttributeError):
            errors.append("invalid subnet CIDRs or delegation")
    for key,value in {"capacity_reservation_verified":False,"backup_retention_days":7,
                      "backup_geo_redundant":False,"ha_enabled":False,
                      "runtime_role_nonowner_no_bypassrls":True}.items():
        if type(db.get(key)) is not type(value) or db.get(key)!=value:
            errors.append("database setting missing or unsafe: "+key)
    if db.get("sku_candidate")!="Standard_B1ms":
        errors.append("candidate must be B1ms for current pricing model")
    if type(app.get("replicas_min")) is not int or app["replicas_min"]!=0:
        errors.append("min replicas must be zero for timebox")
    if app.get("synthetic_only") is not True or app.get("external_secrets_enabled") is not False:
        errors.append("runtime must stay synthetic and without external provider secrets")
    for key in ("free_pg_benefit_applied","aca_free_grant_unused_verified",
                "aca_load_balancer_price_verified","aca_static_ip_price_verified",
                "aca_management_meter_applies_verified","dns_monthly_billing_unit_verified",
                "all_in_quote_verified","taxes_verified","residual_costs_verified"):
        if cost.get(key) is not False:
            errors.append("must not mark unresolved cost evidence verified: "+key)
    for key,val in {"delete_full_dedicated_resource_group":True,
                    "independent_managed_rg_inventory_required":True,
                    "independent_empty_inventory_readback_required":True,
                    "deadline_hours":48,
                    "teardown_identity_authorized":False,
                    "failover_operator_assigned":False}.items():
        if type(deletion.get(key)) is not type(val) or deletion.get(key)!=val:
            errors.append("teardown constraint failed: "+key)
    return {"topology_static_checks":"PASS" if not errors else "FAIL",
            "errors":errors,"deployment_authorized":False,
            "all_in_cost_verified":False,"cloud_capacity_proven":False}

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 validate_private_topology.py <topology.json>")
    with open(sys.argv[1],encoding="utf8") as f:
        obj=json.load(f)
    result=assess(obj)
    print(json.dumps(result,indent=2))
    return 0 if result["topology_static_checks"]=="PASS" else 1
if __name__=="__main__":
    sys.exit(main())
