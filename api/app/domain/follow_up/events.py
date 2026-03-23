from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class FollowUpCreated(DomainEvent):
    follow_up_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    tenant_id: uuid.UUID | None = None
    created_by: uuid.UUID | None = None

    def __post_init__(self) -> None:
        if self.follow_up_id is None:
            raise ValueError("FollowUpCreated.follow_up_id is required")
        if self.customer_id is None:
            raise ValueError("FollowUpCreated.customer_id is required")
