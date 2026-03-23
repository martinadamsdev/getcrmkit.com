from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.customer.entities import Contact, Customer, CustomerGrade, Tag


class AbstractCustomerGradeRepository(ABC):
    @abstractmethod
    async def create(self, grade: CustomerGrade) -> CustomerGrade: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> CustomerGrade | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID) -> list[CustomerGrade]: ...

    @abstractmethod
    async def update(self, grade: CustomerGrade) -> CustomerGrade: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def has_customers(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> bool: ...


class AbstractCustomerRepository(ABC):
    @abstractmethod
    async def create(self, customer: Customer) -> Customer: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> Customer | None: ...

    @abstractmethod
    async def get_by_tenant(
        self, tenant_id: uuid.UUID, page: int, page_size: int
    ) -> tuple[list[Customer], int]: ...

    @abstractmethod
    async def update(self, customer: Customer) -> Customer: ...

    @abstractmethod
    async def soft_delete(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> None: ...


class AbstractContactRepository(ABC):
    @abstractmethod
    async def create(self, contact: Contact) -> Contact: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, contact_id: uuid.UUID) -> Contact | None: ...

    @abstractmethod
    async def get_by_customer_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Contact]: ...

    @abstractmethod
    async def update(self, contact: Contact) -> Contact: ...

    @abstractmethod
    async def soft_delete(self, tenant_id: uuid.UUID, contact_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def clear_primary(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> None: ...


class AbstractTagRepository(ABC):
    @abstractmethod
    async def create(self, tag: Tag) -> Tag: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, tag_id: uuid.UUID) -> Tag | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID) -> list[Tag]: ...

    @abstractmethod
    async def get_by_name_and_group(
        self, tenant_id: uuid.UUID, name: str, group_name: str | None
    ) -> Tag | None: ...

    @abstractmethod
    async def update(self, tag: Tag) -> Tag: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, tag_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def add_to_customer(
        self, tenant_id: uuid.UUID, customer_id: uuid.UUID, tag_id: uuid.UUID
    ) -> None: ...

    @abstractmethod
    async def remove_from_customer(
        self, tenant_id: uuid.UUID, customer_id: uuid.UUID, tag_id: uuid.UUID
    ) -> None: ...

    @abstractmethod
    async def get_by_customer_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Tag]: ...
