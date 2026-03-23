import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class BaseEntity:
    id: uuid.UUID = field(default_factory=uuid.uuid7)
    tenant_id: uuid.UUID = field(default_factory=uuid.uuid7)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = field(default=None)
    created_by: uuid.UUID | None = field(default=None)
    updated_by: uuid.UUID | None = field(default=None)
    _events: list[Any] = field(default_factory=list, init=False, repr=False, compare=False)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(UTC)

    def add_event(self, event: Any) -> None:
        self._events.append(event)

    def pull_events(self) -> list[Any]:
        events = list(self._events)
        self._events.clear()
        return events
