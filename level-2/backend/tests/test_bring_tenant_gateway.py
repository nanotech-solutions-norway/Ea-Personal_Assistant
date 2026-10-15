"""Deterministic positive + adversarial tenant-isolation tests (synthetic only)."""

import pathlib
import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.bring_tenant_gateway import (
    BOOKING_EVIDENCE,
    READ_SCOPE,
    BringAuthorizationDenied,
    PrincipalGrant,
    ReadGateConfig,
    ShipmentProvenance,
    TenantAccount,
    VerifiedIdentity,
    authorize_tracking_read,
)

NOW = datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc)
TENANT_A = "tenant-synthetic-a"
TENANT_B = "tenant-synthetic-b"
TRACK_A = "ABC123456789"
TRACK_B = "XYZ987654321"
CUSTOMER_A = "999111222"
CUSTOMER_B = "111999888"
ISSUER = "https://idp.example.invalid/"
AUDIENCE = "api://ea-synthetic"
KEY_A = "https://ea-vault-example.vault.azure.net/secrets/bring-synthetic-a"
KEY_B = "https://ea-vault-example.vault.azure.net/secrets/bring-synthetic-b"


class StubVerifier:
    """Offline stub only; production code MUST inject a cryptographic verifier."""

    production_safe = True

    def verify(self, bearer_token, *, expected_audience):
        if bearer_token == "actor-a":
            return VerifiedIdentity(ISSUER, "subject-a", AUDIENCE, NOW + timedelta(hours=1))
        if bearer_token == "actor-b":
            return VerifiedIdentity(ISSUER, "subject-b", AUDIENCE, NOW + timedelta(hours=1))
        if bearer_token == "expired":
            return VerifiedIdentity(ISSUER, "subject-a", AUDIENCE, NOW - timedelta(minutes=1))
        if bearer_token == "wrong-issuer":
            return VerifiedIdentity("https://evil.invalid/", "subject-a", AUDIENCE, NOW + timedelta(hours=1))
        if bearer_token == "wrong-audience":
            return VerifiedIdentity(ISSUER, "subject-a", "api://wrong", NOW + timedelta(hours=1))
        raise ValueError("invalid synthetic bearer token")


class StubRegistry:
    """Trusted repository stand-in; all IDs are artificial."""

    production_safe = True

    def __init__(self):
        self.grants = {
            "subject-a": PrincipalGrant(ISSUER, "subject-a", TENANT_A, READ_SCOPE, CUSTOMER_A, active=True),
            "subject-b": PrincipalGrant(ISSUER, "subject-b", TENANT_B, READ_SCOPE, CUSTOMER_B, active=True),
        }
        self.accounts = {
            TENANT_A: TenantAccount(TENANT_A, CUSTOMER_A, KEY_A, active=True),
            TENANT_B: TenantAccount(TENANT_B, CUSTOMER_B, KEY_B, active=True),
        }
        self.shipments = {
            (TENANT_A, TRACK_A): ShipmentProvenance(
                TENANT_A, TRACK_A, CUSTOMER_A, BOOKING_EVIDENCE,
                NOW - timedelta(days=2), independently_approved=True
            ),
            (TENANT_B, TRACK_B): ShipmentProvenance(
                TENANT_B, TRACK_B, CUSTOMER_B, BOOKING_EVIDENCE,
                NOW - timedelta(days=2), independently_approved=True
            ),
        }

    def principal_grant(self, issuer, subject):
        grant = self.grants.get(subject)
        return grant if grant and grant.issuer == issuer else None

    def tenant_account(self, tenant_scope):
        return self.accounts.get(tenant_scope)

    def shipment_provenance(self, tenant_scope, tracking_reference):
        return self.shipments.get((tenant_scope, tracking_reference))


class BringTenantGatewayTests(unittest.TestCase):
    def setUp(self):
        self.verifier = StubVerifier()
        self.registry = StubRegistry()
        self.config = ReadGateConfig(issuer=ISSUER, audience=AUDIENCE, enabled=True)

    def check(self, *, token="actor-a", tenant=TENANT_A, reference=TRACK_A, config=None,
              verifier=None, registry=None):
        return authorize_tracking_read(
            bearer_token=token,
            requested_tenant=tenant,
            tracking_reference=reference,
            config=self.config if config is None else config,
            verifier=self.verifier if verifier is None else verifier,
            registry=self.registry if registry is None else registry,
            now=NOW,
        )

    def denied(self, reason, **kwargs):
        with self.assertRaises(BringAuthorizationDenied) as error:
            self.check(**kwargs)
        self.assertEqual(error.exception.reason, reason)

    def test_known_account_and_provenance_allow_read_only_scope(self):
        permit = self.check()
        self.assertEqual(permit.tenant_scope, TENANT_A)
        self.assertEqual(permit.tracking_reference, TRACK_A)
        self.assertEqual(permit.credential_ref, KEY_A)
        self.assertTrue(permit.read_only)

    def test_second_synthetic_tenant_can_only_read_own_shipment(self):
        self.assertEqual(self.check(token="actor-b", tenant=TENANT_B, reference=TRACK_B).credential_ref, KEY_B)

    def test_default_is_disabled(self):
        self.denied("FEATURE_DISABLED", config=ReadGateConfig(ISSUER, AUDIENCE))

    def test_missing_bearer_token(self):
        self.denied("IDENTITY_UNVERIFIED", token="")

    def test_forged_bearer_token(self):
        self.denied("IDENTITY_UNVERIFIED", token="forged-actor-a")

    def test_expired_token(self):
        self.denied("IDENTITY_UNVERIFIED", token="expired")

    def test_wrong_identity_issuer(self):
        self.denied("IDENTITY_UNVERIFIED", token="wrong-issuer")

    def test_wrong_identity_audience(self):
        self.denied("IDENTITY_UNVERIFIED", token="wrong-audience")

    def test_cross_tenant_actor_a_cannot_read_b(self):
        self.denied("TENANT_ACCESS_DENIED", token="actor-a", tenant=TENANT_B, reference=TRACK_B)

    def test_cross_tenant_actor_b_cannot_read_a(self):
        self.denied("TENANT_ACCESS_DENIED", token="actor-b", tenant=TENANT_A, reference=TRACK_A)

    def test_valid_actor_cannot_read_unknown_shipment_even_with_public_tracking(self):
        self.denied("SHIPMENT_PROVENANCE_UNVERIFIED", reference=TRACK_B)

    def test_revoked_principal_is_denied(self):
        self.registry.grants["subject-a"] = replace(self.registry.grants["subject-a"], active=False)
        self.denied("TENANT_ACCESS_DENIED")

    def test_wrong_permission_denied(self):
        self.registry.grants["subject-a"] = replace(
            self.registry.grants["subject-a"], permission="bring.shipment.book"
        )
        self.denied("TENANT_ACCESS_DENIED")

    def test_customer_mismatch_denied(self):
        self.registry.grants["subject-a"] = replace(
            self.registry.grants["subject-a"], customer_number=CUSTOMER_B
        )
        self.denied("ACCOUNT_BINDING_UNVERIFIED")

    def test_tenant_disabled_denied(self):
        self.registry.accounts[TENANT_A] = replace(self.registry.accounts[TENANT_A], active=False)
        self.denied("ACCOUNT_BINDING_UNVERIFIED")

    def test_untrusted_secret_reference_denied(self):
        self.registry.accounts[TENANT_A] = replace(
            self.registry.accounts[TENANT_A], vault_secret_ref="https://example.invalid/secret"
        )
        self.denied("ACCOUNT_BINDING_UNVERIFIED")

    def test_provenance_does_not_match_company(self):
        self.registry.shipments[TENANT_A, TRACK_A] = replace(
            self.registry.shipments[TENANT_A, TRACK_A], customer_number=CUSTOMER_B
        )
        self.denied("SHIPMENT_PROVENANCE_UNVERIFIED")

    def test_unapproved_screenshot_is_not_provenance(self):
        self.registry.shipments[TENANT_A, TRACK_A] = replace(
            self.registry.shipments[TENANT_A, TRACK_A],
            evidence_source="operator_screenshot", independently_approved=True
        )
        self.denied("SHIPMENT_PROVENANCE_UNVERIFIED")

    def test_approval_flag_required(self):
        self.registry.shipments[TENANT_A, TRACK_A] = replace(
            self.registry.shipments[TENANT_A, TRACK_A], independently_approved=False
        )
        self.denied("SHIPMENT_PROVENANCE_UNVERIFIED")

    def test_stale_booking_evidence_denied(self):
        self.registry.shipments[TENANT_A, TRACK_A] = replace(
            self.registry.shipments[TENANT_A, TRACK_A], reviewed_at=NOW - timedelta(days=32)
        )
        self.denied("SHIPMENT_EVIDENCE_STALE")

    def test_future_booking_evidence_denied(self):
        self.registry.shipments[TENANT_A, TRACK_A] = replace(
            self.registry.shipments[TENANT_A, TRACK_A], reviewed_at=NOW + timedelta(minutes=1)
        )
        self.denied("SHIPMENT_EVIDENCE_STALE")

    def test_unsafe_verifier_denied(self):
        class UntrustedVerifier(StubVerifier):
            production_safe = False
        self.denied("TRUSTED_COMPONENT_UNAVAILABLE", verifier=UntrustedVerifier())

    def test_unsafe_registry_denied(self):
        class UntrustedRegistry(StubRegistry):
            production_safe = False
        self.denied("TRUSTED_COMPONENT_UNAVAILABLE", registry=UntrustedRegistry())

    def test_invalid_config_denied(self):
        self.denied("TRUSTED_COMPONENT_UNAVAILABLE",
                    config=ReadGateConfig(ISSUER, AUDIENCE, enabled=True, maximum_evidence_age_days=999))

    def test_reject_query_injection(self):
        self.denied("INVALID_TRACKING_REFERENCE", reference="ABC123456789&lang=no")


if __name__ == "__main__":
    unittest.main()
