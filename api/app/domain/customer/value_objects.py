from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Literal

from app.domain.customer.enums import FollowUpStage


@dataclass(frozen=True)
class CustomerFilter:
    keyword: str | None = None
    grade_id: uuid.UUID | None = None
    source: str | None = None
    follow_status: FollowUpStage | None = None
    country: str | None = None
    industry: str | None = None
    tag_ids: list[uuid.UUID] = field(default_factory=list)
    owner_id: uuid.UUID | None = None
    created_at_from: datetime | None = None
    created_at_to: datetime | None = None
    last_follow_at_from: datetime | None = None
    last_follow_at_to: datetime | None = None
    sort_by: Literal["created_at", "name", "last_follow_at"] = "created_at"
    sort: Literal["asc", "desc"] = "desc"


@dataclass(frozen=True)
class DuplicateMatch:
    customer_id: uuid.UUID
    customer_name: str
    match_type: str
    matched_value: str


@dataclass(frozen=True)
class Customer360Stats:
    contact_count: int
    follow_up_count: int = 0
    quotation_count: int = 0
    order_count: int = 0
    last_follow_at: datetime | None = None
    total_order_amount: Decimal | None = None
