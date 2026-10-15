#!/usr/bin/env python3
"""Offline, local-only examination of private MCA billing-profile price-sheet CSV.

Never copies, uploads or emits billing profiles, subscription IDs, row contents,
negotiated prices, paths or credentials. No Azure SDK, token or network access.
An operator-supplied private sheet is not a trusted deployment authorization.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import sys

METERS = {
    "aca_cpu_active": ("0426badc-b719-5201-b141-b2d5c4943b7d", "vcpu", "active", "second"),
    "aca_memory_active": ("3ba64b1c-cb46-5ee0-b086-a68736392ac0", "memory", "active", "gib"),
}
MAX_BYTES = 25 * 1024 * 1024
REGIONS = {"westeurope", "eu west", "west europe"}
REQUIRED_FIELDS = {
    "meterId", "meterName", "meterRegion", "priceType",
    "tierMinimumUnits", "unitOfMeasure", "unitPrice", "currency",
    "billingCurrency", "billingProfileId", "productOrderName",
}
REPO_ROOT = Path(__file__).resolve().parents[4]


def _decimal(value: object) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        return None
    try:
        result = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None
    return result if result.is_finite() and result >= 0 else None


def _date(value: object) -> date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


def assess_rows(rows: object, *, expected_profile: str | None, today: date) -> dict:
    """Only aggregate NON-SENSITIVE counters, never actual prices or row values."""
    result = {
        name: {"matched_rows": 0, "positive_candidates": 0,
               "zero_candidates": 0, "ambiguous_or_invalid": 0,
               "classification": "NOT_FOUND"}
        for name in METERS
    }
    errors = []
    if not isinstance(rows, list):
        rows = []
        errors.append("invalid sheet data type")
    if not isinstance(expected_profile, str) or len(expected_profile.strip()) < 3:
        errors.append("private billing profile expected value is missing")
        expected_profile = None
    for row in rows:
        if not isinstance(row, dict):
            errors.append("invalid sheet row")
            continue
        meter_id = str(row.get("meterId") or "")
        matched = [k for k, v in METERS.items() if v[0].casefold() == meter_id.casefold()]
        if not matched:
            continue
        name = matched[0]
        item = result[name]
        item["matched_rows"] += 1
        rname = str(row.get("meterName") or "").casefold()
        region = str(row.get("meterRegion") or "").casefold()
        unit = str(row.get("unitOfMeasure") or "").casefold()
        price_type = str(row.get("priceType") or "").casefold()
        amount = _decimal(row.get("unitPrice"))
        tier = _decimal(row.get("tierMinimumUnits"))
        row_currency = str(row.get("currency") or "").upper()
        bill_currency = str(row.get("billingCurrency") or "").upper()
        profile = row.get("billingProfileId")
        order = row.get("productOrderName")
        start = _date(row.get("effectiveStartDate"))
        end = _date(row.get("effectiveEndDate"))
        # Reject mismatched currency and missing profile binding. The sheet is
        # private, but the connection to the authorized EA billing agreement
        # still requires independent human confirmation after this check.
        valid = (
            expected_profile is not None and profile == expected_profile
            and price_type == "consumption"
            and region in REGIONS and row_currency == "EUR" and bill_currency == "EUR"
            and isinstance(order, str) and bool(order.strip())
            and amount is not None and tier == 0
            and start is not None and start <= today
            and (not row.get("effectiveEndDate") or (end is not None and end >= today))
            and METERS[name][1] in rname and METERS[name][2] in rname
            and METERS[name][3] in unit
        )
        if not valid:
            item["ambiguous_or_invalid"] += 1
        elif amount == 0:
            item["zero_candidates"] += 1
        else:
            item["positive_candidates"] += 1
    for name, record in result.items():
        if record["ambiguous_or_invalid"]:
            record["classification"] = "UNRESOLVED_SCOPE_OR_RATE_MISMATCH"
        elif record["positive_candidates"] == 1 and record["zero_candidates"] == 0:
            record["classification"] = "ONE_PRIVATE_POSITIVE_CANDIDATE_NEEDS_INDEPENDENT_REVIEW"
        elif record["positive_candidates"] or record["zero_candidates"]:
            record["classification"] = "UNRESOLVED_ZERO_OR_MULTIPLE_TARIFFS"
    all_unique = all(r["classification"] == "ONE_PRIVATE_POSITIVE_CANDIDATE_NEEDS_INDEPENDENT_REVIEW"
                     for r in result.values())
    return {
        "evidence_stage": "PRIVATE_PRICESHEET_CANDIDATES_REQUIRE_INDEPENDENT_VALIDATION"
                          if all_unique and not errors else "BLOCKED_MISSING_OR_AMBIGUOUS_PRIVATE_EVIDENCE",
        "private_source_read": True,
        "scope_binding_self_attested_only": bool(expected_profile),
        "technical_parse_errors": sorted(set(errors)),
        "component_counts": result,
        "numeric_private_rates_exposed": False,
        "billing_agreement_independently_verified": False,
        "account_free_grant_balance_verified": False,
        "tax_inclusive_all_in_quote_verified": False,
        "post_teardown_liability_verified": False,
        "deployment_authorized": False,
        "live_sync_authorized": False,
        "message": "No private rates or identifiers displayed or sent. Even a unique local billing row cannot authorize Azure spend or real-provider synchronization.",
    }


def _read_local_csv(path: Path) -> list[dict]:
    # Restrict read to local, untracked paths outside the working repository.
    actual = path.expanduser().resolve(strict=True)
    if actual == REPO_ROOT or REPO_ROOT in actual.parents:
        raise ValueError("private billing inputs must not be inside the GitHub repository")
    if not actual.is_file() or actual.suffix.lower() != ".csv":
        raise ValueError("expected private local CSV export")
    if actual.stat().st_size > MAX_BYTES:
        raise ValueError("private file too large for bounded local review")
    with actual.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED_FIELDS.issubset(set(reader.fieldnames)):
            raise ValueError("private CSV lacks required MCA pricing schema fields")
        return [row for row in reader if row is not None]


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline local-only sanitized EA billing evidence read")
    parser.add_argument("--input", required=True, help="private MCA price sheet CSV, OUTSIDE git checkout")
    args = parser.parse_args()
    # Private local environment only; never hardcode subscription/profile IDs in repo.
    profile = os.environ.get("EA_PRIVATE_BILLING_PROFILE_ID")
    try:
        rows = _read_local_csv(Path(args.input))
        result = assess_rows(rows, expected_profile=profile, today=date.today())
    except (ValueError, OSError, UnicodeError, csv.Error):
        result = {
            "evidence_stage": "BLOCKED_CANNOT_READ_PRIVATE_BILLING_EVIDENCE",
            "private_source_read": False,
            "component_counts": {},
            "numeric_private_rates_exposed": False,
            "billing_agreement_independently_verified": False,
            "tax_inclusive_all_in_quote_verified": False,
            "deployment_authorized": False,
            "live_sync_authorized": False,
            "message": "Private CSV unavailable, unsuitable, or inside public git checkout; no data emitted.",
        }
    print(json.dumps(result, indent=2))
    return 0 if result["private_source_read"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
