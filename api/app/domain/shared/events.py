import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class DomainEvent:
    event_id: uuid.UUID = field(default_factory=uuid.uuid7)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
