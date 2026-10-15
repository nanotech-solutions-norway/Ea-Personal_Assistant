#!/usr/bin/env python3
"""Unauthenticated ACA EUR active compute meter discovery; strictly non-deploying.

Inspect *all* Container Apps public price rows in West Europe, not just the
ambiguous zero-valued Standard subset. Catalogue rates are neither a
subscription-specific invoice nor verification of any remaining free grant.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

from azure_foundation_meter_probe import collect, URL

OUTPUT = "ea_aca_compute_meter_candidates_20261015.json"
FIELDS = (
    "serviceName", "productName", "skuName", "meterName", "meterId", "skuId",
    "retailPrice", "unitOfMeasure", "tierMinimumUnits", "armRegionName",
    "effectiveStartDate", "isPrimaryMeterRegion", "type"
)
KIND = {
    "cpu": ("vcpu", "active", "1 second"),
    "memory": ("memory", "active", "1 gib second"),
}

def valid_amount(v):
    if isinstance(v, bool) or not isinstance(v, (str, float, int, Decimal)):
        return False
    try:
        x = Decimal(str(v))
    except (InvalidOperation, ValueError):
        return False
    return x.is_finite() and x >= 0

def inspect(rows: object, paginated: bool) -> dict:
    errors = []
    matched = {"cpu": [], "memory": []}
    if not isinstance(rows, list):
        rows = []
        errors.append("invalid catalog payload")
    if paginated is not True:
        errors.append("incomplete retail-catalog pagination")
    for row in rows:
        if not isinstance(row, dict):
            errors.append("non-object row")
            continue
        if row.get("serviceName") != "Azure Container Apps" or str(row.get("armRegionName") or "").lower() != "westeurope":
            continue
        meter_name = str(row.get("meterName") or "").lower()
        unit = str(row.get("unitOfMeasure") or "").lower()
        for kind, (keyword, required_state, required_unit) in KIND.items():
            if not (keyword in meter_name and required_state in meter_name and unit == required_unit):
                continue
            if not valid_amount(row.get("retailPrice")) or not valid_amount(row.get("tierMinimumUnits")):
                errors.append("invalid numeric meter")
                continue
            if Decimal(str(row["tierMinimumUnits"])) != 0:
                continue
            # Preserve exact billing context: Consumption rather than SavingsPlan,
            # deployment plan/product and primary-region flag.
            matched[kind].append({name: row.get(name) for name in FIELDS})
    output = {}
    for kind, group in matched.items():
        group = sorted(group, key=lambda x: (str(x.get("meterName")), str(x.get("skuId")), str(x.get("retailPrice"))))
        positive = [r for r in group if Decimal(str(r["retailPrice"])) > 0]
        zeros = [r for r in group if Decimal(str(r["retailPrice"])) == 0]
        output[kind] = {
            "classification": "PUBLIC_POSITIVE_CANDIDATES_REQUIRE_SKU_REVIEW"
                              if positive else "NO_POSITIVE_ACTIVE_CANDIDATE_FOUND",
            "observed_positive_rows": len(positive),
            "observed_zero_rows": len(zeros),
            "rows": group,
        }
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": URL,
        "region": "westeurope",
        "currency": "EUR",
        "pagination_complete": paginated is True,
        "errors": errors,
        "evidence_status": "INCOMPLETE" if errors else "CATALOG_DISCOVERY_ONLY",
        "compute_meter_groups": output,
        "subscription_tariff_verified": False,
        "free_grant_balance_verified": False,
        "all_in_cost_quote_verified": False,
        "deployment_authorized": False,
        "live_sync_authorized": False,
        "notice": "Public rates may include unrelated product plans, zero/free rows and savings-plan offers. Choose billable SKU only after authoritative independent review.",
    }

def main() -> int:
    rows, complete = collect("Azure Container Apps")
    report = inspect(rows, complete)
    Path(OUTPUT).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for kind, section in report["compute_meter_groups"].items():
        print(f"ACA_{kind.upper()}_POSITIVE_CANDIDATES={section['observed_positive_rows']}")
        print(f"ACA_{kind.upper()}_ZERO_CANDIDATES={section['observed_zero_rows']}")
        for row in section["rows"][:80]:
            print("PUBLIC_CANDIDATE " + json.dumps({"kind": kind, **row}, sort_keys=True))
    print("SUBSCRIPTION_TARIFF_VERIFIED=False")
    print("ALL_IN_COST_QUOTE_VERIFIED=False")
    print("DEPLOYMENT_AUTHORIZED=False")
    return 0 if not report["errors"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
