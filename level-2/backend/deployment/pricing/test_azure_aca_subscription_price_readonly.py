"""Synthetic-only test cases for subscription price-sheet readback."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import azure_aca_subscription_price_readonly as mod

SUB = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"

def row(name, rate, incl=0):
    return {
        "meterId": mod.METER_IDS[name], "currencyCode": "EUR",
        "unitOfMeasure": next(iter(mod.UNIT_EXPECTED[name])),
        "unitPrice": rate, "includedQuantity": incl,
        "offerId": "NOT_PRINTED", "billingPeriodId": "/private/billing"
    }

def page(items, next_link=None):
    return {"properties": {"pricesheets": items, "nextLink": next_link}}


class PriceSheetPrivacyTests(unittest.TestCase):
    def test_read_sanitized_candidate_rates(self):
        p = page([row("ACA_ACTIVE_VCPU_SECOND", 0.000024),
                  row("ACA_ACTIVE_GIB_SECOND", 0.000003),
                  row("ACA_HTTP_REQUESTS_MILLION", 0.4928)])
        result = mod.read_private_pricesheet(SUB, fetcher=lambda url: p)
        self.assertEqual(result["status"], "ACCOUNT_PRICE_SHEET_READ_BUT_NOT_DEPLOYMENT_APPROVAL")
        self.assertEqual(result["rates"]["ACA_ACTIVE_VCPU_SECOND"]["eur_per_unit"], "0.000024")
        self.assertNotIn("NOT_PRINTED", str(result))
        self.assertNotIn("/private/billing", str(result))
        self.assertEqual(result["pages_read"], 1)

    def test_zero_price_is_not_proof_of_free_usage(self):
        out = mod.extract_allowlisted_prices([page([row("ACA_ACTIVE_GIB_SECOND", 0)])])
        self.assertEqual(out["rates"]["ACA_ACTIVE_GIB_SECOND"]["status"],
                         "ACCOUNT_PRICE_CANDIDATE_ZERO_NOT_PROOF_FREE")

    def test_wrong_currency_or_unit_not_accepted(self):
        invalid = row("ACA_ACTIVE_VCPU_SECOND", 0.1)
        invalid["currencyCode"] = "USD"
        other = row("ACA_ACTIVE_VCPU_SECOND", 0.1)
        other["unitOfMeasure"] = "1 Hour"
        out = mod.extract_allowlisted_prices([page([invalid, other])])
        self.assertEqual(out["rates"]["ACA_ACTIVE_VCPU_SECOND"]["status"], "NOT_RETURNED")

    def test_duplicate_tiers_fail_ambiguously(self):
        out = mod.extract_allowlisted_prices([page([
            row("ACA_ACTIVE_VCPU_SECOND", 0.000024),
            row("ACA_ACTIVE_VCPU_SECOND", 0.000012)])])
        self.assertEqual(out["rates"]["ACA_ACTIVE_VCPU_SECOND"]["status"],
                         "AMBIGUOUS_MULTIPLE_PRICE_SHEET_TIERS")

    def test_reject_wrong_host_before_credentialled_get(self):
        evil = page([row("ACA_ACTIVE_VCPU_SECOND", 0.000024)],
                    next_link="https://not-azure.invalid/collect?api-version=2024-08-01")
        seen = []
        def fetch(url):
            seen.append(url)
            return evil
        result = mod.read_private_pricesheet(SUB, fetch)
        self.assertEqual(result["status"], "BLOCKED_UNTRUSTED_NEXT_LINK")
        self.assertEqual(len(seen), 1)

    def test_reject_cross_subscription_next_page(self):
        other_sub = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
        url = (f"https://management.azure.com/subscriptions/{other_sub}/providers/"
               "Microsoft.Consumption/pricesheets/default?api-version=2024-08-01")
        out = mod.read_private_pricesheet(SUB, fetcher=lambda _: page([], url))
        self.assertEqual(out["status"], "BLOCKED_UNTRUSTED_NEXT_LINK")

    def test_allowlisted_azure_errors_never_expose_private_data(self):
        cases = {
            "AuthorizationFailed": "AUTHORIZATION_FAILED",
            "ResourceNotFound": "RESOURCE_NOT_FOUND",
            "InvalidApiVersionParameter": "UNSUPPORTED_API_VERSION",
            "NoRegisteredProviderFound": "PROVIDER_NOT_AVAILABLE",
            "Forbidden": "FORBIDDEN",
            "FeatureNotSupported": "FEATURE_NOT_SUPPORTED",
        }
        for raw_code, status in cases.items():
            with self.subTest(raw_code=raw_code):
                message = f"ERROR: ({raw_code}) secret=FAKE_TOKEN subscription={SUB}"
                result = mod.classify_azure_cli_failure(message)
                self.assertEqual(result, status)
                self.assertNotIn(SUB, result)
                self.assertNotIn("FAKE_TOKEN", result)
                probe = mod.read_private_pricesheet(
                    SUB,
                    fetcher=lambda _: {"_ea_safe_error": result},
                )
                self.assertEqual(probe["status"], status)
                self.assertEqual(probe["rates"], {})
                self.assertNotIn(SUB, str(probe))

    def test_unknown_errors_are_not_forwarded(self):
        error = "ERROR: (UnexpectedSensitiveData) token=FAKE_TOKEN"
        self.assertEqual(
            mod.classify_azure_cli_failure(error),
            "UNAVAILABLE_OR_UNAUTHORIZED",
        )
        self.assertEqual(
            mod.classify_azure_cli_failure("HTTP Error 403: hidden URI"),
            "HTTP_403",
        )

    def test_auth_failure_reports_no_identifiers(self):
        out = mod.read_private_pricesheet(SUB, fetcher=lambda _: None)
        self.assertEqual(out["status"], "UNAVAILABLE_OR_UNAUTHORIZED")
        self.assertNotIn(SUB, str(out))

    def test_invalid_identifiers_skip_all_calls(self):
        def unsafe(url):
            raise AssertionError("should never call")
        out = mod.read_private_pricesheet("invalid-sub", fetcher=unsafe)
        self.assertEqual(out["status"], "BLOCKED_INVALID_SUBSCRIPTION_CONFIG")

    def test_incomplete_pagination_fails_closed(self):
        def fetch(url):
            return page([], next_link=url)
        result = mod.read_private_pricesheet(SUB, fetch)
        self.assertEqual(result["status"], "INCOMPLETE_PAGINATION")
        self.assertEqual(result["rates"], {})

    def test_malformed_page_fails_closed(self):
        result = mod.read_private_pricesheet(SUB, fetcher=lambda _: {"properties": {"not-price-sheets": []}})
        self.assertEqual(result["status"], "MALFORMED_RESPONSE")

    def test_url_escaping_does_not_permit_credentials_or_non_azure(self):
        for url in (
            "https://user:password@management.azure.com/subscriptions/" + SUB
            + "/providers/Microsoft.Consumption/pricesheets/default?api-version=2024-08-01",
            "https://management.azure.com.evil.invalid/subscriptions/" + SUB
            + "/providers/Microsoft.Consumption/pricesheets/default?api-version=2024-08-01",
            "http://management.azure.com/subscriptions/" + SUB
            + "/providers/Microsoft.Consumption/pricesheets/default?api-version=2024-08-01",
        ):
            self.assertFalse(mod.safe_next_url(url, SUB))


if __name__ == "__main__":
    unittest.main()
