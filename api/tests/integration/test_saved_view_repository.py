import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import SavedView
from app.infra.database.repositories.saved_view_repository import SavedViewRepository


def make_view(
    tenant_id: uuid.UUID,
    user_id: uuid.UUID,
    name: str = "My View",
    position: int = 0,
) -> SavedView:
    now = datetime.now(UTC)
    return SavedView(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        user_id=user_id,
        entity_type="customer",
        name=name,
        filter_config={"country": "US"},
        is_default=False,
        position=position,
        created_at=now,
        updated_at=now,
    )


class TestSavedViewRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        view = make_view(tenant_id, user_id, name="US Customers")
        created = await repo.create(view)

        fetched = await repo.get_by_id(tenant_id, user_id, created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "US Customers"
        assert fetched.filter_config == {"country": "US"}

    async def test_get_by_id_wrong_user_returns_none(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        other_user = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        view = await repo.create(make_view(tenant_id, user_id))
        result = await repo.get_by_id(tenant_id, other_user, view.id)
        assert result is None

    async def test_get_all_ordered_by_position(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        await repo.create(make_view(tenant_id, user_id, name="C", position=2))
        await repo.create(make_view(tenant_id, user_id, name="A", position=0))
        await repo.create(make_view(tenant_id, user_id, name="B", position=1))

        views = await repo.get_all(tenant_id, user_id, "customer")
        assert len(views) == 3
        assert [v.name for v in views] == ["A", "B", "C"]

    async def test_update(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        view = await repo.create(make_view(tenant_id, user_id, name="Old"))
        view.name = "New"
        view.is_default = True
        view.updated_at = datetime.now(UTC)
        updated = await repo.update(view)

        assert updated.name == "New"
        assert updated.is_default is True

        fetched = await repo.get_by_id(tenant_id, user_id, view.id)
        assert fetched is not None
        assert fetched.name == "New"

    async def test_delete(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        view = await repo.create(make_view(tenant_id, user_id))
        await repo.delete(tenant_id, user_id, view.id)

        fetched = await repo.get_by_id(tenant_id, user_id, view.id)
        assert fetched is None

    async def test_get_by_name(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        await repo.create(make_view(tenant_id, user_id, name="US Customers"))

        found = await repo.get_by_name(tenant_id, user_id, "customer", "US Customers")
        assert found is not None
        assert found.name == "US Customers"

    async def test_get_by_name_not_found(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        result = await repo.get_by_name(tenant_id, user_id, "customer", "Nonexistent")
        assert result is None

    async def test_tenant_and_user_isolation(self, db_session: AsyncSession) -> None:
        tenant_a = uuid.uuid7()
        tenant_b = uuid.uuid7()
        user_a = uuid.uuid7()
        user_b = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        await repo.create(make_view(tenant_a, user_a, name="View A"))
        await repo.create(make_view(tenant_b, user_b, name="View B"))

        views_a = await repo.get_all(tenant_a, user_a, "customer")
        views_b = await repo.get_all(tenant_b, user_b, "customer")

        assert len(views_a) == 1
        assert views_a[0].name == "View A"
        assert len(views_b) == 1
        assert views_b[0].name == "View B"

    async def test_get_all_empty(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        repo = SavedViewRepository(db_session)

        views = await repo.get_all(tenant_id, user_id, "customer")
        assert views == []
