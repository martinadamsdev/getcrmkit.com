from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from app.domain.customer.entities import Contact, Customer, CustomerGrade, Tag
from app.domain.customer.exceptions import CustomerNotFoundError
from app.domain.customer.repository import (
    AbstractContactRepository,
    AbstractCustomerGradeRepository,
    AbstractCustomerRepository,
    AbstractTagRepository,
)
from app.domain.customer.value_objects import Customer360Stats


@dataclass
class Customer360View:
    customer: Customer
    grade: CustomerGrade | None
    tags: list[Tag]
    contacts: list[Contact]
    follow_ups: list[dict[str, Any]] = field(default_factory=list)
    quotations: list[dict[str, Any]] = field(default_factory=list)
    orders: list[dict[str, Any]] = field(default_factory=list)
    stats: Customer360Stats = field(default_factory=lambda: Customer360Stats(contact_count=0))


class Customer360QueryService:
    def __init__(
        self,
        customer_repo: AbstractCustomerRepository,
        contact_repo: AbstractContactRepository,
        grade_repo: AbstractCustomerGradeRepository,
        tag_repo: AbstractTagRepository,
    ) -> None:
        self._customer_repo = customer_repo
        self._contact_repo = contact_repo
        self._grade_repo = grade_repo
        self._tag_repo = tag_repo

    async def get_360_view(self, customer_id: uuid.UUID, tenant_id: uuid.UUID) -> Customer360View:
        customer = await self._customer_repo.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise CustomerNotFoundError(str(customer_id))
        grade = None
        if customer.grade_id:
            grade = await self._grade_repo.get_by_id(tenant_id, customer.grade_id)
        tags = await self._tag_repo.get_by_customer_id(tenant_id, customer_id)
        contacts = await self._contact_repo.get_by_customer_id(tenant_id, customer_id)
        stats = Customer360Stats(contact_count=len(contacts), last_follow_at=customer.last_follow_at)
        return Customer360View(customer=customer, grade=grade, tags=tags, contacts=contacts, stats=stats)
