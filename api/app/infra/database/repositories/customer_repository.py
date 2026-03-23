from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import exists, func, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import Contact, Customer, CustomerGrade, Tag
from app.domain.customer.enums import FollowUpStage
from app.domain.customer.repository import (
    AbstractContactRepository,
    AbstractCustomerGradeRepository,
    AbstractCustomerRepository,
    AbstractTagRepository,
)
from app.domain.customer.value_objects import CustomerFilter
from app.infra.database.models.customer import (
    ContactModel,
    CustomerGradeModel,
    CustomerModel,
    TagModel,
    customer_tags_table,
)

SORT_COLUMNS: dict[str, object] = {
    "created_at": CustomerModel.created_at,
    "name": CustomerModel.name,
    "last_follow_at": CustomerModel.last_follow_at,
}


class CustomerGradeRepository(AbstractCustomerGradeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, grade: CustomerGrade) -> CustomerGrade:
        model = self._to_model(grade)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> CustomerGrade | None:
        stmt = select(CustomerGradeModel).where(
            CustomerGradeModel.id == grade_id,
            CustomerGradeModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID) -> list[CustomerGrade]:
        stmt = (
            select(CustomerGradeModel)
            .where(CustomerGradeModel.tenant_id == tenant_id)
            .order_by(CustomerGradeModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def update(self, grade: CustomerGrade) -> CustomerGrade:
        stmt = select(CustomerGradeModel).where(
            CustomerGradeModel.id == grade.id,
            CustomerGradeModel.tenant_id == grade.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = grade.name
        model.label = grade.label
        model.color = grade.color
        model.position = grade.position
        model.updated_by = grade.updated_by
        model.updated_at = grade.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> None:
        stmt = select(CustomerGradeModel).where(
            CustomerGradeModel.id == grade_id,
            CustomerGradeModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    async def has_customers(self, tenant_id: uuid.UUID, grade_id: uuid.UUID) -> bool:
        stmt = select(
            exists().where(
                CustomerModel.grade_id == grade_id,
                CustomerModel.tenant_id == tenant_id,
                CustomerModel.deleted_at.is_(None),
            )
        )
        result = await self._session.execute(stmt)
        return bool(result.scalar())

    @staticmethod
    def _to_model(grade: CustomerGrade) -> CustomerGradeModel:
        return CustomerGradeModel(
            id=grade.id,
            tenant_id=grade.tenant_id,
            name=grade.name,
            label=grade.label,
            color=grade.color,
            position=grade.position,
            created_by=grade.created_by,
            updated_by=grade.updated_by,
            created_at=grade.created_at,
            updated_at=grade.updated_at,
        )

    @staticmethod
    def _to_entity(model: CustomerGradeModel) -> CustomerGrade:
        return CustomerGrade(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            label=model.label,
            color=model.color,
            position=model.position,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class CustomerRepository(AbstractCustomerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, customer: Customer) -> Customer:
        model = self._to_model(customer)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> Customer | None:
        stmt = select(CustomerModel).where(
            CustomerModel.id == customer_id,
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_tenant(
        self, tenant_id: uuid.UUID, page: int, page_size: int, filters: CustomerFilter | None = None
    ) -> tuple[list[Customer], int]:
        conditions = [
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        ]

        if filters is not None:
            if filters.keyword:
                conditions.append(CustomerModel.name.op("%")(filters.keyword))
            if filters.grade_id is not None:
                conditions.append(CustomerModel.grade_id == filters.grade_id)
            if filters.source is not None:
                conditions.append(CustomerModel.source == filters.source)
            if filters.follow_status is not None:
                conditions.append(CustomerModel.follow_status == filters.follow_status.value)
            if filters.country is not None:
                conditions.append(CustomerModel.country == filters.country)
            if filters.industry is not None:
                conditions.append(CustomerModel.industry == filters.industry)
            if filters.owner_id is not None:
                conditions.append(CustomerModel.owner_id == filters.owner_id)
            if filters.tag_ids:
                conditions.append(
                    exists(
                        select(customer_tags_table.c.customer_id).where(
                            customer_tags_table.c.customer_id == CustomerModel.id,
                            customer_tags_table.c.tag_id.in_(filters.tag_ids),
                        )
                    )
                )
            if filters.created_at_from is not None:
                conditions.append(CustomerModel.created_at >= filters.created_at_from)
            if filters.created_at_to is not None:
                conditions.append(CustomerModel.created_at <= filters.created_at_to)
            if filters.last_follow_at_from is not None:
                conditions.append(CustomerModel.last_follow_at >= filters.last_follow_at_from)
            if filters.last_follow_at_to is not None:
                conditions.append(CustomerModel.last_follow_at <= filters.last_follow_at_to)

        count_stmt = select(func.count()).select_from(CustomerModel).where(*conditions)
        total = (await self._session.execute(count_stmt)).scalar_one()

        # Sort
        sort_col = SORT_COLUMNS.get(filters.sort_by if filters else "created_at", CustomerModel.created_at)
        sort_order = filters.sort_order if filters else "desc"
        order_clause = sort_col.asc() if sort_order == "asc" else sort_col.desc()  # type: ignore[attr-defined]

        stmt = (
            select(CustomerModel)
            .where(*conditions)
            .order_by(order_clause)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        items = [self._to_entity(m) for m in result.scalars()]
        return items, total

    async def update(self, customer: Customer) -> Customer:
        stmt = select(CustomerModel).where(
            CustomerModel.id == customer.id,
            CustomerModel.tenant_id == customer.tenant_id,
            CustomerModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = customer.name
        model.country = customer.country
        model.region = customer.region
        model.city = customer.city
        model.address = customer.address
        model.industry = customer.industry
        model.company_size = customer.company_size
        model.website = customer.website
        model.source = customer.source
        model.grade_id = customer.grade_id
        model.follow_status = customer.follow_status.value
        model.main_products = customer.main_products
        model.annual_volume = customer.annual_volume
        model.current_supplier = customer.current_supplier
        model.decision_process = customer.decision_process
        model.owner_id = customer.owner_id
        model.claimed_at = customer.claimed_at
        model.last_follow_at = customer.last_follow_at
        model.custom_fields = customer.custom_fields
        model.updated_by = customer.updated_by
        model.updated_at = customer.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def soft_delete(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> None:
        stmt = select(CustomerModel).where(
            CustomerModel.id == customer_id,
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.deleted_at = datetime.now(UTC)
        await self._session.flush()

    async def find_by_name_exact(
        self, tenant_id: uuid.UUID, name: str, exclude_id: uuid.UUID | None = None
    ) -> list[Customer]:
        conditions = [
            func.lower(func.trim(CustomerModel.name)) == func.lower(func.trim(name)),
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        ]
        if exclude_id is not None:
            conditions.append(CustomerModel.id != exclude_id)
        stmt = select(CustomerModel).where(*conditions)
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def find_by_email_domain(
        self, tenant_id: uuid.UUID, domain: str, exclude_id: uuid.UUID | None = None
    ) -> list[Customer]:
        id_conditions = [
            func.split_part(ContactModel.email, literal_column("'@'"), 2) == domain,
            ContactModel.deleted_at.is_(None),
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        ]
        if exclude_id is not None:
            id_conditions.append(CustomerModel.id != exclude_id)
        id_subq = (
            select(CustomerModel.id)
            .join(ContactModel, ContactModel.customer_id == CustomerModel.id)
            .where(*id_conditions)
            .distinct()
            .subquery()
        )
        stmt = select(CustomerModel).where(CustomerModel.id.in_(select(id_subq)))
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def find_by_email_exact(
        self, tenant_id: uuid.UUID, email: str, exclude_id: uuid.UUID | None = None
    ) -> list[Customer]:
        id_conditions = [
            ContactModel.email == email,
            ContactModel.deleted_at.is_(None),
            CustomerModel.tenant_id == tenant_id,
            CustomerModel.deleted_at.is_(None),
        ]
        if exclude_id is not None:
            id_conditions.append(CustomerModel.id != exclude_id)
        id_subq = (
            select(CustomerModel.id)
            .join(ContactModel, ContactModel.customer_id == CustomerModel.id)
            .where(*id_conditions)
            .distinct()
            .subquery()
        )
        stmt = select(CustomerModel).where(CustomerModel.id.in_(select(id_subq)))
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(CustomerModel)
            .where(
                CustomerModel.tenant_id == tenant_id,
                CustomerModel.deleted_at.is_(None),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    def _to_model(customer: Customer) -> CustomerModel:
        return CustomerModel(
            id=customer.id,
            tenant_id=customer.tenant_id,
            name=customer.name,
            country=customer.country,
            region=customer.region,
            city=customer.city,
            address=customer.address,
            industry=customer.industry,
            company_size=customer.company_size,
            website=customer.website,
            source=customer.source,
            grade_id=customer.grade_id,
            follow_status=customer.follow_status.value,
            main_products=customer.main_products,
            annual_volume=customer.annual_volume,
            current_supplier=customer.current_supplier,
            decision_process=customer.decision_process,
            owner_id=customer.owner_id,
            claimed_at=customer.claimed_at,
            last_follow_at=customer.last_follow_at,
            custom_fields=customer.custom_fields,
            created_by=customer.created_by,
            updated_by=customer.updated_by,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
            deleted_at=customer.deleted_at,
        )

    @staticmethod
    def _to_entity(model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            country=model.country,
            region=model.region,
            city=model.city,
            address=model.address,
            industry=model.industry,
            company_size=model.company_size,
            website=model.website,
            source=model.source,
            grade_id=model.grade_id,
            follow_status=FollowUpStage(model.follow_status),
            main_products=model.main_products,
            annual_volume=model.annual_volume,
            current_supplier=model.current_supplier,
            decision_process=model.decision_process,
            owner_id=model.owner_id,
            claimed_at=model.claimed_at,
            last_follow_at=model.last_follow_at,
            custom_fields=model.custom_fields,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )


class ContactRepository(AbstractContactRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, contact: Contact) -> Contact:
        model = self._to_model(contact)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, contact_id: uuid.UUID) -> Contact | None:
        stmt = select(ContactModel).where(
            ContactModel.id == contact_id,
            ContactModel.tenant_id == tenant_id,
            ContactModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_customer_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Contact]:
        stmt = select(ContactModel).where(
            ContactModel.customer_id == customer_id,
            ContactModel.tenant_id == tenant_id,
            ContactModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def update(self, contact: Contact) -> Contact:
        stmt = select(ContactModel).where(
            ContactModel.id == contact.id,
            ContactModel.tenant_id == contact.tenant_id,
            ContactModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = contact.name
        model.title = contact.title
        model.email = contact.email
        model.phone = contact.phone
        model.whatsapp = contact.whatsapp
        model.skype = contact.skype
        model.linkedin = contact.linkedin
        model.wechat = contact.wechat
        model.is_primary = contact.is_primary
        model.notes = contact.notes
        model.custom_fields = contact.custom_fields
        model.updated_by = contact.updated_by
        model.updated_at = contact.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def soft_delete(self, tenant_id: uuid.UUID, contact_id: uuid.UUID) -> None:
        stmt = select(ContactModel).where(
            ContactModel.id == contact_id,
            ContactModel.tenant_id == tenant_id,
            ContactModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.deleted_at = datetime.now(UTC)
        await self._session.flush()

    async def clear_primary(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> None:
        from sqlalchemy import update

        stmt = (
            update(ContactModel)
            .where(
                ContactModel.customer_id == customer_id,
                ContactModel.tenant_id == tenant_id,
                ContactModel.deleted_at.is_(None),
            )
            .values(is_primary=False)
        )
        await self._session.execute(stmt)
        await self._session.flush()

    @staticmethod
    def _to_model(contact: Contact) -> ContactModel:
        return ContactModel(
            id=contact.id,
            tenant_id=contact.tenant_id,
            customer_id=contact.customer_id,
            name=contact.name,
            title=contact.title,
            email=contact.email,
            phone=contact.phone,
            whatsapp=contact.whatsapp,
            skype=contact.skype,
            linkedin=contact.linkedin,
            wechat=contact.wechat,
            is_primary=contact.is_primary,
            notes=contact.notes,
            custom_fields=contact.custom_fields,
            created_by=contact.created_by,
            updated_by=contact.updated_by,
            created_at=contact.created_at,
            updated_at=contact.updated_at,
            deleted_at=contact.deleted_at,
        )

    @staticmethod
    def _to_entity(model: ContactModel) -> Contact:
        return Contact(
            id=model.id,
            tenant_id=model.tenant_id,
            customer_id=model.customer_id,
            name=model.name,
            title=model.title,
            email=model.email,
            phone=model.phone,
            whatsapp=model.whatsapp,
            skype=model.skype,
            linkedin=model.linkedin,
            wechat=model.wechat,
            is_primary=model.is_primary,
            notes=model.notes,
            custom_fields=model.custom_fields,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )


class TagRepository(AbstractTagRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, tag: Tag) -> Tag:
        model = self._to_model(tag)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, tag_id: uuid.UUID) -> Tag | None:
        stmt = select(TagModel).where(
            TagModel.id == tag_id,
            TagModel.tenant_id == tenant_id,
            TagModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID) -> list[Tag]:
        stmt = (
            select(TagModel)
            .where(
                TagModel.tenant_id == tenant_id,
                TagModel.deleted_at.is_(None),
            )
            .order_by(TagModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def get_by_name_and_group(self, tenant_id: uuid.UUID, name: str, group_name: str | None) -> Tag | None:
        group_filter = TagModel.group_name == group_name if group_name else TagModel.group_name.is_(None)
        stmt = select(TagModel).where(
            TagModel.tenant_id == tenant_id,
            TagModel.name == name,
            TagModel.deleted_at.is_(None),
            group_filter,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, tag: Tag) -> Tag:
        stmt = select(TagModel).where(
            TagModel.id == tag.id,
            TagModel.tenant_id == tag.tenant_id,
            TagModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = tag.name
        model.color = tag.color
        model.group_name = tag.group_name
        model.position = tag.position
        model.updated_by = tag.updated_by
        model.updated_at = tag.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        stmt = select(TagModel).where(
            TagModel.id == tag_id,
            TagModel.tenant_id == tenant_id,
            TagModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    async def add_to_customer(self, tenant_id: uuid.UUID, customer_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        from sqlalchemy.dialects.postgresql import insert

        stmt = (
            insert(customer_tags_table)
            .values(
                customer_id=customer_id,
                tag_id=tag_id,
            )
            .on_conflict_do_nothing()
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def remove_from_customer(self, tenant_id: uuid.UUID, customer_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        from sqlalchemy import delete

        stmt = delete(customer_tags_table).where(
            customer_tags_table.c.customer_id == customer_id,
            customer_tags_table.c.tag_id == tag_id,
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_by_customer_id(self, tenant_id: uuid.UUID, customer_id: uuid.UUID) -> list[Tag]:
        stmt = (
            select(TagModel)
            .join(
                customer_tags_table,
                customer_tags_table.c.tag_id == TagModel.id,
            )
            .where(
                customer_tags_table.c.customer_id == customer_id,
                TagModel.tenant_id == tenant_id,
                TagModel.deleted_at.is_(None),
            )
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    @staticmethod
    def _to_model(tag: Tag) -> TagModel:
        return TagModel(
            id=tag.id,
            tenant_id=tag.tenant_id,
            name=tag.name,
            color=tag.color,
            group_name=tag.group_name,
            position=tag.position,
            created_by=tag.created_by,
            updated_by=tag.updated_by,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
            deleted_at=tag.deleted_at,
        )

    @staticmethod
    def _to_entity(model: TagModel) -> Tag:
        return Tag(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            color=model.color,
            group_name=model.group_name,
            position=model.position,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
