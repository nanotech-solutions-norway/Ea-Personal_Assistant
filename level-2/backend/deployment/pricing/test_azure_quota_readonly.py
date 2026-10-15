"""Fail-closed tests for West Europe quota evidence categories."""
import importlib.util
import pathlib
import unittest
P=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location("q",P/"azure_quota_readonly.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class QuotaTests(unittest.TestCase):
    def test_no_data_unknown(self):
        q=m.classify({})
        self.assertEqual(q["quota_api"],"INCONCLUSIVE")
        self.assertEqual(q["burst_family_headroom"],"UNKNOWN")
        self.assertFalse(q["capacity_guaranteed"])
    def test_positive_headroom_not_capacity_proof(self):
        q=m.classify({"value":[
            {"name":{"value":"standardBSFamily"},"limit":10,"currentValue":2},
            {"name":{"value":"cores"},"limit":40,"currentValue":3}]})
        self.assertEqual(q["burst_family_headroom"],"POSITIVE")
        self.assertEqual(q["total_core_headroom"],"POSITIVE")
        self.assertFalse(q["capacity_guaranteed"])
    def test_quota_exhausted(self):
        q=m.classify({"value":[{"name":{"value":"standardBSFamily"},"limit":4,"currentValue":4}]})
        self.assertEqual(q["burst_family_headroom"],"ZERO")
        self.assertEqual(q["total_core_headroom"],"UNKNOWN")
    def test_invalid_payloads_do_not_prove_headroom(self):
        for n in [None,True,-1,2.3,"30"]:
            q=m.classify({"value":[{"name":{"value":"standardBSFamily"},"limit":n,"currentValue":0}]})
            self.assertEqual(q["burst_family_headroom"],"UNKNOWN")
    def test_current_value_exceeds_limit_never_passes(self):
        q=m.classify({"value":[{"name":{"value":"standardBSFamily"},"limit":5,"currentValue":6}]})
        self.assertEqual(q["burst_family_headroom"],"UNKNOWN")

    def test_no_raw_identifiers_echoed(self):
        q=m.classify({"value":[{"name":{"value":"standardBSFamily"},"limit":20,"currentValue":3,
            "subscriptionId":"PRIVATE-SUB-ID"}]})
        self.assertNotIn("PRIVATE",str(q))
if __name__=="__main__":
    unittest.main()
