import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import Contact, Customer, CustomerGrade, Tag
from app.domain.customer.enums import FollowUpStage
from app.infra.database.repositories.customer_repository import (
    ContactRepository,
    CustomerGradeRepository,
    CustomerRepository,
    TagRepository,
)


def make_grade(tenant_id: uuid.UUID, name: str = "A", position: int = 0) -> CustomerGrade:
    now = datetime.now(UTC)
    return CustomerGrade(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        name=name,
        color="#22C55E",
        position=position,
        created_at=now,
        updated_at=now,
    )


def make_customer(tenant_id: uuid.UUID, name: str = "Acme Corp") -> Customer:
    now = datetime.now(UTC)
    return Customer(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        name=name,
        follow_status=FollowUpStage.NEW,
        custom_fields={},
        created_at=now,
        updated_at=now,
    )


def make_contact(tenant_id: uuid.UUID, customer_id: uuid.UUID, name: str = "Alice") -> Contact:
    now = datetime.now(UTC)
    return Contact(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        customer_id=customer_id,
        name=name,
        custom_fields={},
        created_at=now,
        updated_at=now,
    )


def make_tag(tenant_id: uuid.UUID, name: str = "VIP") -> Tag:
    now = datetime.now(UTC)
    return Tag(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        name=name,
        color="#3B82F6",
        position=0,
        created_at=now,
        updated_at=now,
    )


# ---------------------------------------------------------------------------
# CustomerGradeRepository
# ---------------------------------------------------------------------------


class TestCustomerGradeRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)
        grade = make_grade(tenant_id, name="Gold")

        created = await repo.create(grade)
        fetched = await repo.get_by_id(tenant_id, created.id)

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "Gold"
        assert fetched.tenant_id == tenant_id
        assert fetched.color == "#22C55E"

    async def test_get_by_id_wrong_tenant_returns_none(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        other_tenant = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)
        grade = await repo.create(make_grade(tenant_id))

        result = await repo.get_by_id(other_tenant, grade.id)
        assert result is None

    async def test_get_all_ordered_by_position(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)
        await repo.create(make_grade(tenant_id, name="C", position=2))
        await repo.create(make_grade(tenant_id, name="A", position=0))
        await repo.create(make_grade(tenant_id, name="B", position=1))

        grades = await repo.get_all(tenant_id)
        assert len(grades) == 3
        assert [g.name for g in grades] == ["A", "B", "C"]

    async def test_update_grade(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)
        grade = await repo.create(make_grade(tenant_id, name="OldName"))

        grade.name = "NewName"
        grade.label = "Premium"
        updated = await repo.update(grade)

        assert updated.name == "NewName"
        assert updated.label == "Premium"

        fetched = await repo.get_by_id(tenant_id, grade.id)
        assert fetched is not None
        assert fetched.name == "NewName"
        assert fetched.label == "Premium"

    async def test_delete_grade(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)
        grade = await repo.create(make_grade(tenant_id))

        await repo.delete(tenant_id, grade.id)
        fetched = await repo.get_by_id(tenant_id, grade.id)
        assert fetched is None

    async def test_has_customers_true(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        grade_repo = CustomerGradeRepository(db_session)
        customer_repo = CustomerRepository(db_session)

        grade = await grade_repo.create(make_grade(tenant_id))
        customer = make_customer(tenant_id)
        customer.grade_id = grade.id
        await customer_repo.create(customer)

        result = await grade_repo.has_customers(tenant_id, grade.id)
        assert result is True

    async def test_has_customers_false(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)
        grade = await repo.create(make_grade(tenant_id))

        result = await repo.has_customers(tenant_id, grade.id)
        assert result is False

    async def test_get_all_empty(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerGradeRepository(db_session)

        grades = await repo.get_all(tenant_id)
        assert grades == []


# ---------------------------------------------------------------------------
# CustomerRepository
# ---------------------------------------------------------------------------


class TestCustomerRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        customer = make_customer(tenant_id, name="Globex Corp")

        created = await repo.create(customer)
        fetched = await repo.get_by_id(tenant_id, created.id)

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "Globex Corp"
        assert fetched.follow_status == FollowUpStage.NEW

    async def test_get_by_id_wrong_tenant_returns_none(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        other_tenant = uuid.uuid7()
        repo = CustomerRepository(db_session)
        customer = await repo.create(make_customer(tenant_id))

        result = await repo.get_by_id(other_tenant, customer.id)
        assert result is None

    async def test_get_by_tenant_pagination(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        for i in range(5):
            await repo.create(make_customer(tenant_id, name=f"Customer {i}"))

        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=3)
        assert total == 5
        assert len(items) == 3

    async def test_soft_delete(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        customer = await repo.create(make_customer(tenant_id))

        await repo.soft_delete(tenant_id, customer.id)
        fetched = await repo.get_by_id(tenant_id, customer.id)
        assert fetched is None

    async def test_update_customer(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        customer = await repo.create(make_customer(tenant_id, name="OldName"))

        customer.name = "NewName"
        customer.follow_status = FollowUpStage.CONTACTED
        updated = await repo.update(customer)

        assert updated.name == "NewName"
        assert updated.follow_status == FollowUpStage.CONTACTED

    async def test_soft_delete_excludes_from_list(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        c1 = await repo.create(make_customer(tenant_id, name="Keep"))
        c2 = await repo.create(make_customer(tenant_id, name="Delete"))

        await repo.soft_delete(tenant_id, c2.id)
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10)

        assert total == 1
        assert len(items) == 1
        assert items[0].id == c1.id

    async def test_create_with_grade(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        grade_repo = CustomerGradeRepository(db_session)
        customer_repo = CustomerRepository(db_session)

        grade = await grade_repo.create(make_grade(tenant_id))
        customer = make_customer(tenant_id)
        customer.grade_id = grade.id
        created = await customer_repo.create(customer)

        fetched = await customer_repo.get_by_id(tenant_id, created.id)
        assert fetched is not None
        assert fetched.grade_id == grade.id

    async def test_get_by_tenant_empty(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)

        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10)
        assert items == []
        assert total == 0


# ---------------------------------------------------------------------------
# ContactRepository
# ---------------------------------------------------------------------------


class TestContactRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        contact = make_contact(tenant_id, customer.id, name="Bob")
        created = await contact_repo.create(contact)

        fetched = await contact_repo.get_by_id(tenant_id, created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "Bob"
        assert fetched.customer_id == customer.id

    async def test_get_by_customer_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice"))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Bob"))

        contacts = await contact_repo.get_by_customer_id(tenant_id, customer.id)
        assert len(contacts) == 2
        names = {c.name for c in contacts}
        assert names == {"Alice", "Bob"}

    async def test_get_by_id_wrong_tenant_returns_none(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        other_tenant = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        contact = await contact_repo.create(make_contact(tenant_id, customer.id))

        result = await contact_repo.get_by_id(other_tenant, contact.id)
        assert result is None

    async def test_soft_delete_contact(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        contact = await contact_repo.create(make_contact(tenant_id, customer.id))

        await contact_repo.soft_delete(tenant_id, contact.id)
        fetched = await contact_repo.get_by_id(tenant_id, contact.id)
        assert fetched is None

    async def test_clear_primary(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        contact = make_contact(tenant_id, customer.id)
        contact.is_primary = True
        created = await contact_repo.create(contact)
        assert created.is_primary is True

        await contact_repo.clear_primary(tenant_id, customer.id)

        fetched = await contact_repo.get_by_id(tenant_id, created.id)
        assert fetched is not None
        assert fetched.is_primary is False

    async def test_update_contact(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        contact = await contact_repo.create(make_contact(tenant_id, customer.id, name="Old"))

        contact.name = "New"
        contact.email = "new@example.com"
        updated = await contact_repo.update(contact)

        assert updated.name == "New"
        assert updated.email == "new@example.com"

    async def test_get_by_customer_id_excludes_soft_deleted(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        c1 = await contact_repo.create(make_contact(tenant_id, customer.id, name="Keep"))
        c2 = await contact_repo.create(make_contact(tenant_id, customer.id, name="Delete"))

        await contact_repo.soft_delete(tenant_id, c2.id)
        contacts = await contact_repo.get_by_customer_id(tenant_id, customer.id)

        assert len(contacts) == 1
        assert contacts[0].id == c1.id

    async def test_get_by_customer_id_empty(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        contacts = await contact_repo.get_by_customer_id(tenant_id, customer.id)
        assert contacts == []


# ---------------------------------------------------------------------------
# TagRepository
# ---------------------------------------------------------------------------


class TestTagRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = TagRepository(db_session)
        tag = make_tag(tenant_id, name="VIP")

        created = await repo.create(tag)
        fetched = await repo.get_by_id(tenant_id, created.id)

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "VIP"
        assert fetched.tenant_id == tenant_id

    async def test_get_all(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = TagRepository(db_session)

        t1 = make_tag(tenant_id, name="Alpha")
        t1.position = 0
        t2 = make_tag(tenant_id, name="Beta")
        t2.position = 1
        await repo.create(t1)
        await repo.create(t2)

        tags = await repo.get_all(tenant_id)
        assert len(tags) == 2

    async def test_get_by_name_and_group_found(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = TagRepository(db_session)
        tag = make_tag(tenant_id, name="ImportantTag")
        tag.group_name = "Priority"
        await repo.create(tag)

        found = await repo.get_by_name_and_group(tenant_id, "ImportantTag", "Priority")
        assert found is not None
        assert found.name == "ImportantTag"
        assert found.group_name == "Priority"

    async def test_get_by_name_and_group_not_found(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = TagRepository(db_session)

        result = await repo.get_by_name_and_group(tenant_id, "Nonexistent", None)
        assert result is None

    async def test_add_to_customer_idempotent(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        tag_repo = TagRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        tag = await tag_repo.create(make_tag(tenant_id))

        # Adding same tag twice should not raise
        await tag_repo.add_to_customer(tenant_id, customer.id, tag.id)
        await tag_repo.add_to_customer(tenant_id, customer.id, tag.id)

        tags = await tag_repo.get_by_customer_id(tenant_id, customer.id)
        assert len(tags) == 1

    async def test_remove_from_customer(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        tag_repo = TagRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        tag = await tag_repo.create(make_tag(tenant_id))

        await tag_repo.add_to_customer(tenant_id, customer.id, tag.id)
        tags_before = await tag_repo.get_by_customer_id(tenant_id, customer.id)
        assert len(tags_before) == 1

        await tag_repo.remove_from_customer(tenant_id, customer.id, tag.id)
        tags_after = await tag_repo.get_by_customer_id(tenant_id, customer.id)
        assert len(tags_after) == 0

    async def test_get_by_customer_id_returns_tags(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        tag_repo = TagRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id))
        tag1 = await tag_repo.create(make_tag(tenant_id, name="Tag1"))
        tag2 = await tag_repo.create(make_tag(tenant_id, name="Tag2"))

        await tag_repo.add_to_customer(tenant_id, customer.id, tag1.id)
        await tag_repo.add_to_customer(tenant_id, customer.id, tag2.id)

        tags = await tag_repo.get_by_customer_id(tenant_id, customer.id)
        assert len(tags) == 2
        tag_names = {t.name for t in tags}
        assert tag_names == {"Tag1", "Tag2"}
