import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import Customer, CustomerGrade, Tag
from app.domain.customer.enums import FollowUpStage
from app.domain.customer.value_objects import CustomerFilter
from app.infra.database.repositories.customer_repository import (
    CustomerGradeRepository,
    CustomerRepository,
    TagRepository,
)


def make_customer(
    tenant_id: uuid.UUID,
    name: str = "Acme Corp",
    **kwargs: object,
) -> Customer:
    now = datetime.now(UTC)
    defaults: dict[str, object] = {
        "id": uuid.uuid7(),
        "tenant_id": tenant_id,
        "name": name,
        "follow_status": FollowUpStage.NEW,
        "custom_fields": {},
        "created_at": now,
        "updated_at": now,
    }
    defaults.update(kwargs)
    return Customer(**defaults)  # type: ignore[arg-type]


def make_grade(tenant_id: uuid.UUID, name: str = "A") -> CustomerGrade:
    now = datetime.now(UTC)
    return CustomerGrade(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        name=name,
        color="#22C55E",
        position=0,
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


class TestCustomerRepoFilter:
    async def test_no_filter_backward_compatible(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Alpha"))
        await repo.create(make_customer(tenant_id, name="Beta"))

        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10)
        assert total == 2
        assert len(items) == 2

    async def test_keyword_search(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Acme Corporation"))
        await repo.create(make_customer(tenant_id, name="Globex Inc"))

        # pg_trgm % operator uses similarity threshold (default 0.3)
        # "Acme Corp" is similar enough to "Acme Corporation"
        filters = CustomerFilter(keyword="Acme Corp")
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Acme Corporation"

    async def test_source_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="A", source="alibaba"))
        await repo.create(make_customer(tenant_id, name="B", source="exhibition"))

        filters = CustomerFilter(source="alibaba")
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "A"

    async def test_country_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="US Co", country="US"))
        await repo.create(make_customer(tenant_id, name="CN Co", country="CN"))

        filters = CustomerFilter(country="US")
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "US Co"

    async def test_grade_id_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        grade_repo = CustomerGradeRepository(db_session)
        grade = await grade_repo.create(make_grade(tenant_id, name="Gold"))

        c1 = make_customer(tenant_id, name="Graded")
        c1.grade_id = grade.id
        await repo.create(c1)
        await repo.create(make_customer(tenant_id, name="Ungraded"))

        filters = CustomerFilter(grade_id=grade.id)
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Graded"

    async def test_follow_status_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="New One", follow_status=FollowUpStage.NEW))
        await repo.create(make_customer(tenant_id, name="Quoted One", follow_status=FollowUpStage.QUOTED))

        filters = CustomerFilter(follow_status=FollowUpStage.QUOTED)
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Quoted One"

    async def test_industry_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Tech Co", industry="technology"))
        await repo.create(make_customer(tenant_id, name="Farm Co", industry="agriculture"))

        filters = CustomerFilter(industry="technology")
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Tech Co"

    async def test_tag_ids_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        tag_repo = TagRepository(db_session)

        tag = await tag_repo.create(make_tag(tenant_id, name="VIP"))
        c1 = await repo.create(make_customer(tenant_id, name="Tagged"))
        await repo.create(make_customer(tenant_id, name="Untagged"))
        await tag_repo.add_to_customer(tenant_id, c1.id, tag.id)

        filters = CustomerFilter(tag_ids=[tag.id])
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Tagged"

    async def test_multiple_conditions_combined(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Match", country="US", source="alibaba"))
        await repo.create(make_customer(tenant_id, name="Wrong Country", country="CN", source="alibaba"))
        await repo.create(make_customer(tenant_id, name="Wrong Source", country="US", source="exhibition"))

        filters = CustomerFilter(country="US", source="alibaba")
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Match"

    async def test_sort_by_name_asc(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_id, name="Charlie"))
        await repo.create(make_customer(tenant_id, name="Alice"))
        await repo.create(make_customer(tenant_id, name="Bob"))

        filters = CustomerFilter(sort_by="name", sort="asc")
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 3
        assert [c.name for c in items] == ["Alice", "Bob", "Charlie"]

    async def test_date_range_filter_last_follow_at(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = CustomerRepository(db_session)
        now = datetime.now(UTC)
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)

        await repo.create(make_customer(tenant_id, name="Recent", last_follow_at=yesterday))
        await repo.create(make_customer(tenant_id, name="Old", last_follow_at=last_week))

        filters = CustomerFilter(
            last_follow_at_from=now - timedelta(days=2),
            last_follow_at_to=now,
        )
        items, total = await repo.get_by_tenant(tenant_id, page=1, page_size=10, filters=filters)
        assert total == 1
        assert items[0].name == "Recent"

    async def test_tenant_isolation(self, db_session: AsyncSession) -> None:
        tenant_a = uuid.uuid7()
        tenant_b = uuid.uuid7()
        repo = CustomerRepository(db_session)
        await repo.create(make_customer(tenant_a, name="A Corp"))
        await repo.create(make_customer(tenant_b, name="B Corp"))

        items_a, total_a = await repo.get_by_tenant(tenant_a, page=1, page_size=10)
        items_b, total_b = await repo.get_by_tenant(tenant_b, page=1, page_size=10)

        assert total_a == 1
        assert total_b == 1
        assert items_a[0].name == "A Corp"
        assert items_b[0].name == "B Corp"
