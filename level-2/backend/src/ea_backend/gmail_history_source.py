"""Read-only Gmail users.history.list collector for bounded EA staging.

A successful result identifies dirty Gmail threads; it does not authorize a
draft or infer a thread's current business state. Re-fetch every current
thread with approved credentials before acting, then atomically persist the
resulting projection and returned mailbox historyId. No OAuth in this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .unified_sync import SyncContractError

HISTORY_POINTER_FIELDS = ("messagesAdded", "messagesDeleted", "labelsAdded", "labelsRemoved")


class GmailHistoryExpired(SyncContractError):
    """Gmail 404: historyId invalid or expired; perform separate full sync."""


@dataclass(frozen=True)
class GmailHistoryObservation:
    dirty_thread_ids: tuple[str, ...]
    next_history_id: str
    pages_fetched: int


def collect_gmail_history(
    *,
    start_history_id: str,
    list_history: Callable[[dict[str, str]], Mapping[str, Any]],
    max_pages: int = 100,
    max_threads: int = 10000,
) -> GmailHistoryObservation:
    """Complete a mailbox history scan or fail without returning a cursor."""
    if not isinstance(start_history_id, str) or not start_history_id.isdigit():
        raise SyncContractError("Invalid startHistoryId")
    if not 1 <= max_pages <= 1000 or not 1 <= max_threads <= 100000:
        raise SyncContractError("Invalid history limits")
    token: str | None = None
    seen: set[str] = set()
    dirty: set[str] = set()
    for page in range(1, max_pages + 1):
        query = {"userId": "me", "startHistoryId": start_history_id, "maxResults": "500"}
        if token:
            query["pageToken"] = token
        response = list_history(query)
        if not isinstance(response, dict):
            raise SyncContractError("Invalid history response")
        changes = response.get("history", [])
        if not isinstance(changes, list):
            raise SyncContractError("History entries must be a list")
        for entry in changes:
            if not isinstance(entry, dict) or not str(entry.get("id", "")).isdigit():
                raise SyncContractError("History entry missing valid historyId")
            # messages is a summary that may duplicate messagesAdded. Deduplicate.
            for msg in entry.get("messages", []):
                if not isinstance(msg, dict) or not isinstance(msg.get("threadId"), str):
                    raise SyncContractError("History message missing threadId")
                dirty.add(msg["threadId"])
            for field in HISTORY_POINTER_FIELDS:
                pointers = entry.get(field, [])
                if not isinstance(pointers, list):
                    raise SyncContractError("Invalid Gmail change list")
                for ptr in pointers:
                    if not isinstance(ptr, dict) or not isinstance(ptr.get("message"), dict):
                        raise SyncContractError("Invalid Gmail change message")
                    tid = ptr["message"].get("threadId")
                    if not isinstance(tid, str) or not tid.strip():
                        raise SyncContractError("Missing changed threadId")
                    dirty.add(tid)
            if len(dirty) > max_threads:
                raise SyncContractError("Gmail thread cap exceeded")
        continuation = response.get("nextPageToken")
        if continuation is None:
            cursor = response.get("historyId")
            if not isinstance(cursor, str) or not cursor.isdigit():
                raise SyncContractError("Missing terminal mailbox historyId")
            if int(cursor) < int(start_history_id):
                raise SyncContractError("Gmail mailbox history moved backwards")
            return GmailHistoryObservation(tuple(sorted(dirty)), cursor, page)
        if not isinstance(continuation, str) or not continuation.strip() or continuation in seen:
            raise SyncContractError("Invalid or repeated Gmail pageToken")
        seen.add(continuation)
        token = continuation
    raise SyncContractError("Gmail history pagination incomplete")
