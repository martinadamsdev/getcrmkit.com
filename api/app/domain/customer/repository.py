from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.customer.entities import Contact, Customer, CustomerGrade, DataJob, SavedView, Tag
from app.domain.customer.value_objects import CustomerFilter


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
        self,
        tenant_id: uuid.UUID,
        page: int,
        page_size: int,
        filters: CustomerFilter | None = None,
    ) -> tuple[list[Customer], int]: ...

    @abstractmethod
    async def update(self, customer: Customer) -> Customer: ...

    @abstractmethod
    async def soft_delete(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def find_by_name_exact(
        self, tenant_id: uuid.UUID, name: str, exclude_id: uuid.UUID | None = None
    ) -> list[Customer]: ...

    @abstractmethod
    async def find_by_email_domain(
        self, tenant_id: uuid.UUID, domain: str, exclude_id: uuid.UUID | None = None
    ) -> list[Customer]: ...

    @abstractmethod
    async def find_by_email_exact(
        self, tenant_id: uuid.UUID, email: str, exclude_id: uuid.UUID | None = None
    ) -> list[Customer]: ...

    @abstractmethod
    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int: ...


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
    async def get_by_name_and_group(self, tenant_id: uuid.UUID, name: str, group_name: str | None) -> Tag | None: ...

    @abstractmethod
    async def update(self, tag: Tag) -> Tag: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, tag_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def add_to_customer(self, tenant_id: uuid.UUID, customer_id: uuid.UUID, tag_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def remove_from_customer(self, tenant_id: uuid.UUID, customer_id: uuid.UUID, tag_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_customer_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Tag]: ...


class AbstractSavedViewRepository(ABC):
    @abstractmethod
    async def create(self, view: SavedView) -> SavedView: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, user_id: uuid.UUID, view_id: uuid.UUID) -> SavedView | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID, user_id: uuid.UUID, entity_type: str) -> list[SavedView]: ...

    @abstractmethod
    async def get_by_name(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, entity_type: str, name: str
    ) -> SavedView | None: ...

    @abstractmethod
    async def update(self, view: SavedView) -> SavedView: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, user_id: uuid.UUID, view_id: uuid.UUID) -> None: ...


class AbstractDataJobRepository(ABC):
    @abstractmethod
    async def create(self, job: DataJob) -> DataJob: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, job_id: uuid.UUID) -> DataJob | None: ...

    @abstractmethod
    async def update(self, job: DataJob) -> DataJob: ...
