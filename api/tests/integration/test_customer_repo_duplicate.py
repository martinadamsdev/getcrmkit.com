import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import Contact, Customer
from app.domain.customer.enums import FollowUpStage
from app.infra.database.repositories.customer_repository import (
    ContactRepository,
    CustomerRepository,
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


def make_contact(
    tenant_id: uuid.UUID,
    customer_id: uuid.UUID,
    name: str = "Alice",
    email: str | None = None,
) -> Contact:
    now = datetime.now(UTC)
    return Contact(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        customer_id=customer_id,
        name=name,
        email=email,
        custom_fields={},
        created_at=now,
        updated_at=now,
    )


class TestFindByNameExact:
    async def test_case_insensitive_match(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Acme Corp"))

        results = await repo.find_by_name_exact(tenant_id, "acme corp")
        assert len(results) == 1
        assert results[0].name == "Acme Corp"

    async def test_whitespace_trimmed(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Acme Corp"))

        results = await repo.find_by_name_exact(tenant_id, "  Acme Corp  ")
        assert len(results) == 1

    async def test_no_match(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Acme Corp"))

        results = await repo.find_by_name_exact(tenant_id, "Globex Inc")
        assert len(results) == 0

    async def test_exclude_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        c1 = await repo.create(make_customer(tenant_id, name="Acme Corp"))
        await repo.create(make_customer(tenant_id, name="Acme Corp"))

        results = await repo.find_by_name_exact(tenant_id, "Acme Corp", exclude_id=c1.id)
        assert len(results) == 1
        assert results[0].id != c1.id

    async def test_soft_deleted_excluded(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        customer = await repo.create(make_customer(tenant_id, name="Acme Corp"))
        await repo.soft_delete(tenant_id, customer.id)

        results = await repo.find_by_name_exact(tenant_id, "Acme Corp")
        assert len(results) == 0


class TestFindByEmailDomain:
    async def test_find_by_domain(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id, name="Acme"))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice", email="alice@acme.com"))

        results = await customer_repo.find_by_email_domain(tenant_id, "acme.com")
        assert len(results) == 1
        assert results[0].name == "Acme"

    async def test_no_match(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id, name="Acme"))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice", email="alice@acme.com"))

        results = await customer_repo.find_by_email_domain(tenant_id, "other.com")
        assert len(results) == 0

    async def test_exclude_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        c1 = await customer_repo.create(make_customer(tenant_id, name="Acme 1"))
        c2 = await customer_repo.create(make_customer(tenant_id, name="Acme 2"))
        await contact_repo.create(make_contact(tenant_id, c1.id, name="Alice", email="alice@acme.com"))
        await contact_repo.create(make_contact(tenant_id, c2.id, name="Bob", email="bob@acme.com"))

        results = await customer_repo.find_by_email_domain(tenant_id, "acme.com", exclude_id=c1.id)
        assert len(results) == 1
        assert results[0].id == c2.id

    async def test_soft_deleted_contact_excluded(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id, name="Acme"))
        contact = await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice", email="alice@acme.com"))
        await contact_repo.soft_delete(tenant_id, contact.id)

        results = await customer_repo.find_by_email_domain(tenant_id, "acme.com")
        assert len(results) == 0

    async def test_soft_deleted_customer_excluded(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id, name="Acme"))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice", email="alice@acme.com"))
        await customer_repo.soft_delete(tenant_id, customer.id)

        results = await customer_repo.find_by_email_domain(tenant_id, "acme.com")
        assert len(results) == 0


class TestFindByEmailExact:
    async def test_find_by_exact_email(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id, name="Acme"))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice", email="alice@acme.com"))

        results = await customer_repo.find_by_email_exact(tenant_id, "alice@acme.com")
        assert len(results) == 1
        assert results[0].name == "Acme"

    async def test_no_match(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        customer = await customer_repo.create(make_customer(tenant_id, name="Acme"))
        await contact_repo.create(make_contact(tenant_id, customer.id, name="Alice", email="alice@acme.com"))

        results = await customer_repo.find_by_email_exact(tenant_id, "bob@acme.com")
        assert len(results) == 0

    async def test_exclude_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        contact_repo = ContactRepository(db_session)

        c1 = await customer_repo.create(make_customer(tenant_id, name="Acme 1"))
        c2 = await customer_repo.create(make_customer(tenant_id, name="Acme 2"))
        await contact_repo.create(make_contact(tenant_id, c1.id, name="Alice", email="shared@acme.com"))
        await contact_repo.create(make_contact(tenant_id, c2.id, name="Bob", email="shared@acme.com"))

        results = await customer_repo.find_by_email_exact(tenant_id, "shared@acme.com", exclude_id=c1.id)
        assert len(results) == 1
        assert results[0].id == c2.id


class TestCountByTenant:
    async def test_count(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="A"))
        await repo.create(make_customer(tenant_id, name="B"))

        count = await repo.count_by_tenant(tenant_id)
        assert count == 2

    async def test_count_excludes_soft_deleted(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="A"))
        c2 = await repo.create(make_customer(tenant_id, name="B"))
        await repo.soft_delete(tenant_id, c2.id)

        count = await repo.count_by_tenant(tenant_id)
        assert count == 1

    async def test_count_empty(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)

        count = await repo.count_by_tenant(tenant_id)
        assert count == 0
