from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping, Any


class EventValidationError(ValueError):
    pass


@dataclass(frozen=True)
class EventEnvelope:
    event_id: str
    source: str
    received_at: str
    cursor: str
    resource_key: str | None
    event_kind: str | None
    metadata: dict[str, Any]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_event_id(*parts: str) -> str:
    raw = "|".join(parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def parse_gmail_pubsub(payload: Mapping[str, Any], *, received_at: str | None = None) -> EventEnvelope:
    message = payload.get("message")
    if not isinstance(message, Mapping):
        raise EventValidationError("missing Pub/Sub message")

    data = message.get("data")
    if not isinstance(data, str) or not data:
        raise EventValidationError("missing Pub/Sub message.data")

    try:
        decoded = base64.b64decode(data, validate=True).decode("utf-8")
        notice = json.loads(decoded)
    except Exception as exc:
        raise EventValidationError("invalid Gmail Pub/Sub data") from exc

    email = notice.get("emailAddress")
    history_id = notice.get("historyId")
    if not isinstance(email, str) or "@" not in email:
        raise EventValidationError("invalid Gmail emailAddress")
    if not isinstance(history_id, str) or not history_id.isdigit():
        raise EventValidationError("invalid Gmail historyId")

    pubsub_id = str(message.get("messageId") or message.get("message_id") or "")
    if not pubsub_id:
        pubsub_id = _stable_event_id(email, history_id)

    published = str(message.get("publishTime") or message.get("publish_time") or "")
    event_id = _stable_event_id("gmail", pubsub_id, email, history_id)

    return EventEnvelope(
        event_id=event_id,
        source="gmail",
        received_at=received_at or _now_iso(),
        cursor=history_id,
        resource_key=email.lower(),
        event_kind="mailbox_history_changed",
        metadata={
            "pubsub_message_id": pubsub_id,
            "publish_time": published or None,
        },
    )


def parse_calendar_headers(headers: Mapping[str, str], *, received_at: str | None = None) -> EventEnvelope:
    normalized = {str(k).lower(): str(v) for k, v in headers.items()}
    channel_id = normalized.get("x-goog-channel-id", "")
    resource_id = normalized.get("x-goog-resource-id", "")
    resource_state = normalized.get("x-goog-resource-state", "")
    message_number = normalized.get("x-goog-message-number", "")

    if not channel_id:
        raise EventValidationError("missing X-Goog-Channel-ID")
    if not resource_id:
        raise EventValidationError("missing X-Goog-Resource-ID")
    if not resource_state:
        raise EventValidationError("missing X-Goog-Resource-State")
    if not message_number.isdigit():
        raise EventValidationError("invalid X-Goog-Message-Number")

    event_id = _stable_event_id(
        "google_calendar",
        channel_id,
        resource_id,
        message_number,
        resource_state,
    )

    return EventEnvelope(
        event_id=event_id,
        source="google_calendar",
        received_at=received_at or _now_iso(),
        cursor=message_number,
        resource_key=resource_id,
        event_kind=resource_state,
        metadata={
            "channel_id": channel_id,
            "resource_id": resource_id,
            "message_number": message_number,
            "resource_state": resource_state,
            "resource_uri": normalized.get("x-goog-resource-uri"),
            "channel_expiration": normalized.get("x-goog-channel-expiration"),
        },
    )
