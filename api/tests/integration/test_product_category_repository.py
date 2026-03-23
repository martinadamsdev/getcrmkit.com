import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import Product, ProductCategory
from app.infra.database.models.user import UserModel
from app.infra.database.repositories.product_category_repository import ProductCategoryRepository
from app.infra.database.repositories.product_repository import ProductRepository


async def _create_test_user(session: AsyncSession, tenant_id: uuid.UUID) -> uuid.UUID:
    now = datetime.now(UTC)
    user_id = uuid.uuid7()
    user = UserModel(
        id=user_id,
        tenant_id=tenant_id,
        email=f"test-{user_id}@example.com",
        password_hash="hashed",
        name="Test User",
        created_at=now,
        updated_at=now,
    )
    session.add(user)
    await session.flush()
    return user_id


@pytest.fixture
def tenant_id():
    return uuid.uuid7()


@pytest.fixture
def category_repo(db_session: AsyncSession):
    return ProductCategoryRepository(db_session)


def _make_category(tenant_id: uuid.UUID, name: str = "Electronics", **kwargs) -> ProductCategory:
    return ProductCategory(
        tenant_id=tenant_id,
        name=name,
        **kwargs,
    )


class TestProductCategoryRepository:
    async def test_create_and_get_by_id(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        cat = _make_category(tenant_id, name="Electronics")
        created = await category_repo.create(cat)
        result = await category_repo.get_by_id(tenant_id, created.id)
        assert result is not None
        assert result.name == "Electronics"
        assert result.level == 1

    async def test_get_by_id_not_found(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        result = await category_repo.get_by_id(tenant_id, uuid.uuid7())
        assert result is None

    async def test_get_all(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        await category_repo.create(_make_category(tenant_id, name="A", position=1))
        await category_repo.create(_make_category(tenant_id, name="B", position=0))
        categories = await category_repo.get_all(tenant_id)
        assert len(categories) == 2
        # Sorted by level then position
        assert categories[0].name == "B"
        assert categories[1].name == "A"

    async def test_get_children(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        parent = await category_repo.create(_make_category(tenant_id, name="Parent"))
        child1 = _make_category(tenant_id, name="Child1", parent_id=parent.id, level=2, position=1)
        child2 = _make_category(tenant_id, name="Child2", parent_id=parent.id, level=2, position=0)
        await category_repo.create(child1)
        await category_repo.create(child2)
        children = await category_repo.get_children(tenant_id, parent.id)
        assert len(children) == 2
        # Sorted by position
        assert children[0].name == "Child2"
        assert children[1].name == "Child1"

    async def test_get_tree(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        """get_tree returns all categories sorted by level + position."""
        parent = await category_repo.create(_make_category(tenant_id, name="Root", position=0))
        child = _make_category(tenant_id, name="Child", parent_id=parent.id, level=2, position=0)
        await category_repo.create(child)
        tree = await category_repo.get_tree(tenant_id)
        assert len(tree) == 2
        assert tree[0].level == 1
        assert tree[1].level == 2

    async def test_update(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        cat = await category_repo.create(_make_category(tenant_id, name="Old"))
        cat.name = "New"
        updated = await category_repo.update(cat)
        assert updated.name == "New"

    async def test_delete(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        cat = await category_repo.create(_make_category(tenant_id, name="ToDelete"))
        await category_repo.delete(tenant_id, cat.id)
        result = await category_repo.get_by_id(tenant_id, cat.id)
        assert result is None

    async def test_has_products_true(
        self, category_repo: ProductCategoryRepository, db_session: AsyncSession, tenant_id: uuid.UUID
    ) -> None:
        user_id = await _create_test_user(db_session, tenant_id)
        cat = await category_repo.create(_make_category(tenant_id, name="WithProducts"))
        product_repo = ProductRepository(db_session)
        p = Product.create(name="In Category", tenant_id=tenant_id, created_by=user_id, category_id=cat.id)
        await product_repo.create(p)
        assert await category_repo.has_products(tenant_id, cat.id) is True

    async def test_has_products_false(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        cat = await category_repo.create(_make_category(tenant_id, name="Empty"))
        assert await category_repo.has_products(tenant_id, cat.id) is False

    async def test_has_children_true(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        parent = await category_repo.create(_make_category(tenant_id, name="Parent"))
        child = _make_category(tenant_id, name="Child", parent_id=parent.id, level=2)
        await category_repo.create(child)
        assert await category_repo.has_children(tenant_id, parent.id) is True

    async def test_has_children_false(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        cat = await category_repo.create(_make_category(tenant_id, name="Leaf"))
        assert await category_repo.has_children(tenant_id, cat.id) is False

    async def test_tenant_isolation(self, category_repo: ProductCategoryRepository, tenant_id: uuid.UUID) -> None:
        other_tenant = uuid.uuid7()
        await category_repo.create(_make_category(tenant_id, name="Mine"))
        await category_repo.create(_make_category(other_tenant, name="Other"))
        categories = await category_repo.get_all(tenant_id)
        assert len(categories) == 1
        assert categories[0].name == "Mine"
