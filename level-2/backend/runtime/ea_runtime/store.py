from __future__ import annotations

from dataclasses import asdict
from typing import Protocol

from .events import EventEnvelope


class EventStore(Protocol):
    def put_if_absent(self, event: EventEnvelope) -> bool:
        """Persist event durably.

        Returns True when newly inserted, False when already present.
        """


class InMemoryEventStore:
    """Test-only store. Never use as a production webhook acknowledgement sink."""

    def __init__(self) -> None:
        self.events: dict[str, dict] = {}

    def put_if_absent(self, event: EventEnvelope) -> bool:
        if event.event_id in self.events:
            return False
        self.events[event.event_id] = asdict(event)
        return True
