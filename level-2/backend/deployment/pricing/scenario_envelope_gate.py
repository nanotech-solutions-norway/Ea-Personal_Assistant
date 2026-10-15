#!/usr/bin/env python3
"""Offline, non-deployable stress envelope for an EA synthetic-only Azure pilot.

Bounds consumption volumes; uses separately recorded *public* EUR rate evidence.
It does not establish subscription charges, a tax ruling, a teardown guarantee,
or any authority to create Azure resources or synchronize live calendars.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

from timeboxed_cost_gate import REQUIRED, assess as assess_quote

CAPS = {
    "aca_peak_replicas", "aca_vcpu_per_replica", "aca_gib_per_replica",
    "aca_active_seconds_per_replica", "aca_http_requests", "dns_queries",
    "lb_processed_gb", "egress_gb", "log_ingested_gb",
    "keyvault_operations", "backup_excess_gb_month",
    "registry_storage_gb_month", "static_public_ip_count",
    "standard_lb_rule_bundle_count",
}
INTEGER_CAPS = {
    "aca_peak_replicas", "aca_active_seconds_per_replica",
    "aca_http_requests", "dns_queries", "keyvault_operations",
    "static_public_ip_count", "standard_lb_rule_bundle_count",
}
BLOCKED = "BLOCKED_NO_DEPLOYMENT"

def decimal_value(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        raise ValueError("quantity must be a nonnegative finite number")
    try:
        v = Decimal(str(value))
    except (ValueError, InvalidOperation) as exc:
        raise ValueError("quantity is not a number") from exc
    if not v.is_finite() or v < 0:
        raise ValueError("quantity must be nonnegative and finite")
    return v

def assess(envelope: object, quote: object, today: date | None = None) -> dict:
    today = today or date.today()
    errors = []
    if not isinstance(envelope, dict):
        envelope = {}
        errors.append("envelope must be an object")
    required = {
        "schema_version": "1.0",
        "project": "Ea-Personal_Assistant",
        "region": "westeurope",
        "currency": "EUR",
        "data_scope": "synthetic_only",
        "hours": 48,
        "proposal_state": "PENDING_REVIEW_NONDEPLOYABLE",
        "resource_creation_enabled": False,
        "live_provider_sync_enabled": False,
        "count_unverified_free_benefits": False,
    }
    for k, expected in required.items():
        received = envelope.get(k)
        if type(received) is not type(expected) or received != expected:
            errors.append(k + ": unexpected value or type")
    caps = envelope.get("caps")
    if not isinstance(caps, dict):
        caps = {}
        errors.append("caps table missing")
    if set(caps) != CAPS:
        errors.append("caps must enumerate exactly the bounded workload dimensions")
    values = {}
    for key in CAPS:
        try:
            values[key] = decimal_value(caps.get(key))
            if key in INTEGER_CAPS and values[key] != values[key].to_integral_value():
                errors.append(key + ": expected whole units")
        except ValueError as exc:
            errors.append(key + ": " + str(exc))
    if len(values) == len(CAPS):
        if values["aca_peak_replicas"] != 1 or values["static_public_ip_count"] != 1 or values["standard_lb_rule_bundle_count"] != 1:
            errors.append("model supports only one replica, one managed IP and first LB bundle")
        if values["aca_vcpu_per_replica"] <= 0 or values["aca_gib_per_replica"] <= 0:
            errors.append("replica CPU and memory must be positive")
        if values["aca_active_seconds_per_replica"] > Decimal(48 * 3600):
            errors.append("active replica seconds exceed 48-hour timebox")
    tail = envelope.get("post_teardown_billable_hours")
    if tail is not None:
        try:
            decimal_value(tail)
        except ValueError as exc:
            errors.append("post_teardown_billable_hours: " + str(exc))
    if envelope.get("teardown_tail_subscription_evidence_verified") is not False:
        errors.append("no verified teardown tail has been established")
    if not isinstance(quote, dict):
        errors.append("quote must be an object")
        quote = {}
    quoted = assess_quote(quote, today)
    components = quote.get("components")
    if not isinstance(components, dict):
        components = {}
    missing_prices = sorted(k for k in REQUIRED
                            if not isinstance(components.get(k), dict)
                            or components[k].get("state") not in ("priced", "excluded"))
    public_retail_partial = Decimal("0")
    for key in REQUIRED:
        item = components.get(key)
        if isinstance(item, dict) and item.get("state") == "priced":
            try:
                public_retail_partial += decimal_value(item.get("amount_eur"))
            except ValueError:
                errors.append(key + ": invalid recorded public price")
    quantities = {}
    if len(values) == len(CAPS):
        quantities = {
            "aca_vcpu_seconds_max": str(values["aca_peak_replicas"] * values["aca_vcpu_per_replica"] * values["aca_active_seconds_per_replica"]),
            "aca_gib_seconds_max": str(values["aca_peak_replicas"] * values["aca_gib_per_replica"] * values["aca_active_seconds_per_replica"]),
            "aca_http_requests_max": str(values["aca_http_requests"]),
            "dns_queries_max": str(values["dns_queries"]),
            "lb_processed_gb_max": str(values["lb_processed_gb"]),
            "data_egress_gb_max": str(values["egress_gb"]),
            "log_ingestion_gb_max": str(values["log_ingested_gb"]),
            "key_vault_operations_max": str(values["keyvault_operations"]),
            "backup_excess_gb_month_max": str(values["backup_excess_gb_month"]),
            "registry_storage_gb_month_max": str(values["registry_storage_gb_month"]),
        }
    return {
        "model_validation": "PASS" if not errors else "FAIL",
        "model_errors": errors,
        "scenario_classification": "PENDING_REVIEW_SYNTHETIC_ASSUMPTIONS",
        "bounded_usage": quantities,
        "recorded_public_retail_partial_eur": str(public_retail_partial.quantize(Decimal("0.0001"))) if not errors else None,
        "unpriced_categories": missing_prices,
        "subscription_specific_all_in_quote_verified": False,
        "teardown_tail_cost_verified": False,
        "existing_quote_gate": quoted["status"],
        "deployment_decision": BLOCKED,
        "deployment_authorized": False,
        "live_sync_authorized": False,
        "notice": "Partial public retail arithmetic is not an actual invoice or upper cost bound. No private tenant billing, taxes, residuals or independent sign-off verified.",
    }

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: scenario_envelope_gate.py <envelope.json> <existing_quote.json>", file=sys.stderr)
        return 2
    envelope = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    quote = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    outcome = assess(envelope, quote)
    print(json.dumps(outcome, indent=2))
    return 0 if outcome["model_validation"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
