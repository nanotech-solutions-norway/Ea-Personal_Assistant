#!/usr/bin/env python3
"""Offline evidence-coverage audit for the proposed EA Azure 48-hour staging BOM.

An existing parent quote marked "priced" does not prove that every subordinate
billing meter (e.g. LB rules *and* bytes) has been covered. This read-only audit
does not verify Azure billing agreements, accept attestations, authenticate,
create/delete cloud resources, or authorize provider synchronization.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import sys

from timeboxed_cost_gate import REQUIRED, assess as assess_quote

# All 20 parent cost categories retain at least one separately reviewed meter.
# Parent names are imported from the existing canonical gate, not reinterpreted.
REQUIRED_LEAVES = {
    "postgres_compute": ("pg_b1ms_instance_hours",),
    "postgres_storage": ("pg_provisioned_storage_month", "pg_post_deletion_storage_tail"),
    "postgres_backup": ("pg_excess_backup_gb_month", "pg_backup_retention_tail"),
    "container_apps_usage": ("aca_active_vcpu_seconds", "aca_active_gib_seconds", "aca_http_requests", "aca_idle_resource_usage"),
    "container_apps_environment_fee": ("aca_environment_management_fee",),
    "container_apps_managed_public_ip": ("aca_managed_static_ip_hours", "aca_managed_static_ip_tail"),
    "container_apps_managed_load_balancer": ("aca_standard_lb_base_rules_hours", "aca_standard_lb_processed_gb", "aca_standard_lb_extra_rule_hours", "aca_standard_lb_tail"),
    "container_apps_managed_auxiliary_resources": ("aca_managed_rg_other_billable_resources",),
    "container_apps_private_endpoint": ("aca_private_endpoint_hours",),
    "vnet_subnets": ("vnet_network_metered_features",),
    "private_dns": ("private_dns_zone_billing_period", "private_dns_queries"),
    "nat_or_egress_gateway": ("nat_gateway_and_attached_egress",),
    "private_link": ("private_link_endpoints_or_link_data",),
    "container_registry": ("acr_storage_gb_month", "acr_billable_tier_or_operations"),
    "key_vault": ("key_vault_secret_operations", "key_vault_service_tier"),
    "logs_monitoring": ("log_ingestion_gb", "log_retention_billable_period", "monitor_other_metered_features"),
    "data_egress": ("internet_egress_gb", "network_interregion_or_other_transfer"),
    "other_cloud": ("misc_auxiliary_platform_resources", "late_post_delete_charges"),
    "taxes": ("applicable_vat", "other_applicable_taxes"),
    "contingency": ("residual_spend_contingency",),
}
# Only these four *selected public retail candidates* had dated source arithmetic
# in the prior cost template. None is a contract or full meter price list.
PUBLIC_PARTIAL = {
    "pg_b1ms_instance_hours": "postgres_compute",
    "pg_provisioned_storage_month": "postgres_storage",
    "aca_managed_static_ip_hours": "container_apps_managed_public_ip",
    "aca_standard_lb_base_rules_hours": "container_apps_managed_load_balancer",
}
PARTIAL_PUBLIC_EVIDENCE_BASE = (
    "https://github.com/nanotech-solutions-norway/"
    "Ea-Personal_Assistant/actions/runs/"
)
VALID_STATES = {
    "UNKNOWN",
    "PUBLIC_RETAIL_PARTIAL_UNVERIFIED",
    "PROPOSED_EXCLUSION_NOT_ACCEPTED",
}
EXPECTED_COUNT = sum(map(len, REQUIRED_LEAVES.values()))


def evaluate(plan: object, quote: object, today: date | None = None) -> dict:
    today = today or date.today()
    errors: list[str] = []
    if not isinstance(plan, dict):
        plan = {}
        errors.append("evidence matrix missing")
    required_header = {
        "schema_version": "1.0",
        "project": "Ea-Personal_Assistant",
        "region": "westeurope",
        "currency": "EUR",
        "hours": 48,
        "data_scope": "synthetic_only",
        "scope_state": "NONDEPLOYABLE_PUBLIC_COVERAGE_INVENTORY",
        "billing_agreement_independently_verified": False,
        "subscription_specific_rates_verified": False,
        "tax_inclusive_total_verified": False,
        "tail_liability_verified": False,
        "independent_reviewer_approved": False,
        "resource_creation_enabled": False,
        "live_provider_sync_enabled": False,
    }
    if set(plan) != set(required_header) | {"meters", "note"}:
        errors.append("unknown or missing top-level matrix keys")
    for key, expected in required_header.items():
        if type(plan.get(key)) is not type(expected) or plan.get(key) != expected:
            errors.append(key + ": unsupported value / misleading approval claim")
    if set(REQUIRED_LEAVES) != set(REQUIRED):
        errors.append("parent categories no longer match canonical cost gate")
    meters = plan.get("meters")
    if not isinstance(meters, dict):
        meters = {}
        errors.append("missing cost meter table")
    if set(meters) != set(REQUIRED_LEAVES):
        errors.append("matrix must enumerate all 20 parent categories without extras")
    unknown: list[str] = []
    partial: list[str] = []
    proposed_exclusions: list[str] = []
    parent_with_submeters_unverified = []
    for parent, leaves in REQUIRED_LEAVES.items():
        entries = meters.get(parent)
        if not isinstance(entries, dict) or set(entries) != set(leaves):
            errors.append(parent + ": missing, duplicate or extra billable meter")
            entries = entries if isinstance(entries, dict) else {}
        has_unresolved = False
        for name in leaves:
            row = entries.get(name)
            if not isinstance(row, dict) or set(row) != {"state", "source_url", "scope_explanation"}:
                errors.append(name + ": incomplete or additional evidence fields")
                has_unresolved = True
                continue
            state = row.get("state")
            url = row.get("source_url")
            explanation = row.get("scope_explanation")
            if state not in VALID_STATES or not isinstance(explanation, str) or not (12 <= len(explanation) <= 500):
                errors.append(name + ": untrusted state or inadequate scoped explanation")
            if state == "PUBLIC_RETAIL_PARTIAL_UNVERIFIED":
                if PUBLIC_PARTIAL.get(name) != parent:
                    errors.append(name + ": no matched prior public retail price candidate")
                if not isinstance(url, str) or not url.startswith(PARTIAL_PUBLIC_EVIDENCE_BASE):
                    errors.append(name + ": missing appropriate exact public evidence source")
                partial.append(name)
            elif state == "PROPOSED_EXCLUSION_NOT_ACCEPTED":
                if url is not None:
                    errors.append(name + ": unreviewed exclusion cannot cite a price sheet")
                proposed_exclusions.append(name)
                has_unresolved = True
            else:
                if url is not None:
                    errors.append(name + ": unknown meter has fabricated evidence URL")
                unknown.append(name)
                has_unresolved = True
        if has_unresolved:
            parent_with_submeters_unverified.append(parent)
    if not isinstance(quote, dict):
        quote = {}
        errors.append("quote missing")
    quote_result = assess_quote(quote, today)
    components = quote.get("components") if isinstance(quote.get("components"), dict) else {}
    parent_marked_priced_but_children_unknown = sorted(
        k for k in parent_with_submeters_unverified
        if isinstance(components.get(k), dict) and components[k].get("state") == "priced"
    )
    # Check that all four public candidate line items still have the matched
    # priced base row, not accidental removal or replacement by zero.
    for name, parent in PUBLIC_PARTIAL.items():
        row = meters.get(parent)
        evidence_state = row.get(name, {}).get("state") if isinstance(row, dict) and isinstance(row.get(name), dict) else None
        quote_row = components.get(parent) if isinstance(components.get(parent), dict) else {}
        if evidence_state != "PUBLIC_RETAIL_PARTIAL_UNVERIFIED":
            errors.append(name + ": existing cited candidate missing from coverage matrix")
        if quote_row.get("state") != "priced" or not quote_row.get("amount_eur"):
            errors.append(name + ": existing partial quote not correctly mapped")
    # A mathematically filled quote can only become a candidate for independent
    # review; this instrument cannot verify account rates or billable tail.
    return {
        "model_validation": "PASS" if not errors else "FAIL",
        "model_errors": sorted(set(errors)),
        "required_parent_categories": len(REQUIRED),
        "required_meter_dimensions": EXPECTED_COUNT,
        "public_partial_dimensions": len(partial),
        "unverified_unknown_dimensions": len(unknown),
        "proposed_exclusions_not_independently_accepted": len(proposed_exclusions),
        "unresolved_meter_dimensions": len(unknown) + len(proposed_exclusions),
        "parent_marked_priced_but_child_meters_unverified": parent_marked_priced_but_children_unknown,
        "missing_independent_proof": sorted(
            ["account_contract_and_rates", "subscription_shared_free_grants",
             "taxes_and_vat", "bounded_teardown_tail", "independent_release_review"]
        ),
        "legacy_arithmetic_quote_state": quote_result["status"],
        "complete_meter_evidence_verified": False,
        "all_in_eur20_upper_bound_verified": False,
        "deployment_authorized": False,
        "live_calendar_sync_authorized": False,
        "classification": "BLOCKED_PRIVATE_BILLING_AND_RESIDUAL_EVIDENCE",
        "notice": "Matrix counts measure discovered coverage, not completion or independent truth. Public retail is not a contract, excluded hypotheses are not proven, zero/unknown may not be inferred as free.",
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: all_in_meter_coverage.py <proposed_matrix.json> <partial_quote.json>", file=sys.stderr)
        return 2
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    quote = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    result = evaluate(plan, quote)
    print(json.dumps(result, indent=2))
    return 0 if result["model_validation"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
