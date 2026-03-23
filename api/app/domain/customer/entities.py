from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.customer.enums import FollowUpStage
from app.domain.shared.entity import BaseEntity


@dataclass
class CustomerGrade(BaseEntity):
    name: str = ""
    label: str | None = None
    color: str = "#3B82F6"
    position: int = 0


@dataclass
class Customer(BaseEntity):
    name: str = ""
    country: str | None = None
    region: str | None = None
    city: str | None = None
    address: str | None = None
    industry: str | None = None
    company_size: str | None = None
    website: str | None = None
    source: str | None = None
    grade_id: uuid.UUID | None = None
    follow_status: FollowUpStage = FollowUpStage.NEW
    main_products: str | None = None
    annual_volume: str | None = None
    current_supplier: str | None = None
    decision_process: str | None = None
    owner_id: uuid.UUID | None = None
    claimed_at: datetime | None = None
    last_follow_at: datetime | None = None
    custom_fields: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        **kwargs: Any,
    ) -> Customer:
        if not name or not name.strip():
            from app.domain.customer.exceptions import CustomerNameRequiredError

            raise CustomerNameRequiredError()
        return cls(
            name=name.strip(),
            tenant_id=tenant_id,
            created_by=created_by,
            **kwargs,
        )


@dataclass
class Contact(BaseEntity):
    customer_id: uuid.UUID = field(default_factory=uuid.uuid7)
    name: str = ""
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    skype: str | None = None
    linkedin: str | None = None
    wechat: str | None = None
    is_primary: bool = False
    notes: str | None = None
    custom_fields: dict[str, Any] = field(default_factory=dict)


@dataclass
class Tag(BaseEntity):
    name: str = ""
    color: str = "#3B82F6"
    group_name: str | None = None
    position: int = 0
