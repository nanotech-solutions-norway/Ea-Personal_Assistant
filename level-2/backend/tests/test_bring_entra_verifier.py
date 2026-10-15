"""Offline Entra JWT tests: ephemeral RSA signer and mocked fixed-URL JWKS.

No tokens, keys or user identifiers from a real Entra tenant are used.
"""

import json
import pathlib
import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

from ea_backend.entra_access_token import EntraAccessTokenVerifier

TENANT = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
CLIENT = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
OTHER_CLIENT = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
OID = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
AUDIENCE = "api://ea-bring-synthetic"
ISSUER = f"https://login.microsoftonline.com/{TENANT}/v2.0"
JWKS = f"https://login.microsoftonline.com/{TENANT}/discovery/v2.0/keys"
NOW = datetime.now(timezone.utc)


class EntraAccessTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        key = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(cls.private_key.public_key()))
        key.update({"kid": "synthetic-key-1", "use": "sig", "issuer": ISSUER})
        cls.jwks = {"keys": [key]}

    def setUp(self):
        self.patcher = patch("jwt.PyJWKClient.fetch_data", return_value=self.jwks)
        self.mock_fetch = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.verifier = EntraAccessTokenVerifier(
            tenant_id=TENANT, api_audience=AUDIENCE,
            authorized_client_ids=(CLIENT,)
        )

    def token(self, *, key=None, algorithm="RS256", **overrides):
        claims = {
            "iss": ISSUER, "aud": AUDIENCE,
            "exp": int((NOW + timedelta(hours=1)).timestamp()),
            "nbf": int((NOW - timedelta(minutes=1)).timestamp()),
            "iat": int((NOW - timedelta(minutes=1)).timestamp()),
            "tid": TENANT, "oid": OID, "azp": CLIENT,
            "ver": "2.0", "scp": "bring.tracking.read",
            "sub": "synthetic-pairwise-subject",
        }
        claims.update(overrides)
        return jwt.encode(
            claims,
            key if key is not None else self.private_key,
            algorithm=algorithm,
            headers={"kid": "synthetic-key-1"},
        )

    def verify(self, token, audience=AUDIENCE):
        return self.verifier.verify(token, expected_audience=audience)

    def test_valid_signed_delegated_token(self):
        result = self.verify(self.token())
        self.assertEqual(result.subject, OID)
        self.assertEqual(result.issuer, ISSUER)
        self.assertEqual(result.audience, AUDIENCE)
        self.assertGreater(result.expires_at, NOW)
        self.mock_fetch.assert_called_once_with()
        self.assertEqual(self.verifier.jwks_url, JWKS)

    def test_bad_signature_denied(self):
        adversary_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with self.assertRaises(ValueError):
            self.verify(self.token(key=adversary_key))

    def test_wrong_issuer_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(iss="https://login.microsoftonline.com/evil/v2.0"))

    def test_wrong_audience_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(aud="api://other"))

    def test_expected_audience_cannot_be_selected_per_request(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(), audience="api://other")

    def test_expired_token_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(exp=int((NOW - timedelta(minutes=1)).timestamp())))

    def test_future_not_before_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(nbf=int((NOW + timedelta(minutes=1)).timestamp())))

    def test_future_issued_at_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(iat=int((NOW + timedelta(minutes=1)).timestamp())))

    def test_wrong_tenant_claim_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(tid=OTHER_CLIENT))

    def test_wrong_azp_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(azp=OTHER_CLIENT))

    def test_missing_delegated_scope_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(scp="User.Read"))

    def test_roles_only_app_token_denied(self):
        claims = {"scp": None, "roles": ["bring.tracking.read"]}
        with self.assertRaises(ValueError):
            self.verify(self.token(**claims))

    def test_wrong_version_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(ver="1.0"))

    def test_missing_oid_denied(self):
        with self.assertRaises(ValueError):
            self.verify(self.token(oid=None))

    def test_unsigned_or_wrong_algorithm_denied(self):
        token = jwt.encode(
            {"aud": AUDIENCE}, key="", algorithm="none",
            headers={"kid": "synthetic-key-1"}
        )
        with self.assertRaises(ValueError):
            self.verify(token)

    def test_signing_key_wrong_issuer_denied(self):
        altered = json.loads(json.dumps(self.jwks))
        altered["keys"][0]["issuer"] = "https://login.microsoftonline.com/other/v2.0"
        self.mock_fetch.return_value = altered
        with self.assertRaises(ValueError):
            self.verify(self.token())

    def test_unknown_signing_key_denied(self):
        self.mock_fetch.return_value = {"keys": []}
        with self.assertRaises(ValueError):
            self.verify(self.token())

    def test_not_accepting_common_or_custom_authority(self):
        with self.assertRaises(ValueError):
            EntraAccessTokenVerifier(
                tenant_id="common", api_audience=AUDIENCE,
                authorized_client_ids=(CLIENT,)
            )

    def test_missing_allowed_clients_denied(self):
        with self.assertRaises(ValueError):
            EntraAccessTokenVerifier(
                tenant_id=TENANT, api_audience=AUDIENCE,
                authorized_client_ids=()
            )

    def test_wrong_key_type_denied(self):
        self.mock_fetch.return_value = {
            "keys": [{"kty": "oct", "k": "c3ludGhldGlj", "kid": "synthetic-key-1"}]
        }
        with self.assertRaises(ValueError):
            self.verify(self.token())


if __name__ == "__main__":
    unittest.main()
