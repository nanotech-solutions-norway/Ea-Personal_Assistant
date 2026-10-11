"""Bounded, provider-neutral pagination collector for staging sync workers.

It performs no API calls itself and never logs provider payloads. The injected
fetch_page must authenticate to one authorized provider collection.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .unified_sync import SourceItem, SyncContractError


@dataclass(frozen=True)
class SourcePage:
    items: tuple[SourceItem, ...]
    next_page_token: str | None
    source_cursor: str | None = None


@dataclass(frozen=True)
class CompletedObservation:
    items: tuple[SourceItem, ...]
    source_cursor: str
    pages_fetched: int


def collect_source_pages(
    fetch_page: Callable[[str | None], SourcePage],
    *,
    max_pages: int = 100,
    max_items: int = 10000,
) -> CompletedObservation:
    """Raise without returning a partial observation after failure/limit/cycle."""
    if not isinstance(max_pages, int) or not 1 <= max_pages <= 1000:
        raise SyncContractError("Invalid provider page budget")
    if not isinstance(max_items, int) or not 1 <= max_items <= 100000:
        raise SyncContractError("Invalid provider item budget")
    token: str | None = None
    seen: set[str] = set()
    items: list[SourceItem] = []
    for page_number in range(1, max_pages + 1):
        page = fetch_page(token)
        if not isinstance(page, SourcePage):
            raise SyncContractError("Invalid provider page envelope")
        items.extend(page.items)
        if len(items) > max_items:
            raise SyncContractError("Provider inventory item cap exceeded")
        next_token = page.next_page_token
        if next_token is None:
            if not isinstance(page.source_cursor, str) or not page.source_cursor.strip():
                raise SyncContractError("Missing authoritative terminal source cursor")
            return CompletedObservation(tuple(items), page.source_cursor, page_number)
        if not isinstance(next_token, str) or not next_token.strip() or next_token in seen:
            raise SyncContractError("Provider cursor is invalid, repeated or cyclic")
        if page.source_cursor is not None:
            raise SyncContractError("Nonterminal provider page must not finalize a cursor")
        seen.add(next_token)
        token = next_token
    raise SyncContractError("Provider pagination incomplete at page limit")
