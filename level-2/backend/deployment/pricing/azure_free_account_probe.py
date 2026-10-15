#!/usr/bin/env python3
"""Private-by-default Azure free-benefit metadata probe (read-only).

Requires prior Azure/login OIDC, existing Reader role, and AZURE_SUBSCRIPTION_ID.
Does not make a subscription-specific claim about 12-month B1ms allowance
unless source metadata explicitly supports it. Public CI logs never include
billing account IDs, raw billing records or token values.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys

UUID = re.compile(r"^[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")
BASE = "https://management.azure.com"

def classify_billing(response):
    if not isinstance(response, dict) or not isinstance(response.get("properties"), dict):
        return "INCONCLUSIVE"
    billing_type = str(response["properties"].get("subscriptionBillingType", "")).strip()
    # "Paid" can be upgraded Azure Free Account still within its 12-month free period.
    if billing_type == "Free":
        return "FREE_BILLING_TYPE_REPORTED_NOT_FREE_SERVICE_PROOF"
    if billing_type in {"Paid", "PrePaid", "Benefit"}:
        return "NONFREE_BILLING_TYPE_FREE_SERVICES_STILL_POSSIBLE"
    return "INCONCLUSIVE"

def classify_free_services(response, now=None):
    """Examine only explicit Active PostgreSQL benefit records, never infer no entitlement."""
    if not isinstance(response, dict) or not isinstance(response.get("value"), list):
        return "INCONCLUSIVE"
    now = now or datetime.datetime.now(datetime.timezone.utc)
    matches = 0
    for row in response["value"]:
        if not isinstance(row, dict):
            continue
        p = row.get("properties")
        if not isinstance(p, dict) or str(p.get("status")) != "Active":
            continue
        end = p.get("endAt")
        if isinstance(end, str) and end:
            try:
                deadline = datetime.datetime.fromisoformat(end.replace("Z", "+00:00"))
                if deadline <= now:
                    continue
            except ValueError:
                continue
        details = p.get("productDetails") or {}
        if not isinstance(details, dict):
            details = {}
        searchable = " ".join(str(x) for x in (
            p.get("displayName", ""), details.get("skuTitle", ""), details.get("productFamily", ""),
        )).lower()
        if "postgres" in searchable:
            matches += 1
    return "ACTIVE_PG_BENEFIT_RECORD_CANDIDATE" if matches else "NO_PG_RECORD_FOUND_NOT_DISPROOF"

def read_rest(url):
    # No shell, no raw response/error forwarding: Azure billing records are private.
    try:
        proc = subprocess.run(
            ["az", "rest", "--method", "get", "--url", url, "--only-show-errors", "--output", "json"],
            capture_output=True, text=True, timeout=75, check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None, "UNAVAILABLE"
    if proc.returncode:
        return None, "UNAVAILABLE_OR_UNAUTHORIZED"
    try:
        return json.loads(proc.stdout), "READ_OK"
    except (json.JSONDecodeError, ValueError):
        return None, "INVALID_RESPONSE"

def main():
    sub = os.environ.get("AZURE_SUBSCRIPTION_ID", "").strip()
    if not UUID.fullmatch(sub):
        print("Azure subscription environment variable invalid or missing", file=sys.stderr)
        return 2
    billing_url = f"{BASE}/subscriptions/{sub}/providers/Microsoft.Billing/billingProperty/default?api-version=2024-04-01"
    benefits_url = f"{BASE}/subscriptions/{sub}/providers/Microsoft.BillingBenefits/freeServices?api-version=2026-06-01"
    bill, bill_transport = read_rest(billing_url)
    benefits, benefit_transport = read_rest(benefits_url)
    result = {
        "billing_property_access": bill_transport,
        "billing_type_signal": classify_billing(bill),
        "billing_benefits_access": benefit_transport,
        "pg_benefit_record_signal": classify_free_services(benefits),
        "twelve_month_postgresql_b1ms_750h_and_32gb_entitlement": "NOT_INDEPENDENTLY_VERIFIED",
        "unused_monthly_entitlement_and_credit_balance": "NOT_INDEPENDENTLY_VERIFIED",
        "deployment_authorized": False,
        "reason": ("Free-account twelve-month allowances and remaining usage require"
                   " direct Free services table verification or equivalent conclusive billing evidence."),
    }
    # Summary is public for a public GitHub repo; only coarse status, no raw payloads.
    print("EA Azure read-only free-account evidence summary")
    for k, v in result.items():
        print(f"  {k}: {v}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("### EA Azure free-account evidence (read-only; no billing identifiers)\n")
            for k, v in result.items():
                f.write(f"- **{k.replace('_',' ')}:** {v}\n")
            f.write("Check the subscription's **Free services for 12 months** table in Azure Portal for B1ms/32 GB and remaining monthly usage; no benefits assumed in the EUR20 cost model.\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
