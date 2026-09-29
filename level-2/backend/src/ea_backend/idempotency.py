from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def action_revision(payload: Mapping[str, Any]) -> str:
    """Hash the exact proposed action payload."""
    return sha256_hex(canonical_json(payload))


def idempotency_key(
    *,
    case_id: str,
    action_type: str,
    source_id: str,
    action_revision_value: str,
) -> str:
    raw = "|".join((case_id, action_type, source_id, action_revision_value))
    return f"ea:{sha256_hex(raw)}"


def approval_payload_hash(
    *,
    action_type: str,
    recipients: Sequence[str],
    subject: str,
    body: str,
    attachment_hashes: Sequence[str],
    source_revision: str,
) -> str:
    payload = {
        "action_type": action_type,
        "recipients": sorted(recipients),
        "subject": subject,
        "body": body,
        "attachment_hashes": sorted(attachment_hashes),
        "source_revision": source_revision,
    }
    return sha256_hex(canonical_json(payload))
