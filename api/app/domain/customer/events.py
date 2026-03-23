from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class CustomerGradeChanged(DomainEvent):
    customer_id: uuid.UUID | None = None
    old_grade_id: uuid.UUID | None = None
    new_grade_id: uuid.UUID | None = None

    def __post_init__(self) -> None:
        if self.customer_id is None:
            raise ValueError("CustomerGradeChanged.customer_id is required")
