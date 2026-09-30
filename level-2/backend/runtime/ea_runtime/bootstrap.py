from __future__ import annotations

from typing import Mapping

from .auth import GoogleDeliveryAuthenticator
from .google_auth import GoogleAuthOidcVerifier
from .postgres_store import PostgresEventStore


def build_components(env: Mapping[str, str]):
    store = PostgresEventStore.from_dsn(env["DATABASE_URL"])
    authenticator = GoogleDeliveryAuthenticator(
        oidc_verifier=GoogleAuthOidcVerifier(),
        gmail_audience=env["GMAIL_PUSH_AUDIENCE"],
        gmail_service_account_email=env["GMAIL_PUSH_SERVICE_ACCOUNT_EMAIL"],
        calendar_channel_token=env["CALENDAR_CHANNEL_TOKEN"],
    )
    return store, authenticator
