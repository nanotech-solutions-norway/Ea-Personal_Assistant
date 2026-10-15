#!/usr/bin/env python3
"""Offline fail-closed Azure EA staging all-in cost preflight.

Checks only the completeness and arithmetic of externally sourced cost evidence.
It cannot establish Azure resource permissions, account billing or deployment
authorization. It contains NO Azure write operations.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
import json
import sys

REQUIRED = (
    "postgres_compute", "postgres_storage", "postgres_backup",
    "container_apps_usage", "container_apps_environment_fee",
    "container_apps_managed_public_ip", "container_apps_managed_load_balancer",
    "container_apps_managed_auxiliary_resources",
    "container_apps_private_endpoint", "vnet_subnets", "private_dns",
    "nat_or_egress_gateway", "private_link", "container_registry",
    "key_vault", "logs_monitoring", "data_egress", "other_cloud",
    "taxes", "contingency"
)
MAX_EUR = Decimal("20")
MAX_HOURS = 48

def _money(value):
    # JSON number or decimal string accepted; bool and null are invalid.
    if value is None or isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError("missing or invalid EUR amount")
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("non-numeric EUR amount") from exc
    if not parsed.is_finite() or parsed < 0:
        raise ValueError("EUR amounts must be finite and nonnegative")
    return parsed

def assess(obj: object, today: date | None = None) -> dict:
    today = today or date.today()
    reasons = []
    total = Decimal("0")
    complete = True
    if not isinstance(obj, dict):
        return {"status":"BLOCKED","estimated_eur":None,"reasons":["quote must be a JSON object"],"deployment_authorized":False}
    if obj.get("schema_version") != "1.0":
        reasons.append("invalid schema version")
    if obj.get("region") != "westeurope" or obj.get("currency") != "EUR":
        reasons.append("region/currency must be westeurope/EUR")
    if obj.get("budget_ceiling_eur") != 20:
        reasons.append("budget ceiling must be EUR 20")
    hours = obj.get("planned_runtime_hours")
    if isinstance(hours, bool) or not isinstance(hours, int) or not 1 <= hours <= MAX_HOURS:
        reasons.append("runtime must be 1–48 integer hours")
    if obj.get("data_scope") != "synthetic_only":
        reasons.append("only synthetic data in staged configuration")
    if obj.get("count_unverified_free_benefits") is not False:
        reasons.append("unverified Azure free allowances must not be counted")
    if obj.get("resource_creation_enabled") is not False or obj.get("live_provider_sync_enabled") is not False:
        reasons.append("resource creation and real data synchronization must remain disabled")
    components = obj.get("components")
    if not isinstance(components, dict):
        components = {}
        reasons.append("missing components table")
    absent = sorted(set(REQUIRED) - components.keys())
    extra = sorted(set(components) - set(REQUIRED))
    if absent: reasons.append("missing cost categories: " + ", ".join(absent))
    if extra: reasons.append("unrecognized cost categories: " + ", ".join(extra))
    for key in REQUIRED:
        item = components.get(key)
        if not isinstance(item, dict):
            complete = False
            continue
        state = item.get("state")
        if state not in ("priced", "excluded"):
            complete = False
            reasons.append(key + ": no verified price or explicit exclusion")
            continue
        source = item.get("source")
        evidence_date = item.get("evidence_date")
        if not isinstance(source, str) or not source.startswith("https://"):
            complete = False
            reasons.append(key + ": missing public/private evidence reference")
        try:
            stamp = date.fromisoformat(evidence_date) if isinstance(evidence_date,str) else None
        except ValueError:
            stamp = None
        if stamp is None or not (0 <= (today-stamp).days <= 30):
            complete = False
            reasons.append(key + ": missing/stale rate evidence")
        if state == "excluded":
            reason = item.get("reason")
            if not isinstance(reason, str) or len(reason.strip()) < 12:
                complete = False
                reasons.append(key + ": exclusion must explain why this feature is unused")
            if item.get("amount_eur") not in (None, 0, "0", "0.00"):
                complete = False
                reasons.append(key + ": excluded category must not carry a charge")
        else:
            try:
                total += _money(item.get("amount_eur"))
            except ValueError as exc:
                complete = False
                reasons.append(key + ": " + str(exc))
    if not complete:
        reasons.append("no complete, current, all-in estimate")
    if complete and total > MAX_EUR:
        reasons.append("fully priced total exceeds EUR 20")
    # This is a preliminary quote gate, never live Azure authorisation.
    quote_complete_and_within_budget = complete and total <= MAX_EUR and not reasons
    if quote_complete_and_within_budget:
        reasons.append("price gate only: separate Azure quota, private network design, deployer RBAC, independent audit, scope/teardown approval required")
    return {
        "status": "QUOTE_WITHIN_CAP_PENDING_INDEPENDENT_GATES" if quote_complete_and_within_budget else "BLOCKED",
        "estimated_eur": str(total.quantize(Decimal("0.001"))) if complete else None,
        "quote_complete_and_within_budget": bool(quote_complete_and_within_budget),
        "deployment_authorized": False,
        "reasons": reasons,
    }

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 timeboxed_cost_gate.py <quote.json>", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        quote = json.load(f)
    result = assess(quote)
    print(json.dumps(result, indent=2))
    return 0 if result["quote_complete_and_within_budget"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
