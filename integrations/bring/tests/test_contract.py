"""Synthetic tests. Never load Mybring secrets or call the network."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_customer_info import customer_count, valid_client_url


class CustomerInfoContractTests(unittest.TestCase):
    def test_valid_customer_response(self):
        self.assertEqual(customer_count(b'{"customers":[{"name":"synthetic"}]}'), 1)

    def test_empty_customer_list(self):
        self.assertEqual(customer_count(b'{"customers":[]}'), 0)

    def test_missing_customers_rejected(self):
        with self.assertRaises(ValueError):
            customer_count(b'{"other":[]}')

    def test_malformed_json_rejected(self):
        with self.assertRaises(ValueError):
            customer_count(b'not json')

    def test_nonobject_customer_rejected(self):
        with self.assertRaises(ValueError):
            customer_count(b'{"customers":[42]}')

    def test_github_https_url_allowed(self):
        self.assertTrue(valid_client_url(
            "https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant"
        ))

    def test_insecure_and_userinfo_urls_rejected(self):
        self.assertFalse(valid_client_url("http://github.com/example"))
        self.assertFalse(valid_client_url("https://user:pass@example.com/"))
        self.assertFalse(valid_client_url("https://example.com/" + chr(13) + chr(10) + "X-Foo:bar"))


if __name__ == "__main__":
    unittest.main()
