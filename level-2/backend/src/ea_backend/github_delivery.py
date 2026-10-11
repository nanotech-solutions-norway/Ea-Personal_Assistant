"""GitHub webhook integrity gate for EA staging.

Validate raw signed bytes before parsing JSON. This is a parser, not an
HTTP listener or an authorization to mutate GitHub. Caller must enforce the
app installation allowlist, delivery deduplication and durable audit store.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from typing import Mapping

from .unified_sync import SyncContractError

ALLOWED_EVENTS = frozenset({"issues", "pull_request", "workflow_run"})
MAX_PAYLOAD_BYTES = 1_048_576


@dataclass(frozen=True)
class GitHubDelivery:
    delivery_id: str
    event_type: str
    repository_full_name: str
    action: str | None
    provider_revision: str | None
    installation_id: int | None


def verify_github_delivery(
    *,
    raw_payload: bytes,
    headers: Mapping[str, str],
    webhook_secret: str,
    allowed_repositories: frozenset[str],
    allowed_installation_ids: frozenset[int] | None = None,
) -> GitHubDelivery:
    if not isinstance(raw_payload, bytes) or not 0 < len(raw_payload) <= MAX_PAYLOAD_BYTES:
        raise SyncContractError("Invalid webhook payload size")
    if not isinstance(webhook_secret, str) or not webhook_secret:
        raise SyncContractError("Missing webhook secret")
    if not allowed_repositories:
        raise SyncContractError("No authorized GitHub repositories")
    normalized_headers = {str(k).lower(): v for k, v in headers.items()}
    signature = normalized_headers.get("x-hub-signature-256")
    if not isinstance(signature, str) or not signature.startswith("sha256="):
        raise SyncContractError("Missing GitHub SHA256 signature")
    computed = "sha256=" + hmac.new(
        webhook_secret.encode("utf-8"), raw_payload, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(computed, signature):
        raise SyncContractError("Invalid GitHub webhook signature")

    event = normalized_headers.get("x-github-event")
    delivery_id = normalized_headers.get("x-github-delivery")
    if event not in ALLOWED_EVENTS:
        raise SyncContractError("GitHub event type not allowlisted")
    if not isinstance(delivery_id, str) or not delivery_id.strip() or len(delivery_id) > 128:
        raise SyncContractError("Invalid GitHub delivery ID")
    try:
        payload = json.loads(raw_payload)
    except (ValueError, UnicodeDecodeError) as exc:
        raise SyncContractError("Invalid GitHub webhook JSON") from exc
    if not isinstance(payload, dict):
        raise SyncContractError("Webhook payload must be JSON object")
    repository = payload.get("repository")
    repo_name = repository.get("full_name") if isinstance(repository, dict) else None
    if repo_name not in allowed_repositories:
        raise SyncContractError("GitHub repository not authorized")
    installation = payload.get("installation")
    iid = installation.get("id") if isinstance(installation, dict) else None
    if allowed_installation_ids is not None and iid not in allowed_installation_ids:
        raise SyncContractError("GitHub App installation not authorized")
    if iid is not None and (not isinstance(iid, int) or isinstance(iid, bool)):
        raise SyncContractError("Invalid GitHub installation ID")
    action = payload.get("action")
    if action is not None and not isinstance(action, str):
        raise SyncContractError("Invalid GitHub webhook action")
    # No issue titles, comments, private bodies, or other external content
    # leave the parser. The worker re-reads authoritative records after this.
    item = payload.get(event)
    revision = None
    if isinstance(item, dict):
        updated = item.get("updated_at") or item.get("head_sha")
        if updated is not None:
            revision = str(updated)
    return GitHubDelivery(delivery_id, event, repo_name, action, revision, iid)
