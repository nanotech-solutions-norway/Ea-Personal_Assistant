#!/usr/bin/env python3
"""EA Azure staging: offline teardown coverage and public-rate delay sensitivity.

This tool cannot observe Azure, verify deletions, prove billing stopped, or grant
authority to deploy/delete resources. It refuses invented ARM confirmations.
No cloud SDK, credentials, network access, private tenant data or mutations.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

from timeboxed_cost_gate import REQUIRED, assess as assess_quote

# Required observable classes are logical obligations, not an assertion they
# exist or are in any particular Azure resource group.
RESOURCE_OBLIGATIONS = (
    "ea_primary_resource_group",
    "aca_environment",
    "aca_managed_infrastructure_resource_group",
    "aca_managed_public_egress_ip",
    "aca_managed_standard_load_balancer",
    "postgres_flexible_server",
    "postgres_storage_and_backup_retention",
    "private_dns_zone",
    "private_dns_vnet_link",
    "virtual_network_and_delegated_subnets",
    "container_registry_and_artifacts",
    "key_vault_and_secrets",
    "logs_monitoring_and_retention",
    "network_egress_and_data_processing",
    "other_service_and_billing_tail",
)
DELAY_HOURS = (0, 6, 24, 48)
KNOWN_HOURLY = (
    "postgres_compute", "container_apps_managed_public_ip",
    "container_apps_managed_load_balancer",
)
KNOWN_MONTHLY = ("postgres_storage",)
BUDGET_EUR = Decimal("20")

def decimal_nonnegative(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError("cost amount must be a nonnegative finite number")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid numeric cost amount") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError("cost amount must be nonnegative and finite")
    return amount

def assess(plan: object, quote: object) -> dict:
    errors = []
    if not isinstance(plan, dict):
        errors.append("teardown scenario must be a JSON object")
        plan = {}
    required = {
        "schema_version": "1.0",
        "project": "Ea-Personal_Assistant",
        "mode": "STATIC_PROPOSAL_NO_CLOUD_ACCESS",
        "region": "westeurope",
        "currency": "EUR",
        "data_scope": "synthetic_only",
        "monthly_cost_ceiling_eur": 20,
        "planned_execution_hours": 48,
        "resource_creation_enabled": False,
        "resource_deletion_enabled": False,
        "live_provider_sync_enabled": False,
        "customer_data_allowed": False,
        "unverified_free_grants_counted": False,
        "delete_operation_state": "NOT_ATTEMPTED",
        "independent_arm_post_delete_inventory": "UNAVAILABLE_NOT_DEPLOYED",
        "cost_management_residual_charge_reconciliation": "UNAVAILABLE_NOT_DEPLOYED",
        "no_resources_or_tail_billing_asserted": False,
        "actual_managed_resource_group_name": None,
        "subscription_specific_rates_verified": False,
        "independent_teardown_approval_recorded": False,
    }
    for name, expected in required.items():
        if type(plan.get(name)) is not type(expected) or plan.get(name) != expected:
            errors.append(name + ": unexpected value or type")
    inventory = plan.get("obligations")
    if not isinstance(inventory, dict):
        inventory = {}
        errors.append("obligations must be a dictionary")
    if set(inventory) != set(RESOURCE_OBLIGATIONS):
        errors.append("resource obligations must be exact and complete")
    for name in RESOURCE_OBLIGATIONS:
        item = inventory.get(name)
        if not isinstance(item, dict):
            errors.append(name + ": missing record")
            continue
        # No template may substitute for genuine post-deletion, independent ARM
        # and billing readback. This design artifact cannot certify a teardown.
        expected_item = {
            "predeploy_resource_inventory": "NOT_OBSERVED",
            "post_delete_arm_get": "NOT_PERFORMED",
            "billing_tail_hours_verified": False,
            "estimated_tail_eur_verified": False,
            "evidence_reference": None,
            "actual_resource_id": None,
        }
        if set(item) != set(expected_item):
            errors.append(name + ": unsupported keys or missing evidence fields")
        for field, expected in expected_item.items():
            if type(item.get(field)) is not type(expected) or item.get(field) != expected:
                errors.append(name + ": unsupported predeployment assertion in " + field)
    if not isinstance(quote, dict):
        quote = {}
        errors.append("quote must be a JSON object")
    assessment = assess_quote(quote)
    components = quote.get("components")
    if not isinstance(components, dict):
        components = {}
    unknown = sorted(k for k in REQUIRED if not isinstance(components.get(k), dict)
                     or components[k].get("state") not in ("priced", "excluded"))

    priced_known = {}
    for name in KNOWN_HOURLY + KNOWN_MONTHLY:
        item = components.get(name)
        if not isinstance(item, dict) or item.get("state") != "priced":
            errors.append(name + ": known public rate evidence missing")
            continue
        try:
            priced_known[name] = decimal_nonnegative(item.get("amount_eur"))
        except ValueError:
            errors.append(name + ": unusable recorded retail partial")
    sensitivity = []
    if len(priced_known) == len(KNOWN_HOURLY) + len(KNOWN_MONTHLY):
        # This projection is only of an earlier sampled PUBLIC subset. It does
        # not include app compute, LB processed data, tax or any unknown meter.
        # "48" matches the exact original model's billed public hourly units.
        per_hour = sum((priced_known[name] / Decimal(48) for name in KNOWN_HOURLY), Decimal(0))
        monthly_storage = priced_known["postgres_storage"]
        for delay in DELAY_HOURS:
            public_subset = monthly_storage + per_hour * Decimal(48 + delay)
            sensitivity.append({
                "hypothetical_extra_billable_hours": delay,
                "public_subset_illustration_eur": str(public_subset.quantize(Decimal("0.0001"))),
                "additional_unpriced_charges_unknown": True,
                "eligible_as_all_in_cost_cap": False,
            })
    # Even if every known public price is under EUR20, this is never a proof
    # of a worst-case all-in cap or a completed resource deletion.
    return {
        "model_validation": "PASS" if not errors else "FAIL",
        "model_errors": errors,
        "teardown_verification": "NOT_PERFORMED_NO_CLOUD_RESOURCES",
        "resource_obligations_count": len(RESOURCE_OBLIGATIONS),
        "tracked_missing_cost_categories": unknown,
        "quote_gate": assessment["status"],
        "hypothetical_public_subset_delay_sensitivity": sensitivity,
        "monthly_ceiling_eur": str(BUDGET_EUR),
        "all_in_cost_upper_bound_verified": False,
        "zero_post_teardown_liability_verified": False,
        "independent_arm_resource_deletion_verified": False,
        "subscription_specific_billing_verified": False,
        "deployment_authorized": False,
        "azure_delete_authorized": False,
        "live_sync_authorized": False,
        "decision": "BLOCKED_NO_DEPLOYMENT",
        "notice": "Delay examples use only previously recorded partial PUBLIC rates. Missing billable components, taxes and residual charges remain UNKNOWN, not zero.",
    }

def main():
    if len(sys.argv) != 3:
        print("Usage: teardown_liability_gate.py <static_plan.json> <partial_quote.json>", file=sys.stderr)
        return 2
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    quote = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    result = assess(plan, quote)
    print(json.dumps(result, indent=2))
    return 0 if result["model_validation"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
