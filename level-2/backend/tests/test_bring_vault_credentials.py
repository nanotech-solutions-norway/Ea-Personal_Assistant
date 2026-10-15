"""No-live-secrets test suite for scoped Bring Key Vault access."""

import json
import pathlib
import sys
import unittest
from types import SimpleNamespace

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.bring_tenant_gateway import ScopedTrackingPermit
from ea_backend.bring_vault_credentials import (
    AzureManagedIdentitySecretClientFactory,
    BringCredentialUnavailable,
    ScopedBringVaultResolver,
)

VAULT_A = "https://synthetic-ea-a.vault.azure.net"
VAULT_B = "https://synthetic-ea-b.vault.azure.net"
A_REF = VAULT_A + "/secrets/company-a"
B_REF = VAULT_B + "/secrets/company-b"
API_UID = "synthetic-user"
API_KEY = "synthetic-test-key"
CLIENT_URL = "https://synthetic.example.invalid/ea"


class FakeClient:
    def __init__(self, secret):
        self.secret = secret
        self.calls = []

    def get_secret(self, name):
        self.calls.append(name)
        return SimpleNamespace(value=self.secret)


class VaultCredentialsTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient(json.dumps({
            "api_uid": API_UID, "api_key": API_KEY, "client_url": CLIENT_URL
        }))
        self.selected = []
        def factory(url):
            self.selected.append(url)
            return self.client
        self.resolver = ScopedBringVaultResolver(
            approved_vault_urls=frozenset({VAULT_A}),
            client_factory=factory,
        )

    def permit(self, *, ref=A_REF, tenant="synthetic-a", read_only=True):
        return ScopedTrackingPermit(
            tenant_scope=tenant,
            tracking_reference="FAKEPACKAGE123456",
            credential_ref=ref,
            read_only=read_only,
        )

    def test_authorized_read_fetches_only_named_secret(self):
        creds = self.resolver.resolve(self.permit())
        self.assertEqual(self.selected, [VAULT_A])
        self.assertEqual(self.client.calls, ["company-a"])
        self.assertEqual(creds.api_uid, API_UID)
        self.assertEqual(creds.api_key, API_KEY)
        self.assertEqual(creds.client_url, CLIENT_URL)

    def test_deny_other_tenant_vault_before_io(self):
        with self.assertRaises(BringCredentialUnavailable):
            self.resolver.resolve(self.permit(ref=B_REF, tenant="synthetic-b"))
        self.assertEqual(self.selected, [])

    def test_deny_outside_vault_host_and_query(self):
        for ref in (
            "https://malicious.invalid/secrets/company-a",
            A_REF + "?version=1",
            A_REF + "/other",
            A_REF.replace(".vault.azure.net", ".vault.azure.net.evil.invalid"),
            A_REF.replace("https://", "http://"),
        ):
            with self.subTest(ref=ref):
                with self.assertRaises(BringCredentialUnavailable):
                    self.resolver.resolve(self.permit(ref=ref))
        self.assertEqual(self.selected, [])

    def test_deny_mutating_permit(self):
        with self.assertRaises(BringCredentialUnavailable):
            self.resolver.resolve(self.permit(read_only=False))
        self.assertEqual(self.selected, [])

    def test_deny_missing_or_forged_permit(self):
        with self.assertRaises(BringCredentialUnavailable):
            self.resolver.resolve({"credential_ref": A_REF})
        self.assertEqual(self.selected, [])

    def test_missing_or_invalid_secret_format_fails_closed(self):
        for doc in (
            "not-json",
            "{}",
            '{"api_uid":"u","api_key":"k","client_url":"http://untrusted.invalid"}',
            '{"api_uid":"u","api_key":"k","client_url":"https://example.invalid/?t=1"}',
            '{"api_uid":"u","api_key":"a\\nb","client_url":"https://example.invalid/"}',
            '{"api_uid":"u","api_key":"k","client_url":"https://example.invalid/", "extra":"yes"}',
        ):
            with self.subTest(doc=doc[:16]):
                self.client.secret = doc
                with self.assertRaises(BringCredentialUnavailable):
                    self.resolver.resolve(self.permit())

    def test_secret_value_does_not_appear_in_repr_or_error(self):
        creds = self.resolver.resolve(self.permit())
        self.assertNotIn(API_KEY, repr(creds))
        self.client.secret = "malformed"
        try:
            self.resolver.resolve(self.permit())
        except BringCredentialUnavailable as error:
            self.assertNotIn(API_KEY, str(error))
            self.assertNotIn(A_REF, str(error))
        else:
            self.fail("Malformed secret accepted")

    def test_azure_client_errors_are_sanitized(self):
        def malicious_error(_):
            raise RuntimeError("key=" + API_KEY + " ref=" + A_REF)
        resolver = ScopedBringVaultResolver(
            approved_vault_urls=frozenset({VAULT_A}),
            client_factory=malicious_error,
        )
        with self.assertRaises(BringCredentialUnavailable) as error:
            resolver.resolve(self.permit())
        self.assertEqual(str(error.exception), "BRING_CREDENTIAL_UNAVAILABLE")

    def test_provisioning_requires_allowlist(self):
        with self.assertRaises(ValueError):
            ScopedBringVaultResolver(
                approved_vault_urls=frozenset(), client_factory=lambda url: self.client
            )
        with self.assertRaises(ValueError):
            ScopedBringVaultResolver(
                approved_vault_urls=frozenset({"https://evil.invalid"}),
                client_factory=lambda url: self.client,
            )

    def test_managed_identity_requires_valid_guid(self):
        with self.assertRaises(ValueError):
            AzureManagedIdentitySecretClientFactory(managed_identity_client_id="not-a-guid")
        # Constructor does NOT request Azure credentials or any secret.
        factory = AzureManagedIdentitySecretClientFactory(
            managed_identity_client_id="aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        )
        self.assertTrue(callable(factory))


if __name__ == "__main__":
    unittest.main()
