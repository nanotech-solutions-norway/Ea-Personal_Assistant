"""Adversarial offline MCA evidence tests; no cloud calls or private account data."""
from datetime import date
from pathlib import Path
import csv
import tempfile
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import private_billing_evidence as a

TODAY = date(2026, 10, 15)
PROFILE = "SYNTHETIC-LOCAL-ONLY"

def row(which, *, price="0.001", profile=PROFILE):
    meter, term, _, unit = a.METERS[which]
    return {
        "meterId": meter, "meterName": "Standard vCPU Active Usage" if "cpu" in which else "Standard Memory Active Usage",
        "meterRegion": "EU West", "priceType": "Consumption",
        "tierMinimumUnits": "0", "unitOfMeasure": "1 Second" if "cpu" in which else "1 GiB Second",
        "unitPrice": price, "currency": "EUR", "billingCurrency": "EUR",
        "billingProfileId": profile, "productOrderName": "synthetic-staging-plan",
        "effectiveStartDate": "2026-10-01", "effectiveEndDate": "2026-10-31"
    }

def fixture():
    return [row("aca_cpu_active"), row("aca_memory_active")]

class PrivateEvidenceTests(unittest.TestCase):
    def check(self, data, profile=PROFILE):
        return a.assess_rows(data, expected_profile=profile, today=TODAY)

    def test_two_positive_candidates_never_grant_spend(self):
        r = self.check(fixture())
        self.assertEqual("PRIVATE_PRICESHEET_CANDIDATES_REQUIRE_INDEPENDENT_VALIDATION",r["evidence_stage"])
        self.assertFalse(r["billing_agreement_independently_verified"])
        self.assertFalse(r["numeric_private_rates_exposed"])
        self.assertFalse(r["tax_inclusive_all_in_quote_verified"])
        self.assertFalse(r["deployment_authorized"])
        self.assertFalse(r["live_sync_authorized"])

    def test_missing_or_mismatched_private_profile_blocks(self):
        for profile in (None, "SYNTHETIC-OTHER"):
            r = self.check(fixture(),profile)
            self.assertEqual("BLOCKED_MISSING_OR_AMBIGUOUS_PRIVATE_EVIDENCE",r["evidence_stage"])

    def test_zero_consumption_rate_is_not_free_entitlement(self):
        rows = fixture()
        rows[0]["unitPrice"] = "0"
        r = self.check(rows)
        self.assertEqual("UNRESOLVED_ZERO_OR_MULTIPLE_TARIFFS",r["component_counts"]["aca_cpu_active"]["classification"])
        self.assertFalse(r["account_free_grant_balance_verified"])

    def test_multiple_positive_candidates_not_one_billing_tariff(self):
        rows = fixture()
        rows.append(row("aca_cpu_active",price="0.0001"))
        r = self.check(rows)
        self.assertEqual("BLOCKED_MISSING_OR_AMBIGUOUS_PRIVATE_EVIDENCE",r["evidence_stage"])

    def test_wrong_region_product_context_currency_and_tier_rejected(self):
        for key,val in [
            ("meterRegion","eastus"),("priceType","SavingsPlan"),("tierMinimumUnits","1000000"),
            ("unitOfMeasure","1GB"),("currency","USD"),("billingCurrency","USD"),
            ("productOrderName",""),("effectiveStartDate","2026-12-01"),
            ("effectiveEndDate","2026-09-30"),("meterName","Different Tier")
        ]:
            rows=fixture()
            rows[0][key]=val
            self.assertEqual("BLOCKED_MISSING_OR_AMBIGUOUS_PRIVATE_EVIDENCE",
                             self.check(rows)["evidence_stage"],key)

    def test_reject_nonfinite_negative_invalid_amounts(self):
        for v in (None, "NaN", "Infinity", "-0.1", True, "not-a-rate"):
            rows=fixture()
            rows[0]["unitPrice"]=v
            self.assertEqual("BLOCKED_MISSING_OR_AMBIGUOUS_PRIVATE_EVIDENCE",self.check(rows)["evidence_stage"],v)

    def test_required_fields_absent_and_repo_storage_forbidden(self):
        self.assertTrue(a.REQUIRED_FIELDS.issubset(set(fixture()[0])))
        self.assertEqual("BLOCKED_MISSING_OR_AMBIGUOUS_PRIVATE_EVIDENCE",
                         self.check(fixture()[:1])["evidence_stage"])
        with self.assertRaises(ValueError):
            a._read_local_csv(Path(__file__).resolve())

    def test_private_local_csv_read_without_logging_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/"private.csv"
            with file.open("w",encoding="utf-8",newline="") as f:
                writer=csv.DictWriter(f,fieldnames=list(fixture()[0]))
                writer.writeheader()
                writer.writerows(fixture())
            rows=a._read_local_csv(file)
            report=self.check(rows)
            self.assertEqual("PRIVATE_PRICESHEET_CANDIDATES_REQUIRE_INDEPENDENT_VALIDATION",report["evidence_stage"])
            self.assertNotIn(PROFILE,str(report))
            self.assertNotIn("0.001",str(report))
            self.assertNotIn(str(file),str(report))

    def test_reject_invalid_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"incomplete.csv"
            path.write_text("unitPrice\n0.001\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                a._read_local_csv(path)

if __name__=="__main__":
    unittest.main()
