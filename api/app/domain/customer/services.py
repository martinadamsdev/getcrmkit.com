from __future__ import annotations

import uuid
from typing import Any

from app.domain.customer.entities import Contact, Customer, CustomerGrade, SavedView, Tag
from app.domain.customer.events import CustomerGradeChanged
from app.domain.customer.exceptions import (
    ContactNotFoundError,
    CustomerGradeNotFoundError,
    CustomerNameRequiredError,
    CustomerNotFoundError,
    DuplicateTagError,
    DuplicateViewNameError,
    GradeInUseError,
    SavedViewNotFoundError,
    TagNotFoundError,
)
from app.domain.customer.repository import (
    AbstractContactRepository,
    AbstractCustomerGradeRepository,
    AbstractCustomerRepository,
    AbstractSavedViewRepository,
    AbstractTagRepository,
)
from app.domain.customer.value_objects import CustomerFilter, DuplicateMatch


class CustomerGradeService:
    def __init__(
        self,
        grade_repo: AbstractCustomerGradeRepository,
        customer_repo: AbstractCustomerRepository,
    ) -> None:
        self._grade_repo = grade_repo
        self._customer_repo = customer_repo

    async def create_grade(
        self,
        *,
        name: str,
        label: str | None = None,
        color: str = "#3B82F6",
        position: int = 0,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
    ) -> CustomerGrade:
        grade = CustomerGrade(
            name=name,
            label=label,
            color=color,
            position=position,
            tenant_id=tenant_id,
            created_by=created_by,
        )
        return await self._grade_repo.create(grade)

    async def update_grade(
        self,
        *,
        tenant_id: uuid.UUID,
        grade_id: uuid.UUID,
        **kwargs: Any,
    ) -> CustomerGrade:
        grade = await self._grade_repo.get_by_id(tenant_id, grade_id)
        if grade is None:
            raise CustomerGradeNotFoundError(str(grade_id))
        for key, value in kwargs.items():
            setattr(grade, key, value)
        return await self._grade_repo.update(grade)

    async def delete_grade(self, *, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> None:
        grade = await self._grade_repo.get_by_id(tenant_id, grade_id)
        if grade is None:
            raise CustomerGradeNotFoundError(str(grade_id))
        in_use = await self._grade_repo.has_customers(tenant_id, grade_id)
        if in_use:
            raise GradeInUseError(str(grade_id))
        await self._grade_repo.delete(tenant_id, grade_id)

    async def get_all(self, *, tenant_id: uuid.UUID) -> list[CustomerGrade]:
        return await self._grade_repo.get_all(tenant_id)

    async def get_grade(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> CustomerGrade | None:
        return await self._grade_repo.get_by_id(tenant_id, grade_id)


class CustomerService:
    def __init__(self, customer_repo: AbstractCustomerRepository) -> None:
        self._repo = customer_repo

    async def create_customer(
        self,
        *,
        name: str,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        owner_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> Customer:
        if not name or not name.strip():
            raise CustomerNameRequiredError()
        customer = Customer.create(
            name=name,
            tenant_id=tenant_id,
            created_by=created_by,
            owner_id=owner_id,
            **kwargs,
        )
        return await self._repo.create(customer)

    async def update_customer(
        self,
        *,
        tenant_id: uuid.UUID,
        customer_id: uuid.UUID,
        **kwargs: Any,
    ) -> Customer:
        customer = await self._repo.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise CustomerNotFoundError(str(customer_id))

        old_grade_id = customer.grade_id

        for key, value in kwargs.items():
            setattr(customer, key, value)

        result = await self._repo.update(customer)

        if "grade_id" in kwargs and result.grade_id != old_grade_id:
            result.add_event(
                CustomerGradeChanged(
                    customer_id=result.id,
                    old_grade_id=old_grade_id,
                    new_grade_id=result.grade_id,
                )
            )

        return result

    async def get_customer(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> Customer:
        customer = await self._repo.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise CustomerNotFoundError(str(customer_id))
        return customer

    async def list_customers(
        self,
        tenant_id: uuid.UUID,
        page: int,
        page_size: int,
        filters: CustomerFilter | None = None,
    ) -> tuple[list[Customer], int]:
        return await self._repo.get_by_tenant(tenant_id, page, page_size, filters=filters)

    async def soft_delete_customer(self, *, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> None:
        customer = await self._repo.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise CustomerNotFoundError(str(customer_id))
        await self._repo.soft_delete(tenant_id, customer_id)


class ContactService:
    def __init__(
        self,
        contact_repo: AbstractContactRepository,
        customer_repo: AbstractCustomerRepository,
    ) -> None:
        self._contact_repo = contact_repo
        self._customer_repo = customer_repo

    async def create_contact(
        self,
        *,
        customer_id: uuid.UUID,
        name: str,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        **kwargs: Any,
    ) -> Contact:
        customer = await self._customer_repo.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise CustomerNotFoundError(str(customer_id))

        existing = await self._contact_repo.get_by_customer_id(tenant_id, customer_id)
        is_primary = len(existing) == 0

        contact = Contact(
            customer_id=customer_id,
            name=name,
            tenant_id=tenant_id,
            created_by=created_by,
            is_primary=is_primary,
            **kwargs,
        )
        return await self._contact_repo.create(contact)

    async def update_contact(
        self,
        *,
        tenant_id: uuid.UUID,
        contact_id: uuid.UUID,
        **kwargs: Any,
    ) -> Contact:
        contact = await self._contact_repo.get_by_id(tenant_id, contact_id)
        if contact is None:
            raise ContactNotFoundError(str(contact_id))
        for key, value in kwargs.items():
            setattr(contact, key, value)
        return await self._contact_repo.update(contact)

    async def set_primary(self, *, tenant_id: uuid.UUID, contact_id: uuid.UUID) -> Contact:
        contact = await self._contact_repo.get_by_id(tenant_id, contact_id)
        if contact is None:
            raise ContactNotFoundError(str(contact_id))

        await self._contact_repo.clear_primary(tenant_id, contact.customer_id)
        contact.is_primary = True
        return await self._contact_repo.update(contact)

    async def list_contacts(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Contact]:
        return await self._contact_repo.get_by_customer_id(tenant_id, customer_id)

    async def soft_delete_contact(self, *, tenant_id: uuid.UUID, contact_id: uuid.UUID) -> None:
        contact = await self._contact_repo.get_by_id(tenant_id, contact_id)
        if contact is None:
            raise ContactNotFoundError(str(contact_id))
        await self._contact_repo.soft_delete(tenant_id, contact_id)


class TagService:
    def __init__(self, tag_repo: AbstractTagRepository) -> None:
        self._repo = tag_repo

    async def get_all(self, tenant_id: uuid.UUID) -> list[Tag]:
        return await self._repo.get_all(tenant_id)

    async def create_tag(
        self,
        *,
        name: str,
        group_name: str | None = None,
        color: str = "#3B82F6",
        position: int = 0,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
    ) -> Tag:
        existing = await self._repo.get_by_name_and_group(tenant_id, name, group_name)
        if existing is not None:
            raise DuplicateTagError(name, group_name)
        tag = Tag(
            name=name,
            group_name=group_name,
            color=color,
            position=position,
            tenant_id=tenant_id,
            created_by=created_by,
        )
        return await self._repo.create(tag)

    async def update_tag(
        self,
        *,
        tenant_id: uuid.UUID,
        tag_id: uuid.UUID,
        **kwargs: Any,
    ) -> Tag:
        tag = await self._repo.get_by_id(tenant_id, tag_id)
        if tag is None:
            raise TagNotFoundError(str(tag_id))
        for key, value in kwargs.items():
            setattr(tag, key, value)
        return await self._repo.update(tag)

    async def delete_tag(self, *, tenant_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        tag = await self._repo.get_by_id(tenant_id, tag_id)
        if tag is None:
            raise TagNotFoundError(str(tag_id))
        await self._repo.delete(tenant_id, tag_id)

    async def tag_customer(
        self,
        *,
        tenant_id: uuid.UUID,
        customer_id: uuid.UUID,
        tag_id: uuid.UUID,
    ) -> None:
        tag = await self._repo.get_by_id(tenant_id, tag_id)
        if tag is None:
            raise TagNotFoundError(str(tag_id))
        await self._repo.add_to_customer(tenant_id, customer_id, tag_id)

    async def untag_customer(
        self,
        *,
        tenant_id: uuid.UUID,
        customer_id: uuid.UUID,
        tag_id: uuid.UUID,
    ) -> None:
        await self._repo.remove_from_customer(tenant_id, customer_id, tag_id)

    async def get_tags_for_customer(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Tag]:
        return await self._repo.get_by_customer_id(tenant_id, customer_id)


class DuplicateChecker:
    PUBLIC_DOMAINS = frozenset(
        {
            "gmail.com",
            "hotmail.com",
            "yahoo.com",
            "outlook.com",
            "163.com",
            "126.com",
            "qq.com",
            "foxmail.com",
            "icloud.com",
            "aol.com",
            "mail.com",
            "protonmail.com",
        }
    )

    def __init__(self, customer_repo: AbstractCustomerRepository) -> None:
        self._repo = customer_repo

    async def check(
        self,
        tenant_id: uuid.UUID,
        name: str,
        email: str | None = None,
        exclude_id: uuid.UUID | None = None,
    ) -> list[DuplicateMatch]:
        seen: dict[uuid.UUID, DuplicateMatch] = {}
        name_matches = await self._repo.find_by_name_exact(tenant_id, name, exclude_id)
        for c in name_matches:
            if c.id not in seen:
                seen[c.id] = DuplicateMatch(
                    customer_id=c.id, customer_name=c.name, match_type="name_exact", matched_value=c.name
                )
        if email:
            domain = email.split("@")[-1].lower() if "@" in email else None
            if domain and domain not in self.PUBLIC_DOMAINS:
                domain_matches = await self._repo.find_by_email_domain(tenant_id, domain, exclude_id)
                for c in domain_matches:
                    if c.id not in seen:
                        seen[c.id] = DuplicateMatch(
                            customer_id=c.id, customer_name=c.name, match_type="email_domain", matched_value=domain
                        )
            exact_matches = await self._repo.find_by_email_exact(tenant_id, email, exclude_id)
            for c in exact_matches:
                if c.id not in seen:
                    seen[c.id] = DuplicateMatch(
                        customer_id=c.id, customer_name=c.name, match_type="email_exact", matched_value=email
                    )
        return list(seen.values())


class SavedViewService:
    def __init__(self, repo: AbstractSavedViewRepository) -> None:
        self._repo = repo

    async def create_view(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        name: str,
        entity_type: str,
        filter_config: dict[str, Any],
        is_default: bool = False,
        position: int = 0,
    ) -> SavedView:
        existing = await self._repo.get_by_name(tenant_id, user_id, entity_type, name)
        if existing:
            raise DuplicateViewNameError(name)
        view = SavedView(
            tenant_id=tenant_id,
            user_id=user_id,
            entity_type=entity_type,
            name=name,
            filter_config=filter_config,
            is_default=is_default,
            position=position,
            created_by=user_id,
        )
        return await self._repo.create(view)

    async def update_view(self, *, id: uuid.UUID, tenant_id: uuid.UUID, user_id: uuid.UUID, **kwargs: Any) -> SavedView:
        view = await self._repo.get_by_id(tenant_id, user_id, id)
        if view is None:
            raise SavedViewNotFoundError(str(id))
        if "name" in kwargs:
            existing = await self._repo.get_by_name(tenant_id, user_id, view.entity_type, kwargs["name"])
            if existing and existing.id != view.id:
                raise DuplicateViewNameError(kwargs["name"])
        for key, value in kwargs.items():
            setattr(view, key, value)
        return await self._repo.update(view)

    async def delete_view(self, *, id: uuid.UUID, tenant_id: uuid.UUID, user_id: uuid.UUID) -> None:
        view = await self._repo.get_by_id(tenant_id, user_id, id)
        if view is None:
            raise SavedViewNotFoundError(str(id))
        await self._repo.delete(tenant_id, user_id, id)

    async def get_all(self, *, tenant_id: uuid.UUID, user_id: uuid.UUID, entity_type: str) -> list[SavedView]:
        return await self._repo.get_all(tenant_id, user_id, entity_type)
