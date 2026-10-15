#!/usr/bin/env python3
"""Reconcile Azure PUBLIC retail catalogue rows without asserting an all-in bill.

Input: JSON captured by azure_foundation_meter_probe.py using the unauthenticated
Retail Prices API. Only explicit meter IDs and the base (tier 0) rate are considered.
No network, Azure authentication, RBAC changes, deployment or production sync.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

CATALOG_SOURCE = "https://prices.azure.com/api/retail/prices"
# These are identifiers observed in public GitHub Actions retail-catalog runs.
# A match is NOT proof that a meter applies to this Azure subscription.
METERS = {
    "aca_managed_egress_ip": ("Public IP Meter Discovery", "Virtual Network", "IP Addresses", "9c150bf9-2bad-430e-a53c-c213804f49ef", "Standard IPv4 Static Public IP", "1 Hour"),
    "aca_managed_lb_rules": ("Load Balancer", "Load Balancer", "Load Balancer", "27827eb0-7f60-4928-940b-f5fe15e7a4cb", "Standard Included LB Rules and Outbound Rules", "1 Hour"),
    "aca_managed_lb_data": ("Load Balancer", "Load Balancer", "Load Balancer", "dfc7cc11-fbe2-41c8-b6fa-24a574223938", "Standard Data Processed", "1 GB"),
    "aca_cpu_active": ("Azure Container Apps", "Azure Container Apps", "Azure Container Apps", "0426badc-b719-5201-b141-b2d5c4943b7d", "Standard vCPU Active Usage", "1 Second"),
    "aca_memory_active": ("Azure Container Apps", "Azure Container Apps", "Azure Container Apps", "3ba64b1c-cb46-5ee0-b086-a68736392ac0", "Standard Memory Active Usage", "1 GiB Second"),
    "aca_requests": ("Azure Container Apps", "Azure Container Apps", "Azure Container Apps", "b110d175-46b6-5bbc-adde-cf3438ed87f0", "Standard Requests", "1M"),
    "private_dns_zone": ("Azure DNS", "Azure DNS", "Azure DNS", "0b608a26-f611-4232-8192-ce81b6b57194", "Private Zone", "1"),
    "private_dns_queries": ("Azure DNS", "Azure DNS", "Azure DNS", "46cff9cb-4b15-4af0-bf41-25143827fef8", "Private Queries", "1M"),
}
# Platform documentation confirms CPU/memory billing even when the returned
# "Standard" meter price is 0; never infer free grants or zero costs.
METER_WITH_UNSAFE_ZERO = {"aca_cpu_active", "aca_memory_active"}
REQUIRED_GROUPS = {item[0] for item in METERS.values()}

def _decimal(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError("price must be a finite nonnegative number")
    try:
        v = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid price") from exc
    if not v.is_finite() or v < 0:
        raise ValueError("price must be finite nonnegative")
    return v

def _date(stamp: object):
    try:
        if not isinstance(stamp, str):
            return None
        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc).date() if parsed.tzinfo else None
    except ValueError:
        return None

def reconcile(catalog: object, today: date | None = None) -> dict:
    today = today or datetime.now(timezone.utc).date()
    errors = []
    if not isinstance(catalog, dict):
        catalog = {}
        errors.append("catalogue JSON must be an object")
    for key, expected in (("source", CATALOG_SOURCE), ("currency", "EUR"),
                          ("region", "westeurope"), ("cost_authorized", False)):
        if type(catalog.get(key)) is not type(expected) or catalog.get(key) != expected:
            errors.append(key + ": untrusted catalogue header")
    observed = _date(catalog.get("timestamp_utc"))
    if observed is None or (today - observed).days not in range(31):
        errors.append("catalogue captured timestamp missing, future or >30 days old")

    groups = catalog.get("services")
    if not isinstance(groups, dict):
        groups = {}
        errors.append("missing catalogue services")
    for group in REQUIRED_GROUPS:
        value = groups.get(group)
        if not isinstance(value, dict) or value.get("query_ok") is not True or value.get("pagination_complete") is not True or not isinstance(value.get("matched"), list):
            errors.append(group + ": missing/incomplete source query")

    out = {}
    for name, (group, service, product, meter_id, meter_name, unit) in METERS.items():
        collection = groups.get(group)
        rows = collection.get("matched", []) if isinstance(collection, dict) else []
        candidates = []
        for row in rows:
            if not isinstance(row, dict):
                errors.append(name + ": non-object catalogue row")
                continue
            if (row.get("serviceName") != service or row.get("productName") != product
                or row.get("meterId") != meter_id or row.get("meterName") != meter_name
                or row.get("unitOfMeasure") != unit):
                continue
            try:
                tier = _decimal(row.get("tierMinimumUnits"))
                rate = _decimal(row.get("retailPrice"))
            except ValueError:
                errors.append(name + ": malformed base tier or retail price")
                continue
            if tier != 0:
                continue  # Reject cheaper higher-volume tiers.
            region = str(row.get("armRegionName") or "").lower()
            if region not in ("westeurope", "global", ""):
                continue
            if _date(row.get("effectiveStartDate")) is None or _date(row.get("effectiveStartDate")) > today:
                errors.append(name + ": missing/future effective start")
                continue
            if row.get("skuName") != "Standard" and name not in ("private_dns_zone", "private_dns_queries"):
                continue
            if name in ("private_dns_zone", "private_dns_queries") and row.get("skuName") != "Private":
                continue
            candidates.append((region, rate, row))
        if not candidates:
            out[name] = {"classification": "MISSING_PUBLIC_METER", "public_rate_eur": None}
            errors.append(name + ": exact public retail meter not found")
            continue
        # Explicit regional meter preferred over Global; do not combine distinct SKU tiers.
        score = {"westeurope": 0, "global": 1, "": 2}
        best = min(score.get(x[0], 9) for x in candidates)
        winners = [x for x in candidates if score.get(x[0], 9) == best]
        unique_rates = {str(x[1]) for x in winners}
        if len(unique_rates) != 1:
            out[name] = {"classification": "CONFLICTING_PUBLIC_METERS", "public_rate_eur": None}
            errors.append(name + ": conflicting equally preferred rates")
            continue
        region, rate, row = winners[0]
        state = "PUBLIC_METER_CANDIDATE_UNVERIFIED"
        if rate == 0:
            state = "ZERO_PUBLIC_RATE_NOT_A_VERIFIED_FREE_BENEFIT"
        out[name] = {
            "classification": state,
            "public_rate_eur": str(rate),
            "unit_of_measure": unit,
            "region": row.get("armRegionName"),
            "sku_name": row.get("skuName"),
            "sku_id": row.get("skuId"),
            "meter_id": meter_id,
            "tier_minimum_units": "0",
            "effective_start": row.get("effectiveStartDate"),
        }
    unresolved = sorted(name for name, val in out.items()
                        if val["classification"] != "PUBLIC_METER_CANDIDATE_UNVERIFIED")
    return {
        "reconciliation_status": "VALID_PUBLIC_CANDIDATES_NOT_ACCOUNT_QUOTE" if not errors else "EVIDENCE_INCOMPLETE",
        "errors": errors,
        "source": CATALOG_SOURCE,
        "source_captured_at_utc": catalog.get("timestamp_utc") if not errors else None,
        "currency": "EUR",
        "region": "westeurope",
        "meters": out,
        "unresolved_meter_categories": unresolved,
        "zero_meter_safe_to_assume_free": False,
        "account_specific_pricing_verified": False,
        "subscription_free_benefits_verified": False,
        "all_in_cost_verified": False,
        "deployment_authorized": False,
        "live_sync_authorized": False,
        "note": "Even all-positive public candidates do not evidence real subscription charges, billing treatment, scale/usage, tax, teardown, approval or eligibility.",
    }

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: reconcile_public_retail.py <catalog.json> <output.json>", file=sys.stderr)
        return 2
    report = reconcile(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    Path(sys.argv[2]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PUBLIC_CATALOG_RECONCILIATION=" + report["reconciliation_status"])
    print("UNRESOLVED_PUBLIC_METERS=" + ",".join(report["unresolved_meter_categories"]))
    print("ALL_IN_QUOTE_VERIFIED=False")
    print("DEPLOYMENT_AUTHORIZED=False")
    return 0 if not report["errors"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
