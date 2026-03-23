from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class ProductCreated(DomainEvent):
    product_id: uuid.UUID | None = None
    tenant_id: uuid.UUID | None = None
    created_by: uuid.UUID | None = None

    def __post_init__(self) -> None:
        if self.product_id is None:
            raise ValueError("ProductCreated.product_id is required")


@dataclass(frozen=True)
class ProductDeleted(DomainEvent):
    product_id: uuid.UUID | None = None
    tenant_id: uuid.UUID | None = None

    def __post_init__(self) -> None:
        if self.product_id is None:
            raise ValueError("ProductDeleted.product_id is required")
