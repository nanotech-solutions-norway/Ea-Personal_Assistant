"""Fail-closed offline tests for Azure free-account benefit signals."""
import datetime
import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ea_azure_free_probe", HERE / "azure_free_account_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
NOW = datetime.datetime(2026, 10, 15, tzinfo=datetime.timezone.utc)

class FreeAccountProbeTests(unittest.TestCase):
    def test_unknown_is_not_eligible(self):
        self.assertEqual(probe.classify_billing({}), "INCONCLUSIVE")
        self.assertEqual(probe.classify_free_services({}, NOW), "INCONCLUSIVE")
    def test_free_billing_type_not_proof_of_current_b1ms_allowance(self):
        self.assertEqual(
            probe.classify_billing({"properties":{"subscriptionBillingType":"Free"}}),
            "FREE_BILLING_TYPE_REPORTED_NOT_FREE_SERVICE_PROOF")
    def test_paid_subscription_does_not_disprove_free_allowance(self):
        self.assertEqual(probe.classify_billing({"properties":{"subscriptionBillingType":"Paid"}}),
            "NONFREE_BILLING_TYPE_FREE_SERVICES_STILL_POSSIBLE")
    def test_empty_list_not_proof_of_ineligibility(self):
        self.assertEqual(probe.classify_free_services({"value":[]}, NOW),
            "NO_PG_RECORD_FOUND_NOT_DISPROOF")
    def test_non_pg_record_not_proof(self):
        self.assertEqual(probe.classify_free_services({"value":[{"properties":{
            "displayName":"Service A", "status":"Active", "endAt":"2026-12-31T00:00:00Z"}}]},NOW),
            "NO_PG_RECORD_FOUND_NOT_DISPROOF")
    def test_active_pg_record_only_candidate(self):
        self.assertEqual(probe.classify_free_services({"value":[{"properties":{
            "displayName":"PostgreSQL free service", "status":"Active",
            "endAt":"2026-12-31T00:00:00Z"}}]},NOW),
            "ACTIVE_PG_BENEFIT_RECORD_CANDIDATE")
    def test_expired_pg_record_rejected(self):
        self.assertEqual(probe.classify_free_services({"value":[{"properties":{
            "displayName":"PostgreSQL", "status":"Active",
            "endAt":"2025-12-31T00:00:00Z"}}]},NOW),
            "NO_PG_RECORD_FOUND_NOT_DISPROOF")
    def test_cancelled_pg_record_rejected(self):
        self.assertEqual(probe.classify_free_services({"value":[{"properties":{
            "displayName":"PostgreSQL", "status":"Cancelled"}}]},NOW),
            "NO_PG_RECORD_FOUND_NOT_DISPROOF")
    def test_invalid_date_rejected(self):
        self.assertEqual(probe.classify_free_services({"value":[{"properties":{
            "displayName":"PostgreSQL", "status":"Active","endAt":"bogus"}}]},NOW),
            "NO_PG_RECORD_FOUND_NOT_DISPROOF")
    def test_sensitive_fields_excluded_from_classification(self):
        raw={"properties":{"subscriptionBillingType":"Paid", "billingAccountId":"SECRET_VALUE"}}
        self.assertNotIn("SECRET_VALUE",probe.classify_billing(raw))

if __name__=="__main__":
    unittest.main()
