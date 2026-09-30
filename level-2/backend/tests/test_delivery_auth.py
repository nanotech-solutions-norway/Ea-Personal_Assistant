import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from ea_runtime.auth import GoogleDeliveryAuthenticator


class FakeVerifier:
    production_safe = True

    def __init__(self, claims):
        self.claims = claims
        self.audience = None

    def verify(self, token, *, audience):
        if token == "bad":
            raise ValueError("bad token")
        self.audience = audience
        return dict(self.claims)


class DeliveryAuthTests(unittest.TestCase):
    def auth(self, claims=None):
        verifier = FakeVerifier(claims or {
            "email": "push@example.iam.gserviceaccount.com",
            "email_verified": True,
        })
        return GoogleDeliveryAuthenticator(
            oidc_verifier=verifier,
            gmail_audience="https://ea.example/hooks/gmail",
            gmail_service_account_email="push@example.iam.gserviceaccount.com",
            calendar_channel_token="calendar-secret",
        )

    def test_gmail_verified_identity_allowed(self):
        auth = self.auth()
        self.assertTrue(auth.authorize({
            "HTTP_AUTHORIZATION": "Bearer good"
        }, source="gmail"))

    def test_gmail_wrong_identity_denied(self):
        auth = self.auth({
            "email": "other@example.iam.gserviceaccount.com",
            "email_verified": True,
        })
        self.assertFalse(auth.authorize({
            "HTTP_AUTHORIZATION": "Bearer good"
        }, source="gmail"))

    def test_gmail_unverified_identity_denied(self):
        auth = self.auth({
            "email": "push@example.iam.gserviceaccount.com",
            "email_verified": False,
        })
        self.assertFalse(auth.authorize({
            "HTTP_AUTHORIZATION": "Bearer good"
        }, source="gmail"))

    def test_calendar_channel_token_allowed(self):
        auth = self.auth()
        self.assertTrue(auth.authorize({
            "HTTP_X_GOOG_CHANNEL_TOKEN": "calendar-secret"
        }, source="google_calendar"))

    def test_calendar_wrong_token_denied(self):
        auth = self.auth()
        self.assertFalse(auth.authorize({
            "HTTP_X_GOOG_CHANNEL_TOKEN": "wrong"
        }, source="google_calendar"))

    def test_unknown_source_denied(self):
        self.assertFalse(self.auth().authorize({}, source="unknown"))


if __name__ == "__main__":
    unittest.main()
