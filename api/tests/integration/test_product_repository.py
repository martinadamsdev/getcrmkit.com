import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import Product
from app.domain.product.value_objects import ProductFilter
from app.infra.database.models.user import UserModel
from app.infra.database.repositories.product_repository import ProductRepository


async def _create_test_user(session: AsyncSession, tenant_id: uuid.UUID) -> uuid.UUID:
    """Create a minimal user row to satisfy FK constraints."""
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
def product_repo(db_session: AsyncSession):
    return ProductRepository(db_session)


async def _create_product(
    repo: ProductRepository, tenant_id: uuid.UUID, user_id: uuid.UUID, name: str = "Widget", **kwargs
) -> Product:
    p = Product.create(name=name, tenant_id=tenant_id, created_by=user_id, **kwargs)
    return await repo.create(p)


class TestProductRepository:
    @pytest.fixture(autouse=True)
    async def _setup_user(self, db_session: AsyncSession, tenant_id: uuid.UUID) -> None:
        self._user_id = await _create_test_user(db_session, tenant_id)

    async def test_create_and_get_by_id(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        p = await _create_product(product_repo, tenant_id, self._user_id)
        result = await product_repo.get_by_id(tenant_id, p.id)
        assert result is not None
        assert result.name == "Widget"

    async def test_get_by_id_not_found(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        result = await product_repo.get_by_id(tenant_id, uuid.uuid7())
        assert result is None

    async def test_get_by_tenant(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="A")
        await _create_product(product_repo, tenant_id, self._user_id, name="B")
        items, total = await product_repo.get_by_tenant(tenant_id)
        assert total == 2

    async def test_keyword_filter(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="Acme Widget")
        await _create_product(product_repo, tenant_id, self._user_id, name="Beta Gadget")
        f = ProductFilter(keyword="Widget")
        items, total = await product_repo.get_by_tenant(tenant_id, filters=f)
        assert total == 1
        assert items[0].name == "Acme Widget"

    async def test_is_active_filter(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="Active", is_active=True)
        await _create_product(product_repo, tenant_id, self._user_id, name="Inactive", is_active=False)
        f = ProductFilter(is_active=True)
        items, total = await product_repo.get_by_tenant(tenant_id, filters=f)
        assert total == 1
        assert items[0].name == "Active"

    async def test_selling_price_range_filter(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="Cheap", selling_price=Decimal("5.00"))
        await _create_product(product_repo, tenant_id, self._user_id, name="Expensive", selling_price=Decimal("100.00"))
        f = ProductFilter(min_selling=Decimal("50.00"))
        items, total = await product_repo.get_by_tenant(tenant_id, filters=f)
        assert total == 1
        assert items[0].name == "Expensive"

    async def test_sort_by_name_asc(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="Zeta")
        await _create_product(product_repo, tenant_id, self._user_id, name="Alpha")
        f = ProductFilter(sort_by="name", sort="asc")
        items, _ = await product_repo.get_by_tenant(tenant_id, filters=f)
        assert items[0].name == "Alpha"
        assert items[1].name == "Zeta"

    async def test_update(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        p = await _create_product(product_repo, tenant_id, self._user_id)
        p.name = "Updated Widget"
        result = await product_repo.update(p)
        assert result.name == "Updated Widget"

    async def test_soft_delete(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        p = await _create_product(product_repo, tenant_id, self._user_id)
        await product_repo.soft_delete(tenant_id, p.id)
        result = await product_repo.get_by_id(tenant_id, p.id)
        assert result is None

    async def test_get_by_sku(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="SKU Product", sku="SKU-001")
        result = await product_repo.get_by_sku(tenant_id, "SKU-001")
        assert result is not None
        assert result.name == "SKU Product"

    async def test_get_by_sku_not_found(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        result = await product_repo.get_by_sku(tenant_id, "NONEXIST")
        assert result is None

    async def test_count_by_tenant(self, product_repo: ProductRepository, tenant_id: uuid.UUID) -> None:
        await _create_product(product_repo, tenant_id, self._user_id, name="A")
        await _create_product(product_repo, tenant_id, self._user_id, name="B")
        count = await product_repo.count_by_tenant(tenant_id)
        assert count == 2

    async def test_get_by_category(
        self, product_repo: ProductRepository, db_session: AsyncSession, tenant_id: uuid.UUID
    ) -> None:
        # Create a real category to satisfy FK
        from app.domain.product.entities import ProductCategory
        from app.infra.database.repositories.product_category_repository import ProductCategoryRepository

        cat_repo = ProductCategoryRepository(db_session)
        cat = ProductCategory(tenant_id=tenant_id, name="TestCat")
        cat = await cat_repo.create(cat)

        await _create_product(product_repo, tenant_id, self._user_id, name="In Category", category_id=cat.id)
        await _create_product(product_repo, tenant_id, self._user_id, name="No Category")
        items = await product_repo.get_by_category(tenant_id, cat.id)
        assert len(items) == 1
        assert items[0].name == "In Category"

    async def test_tenant_isolation(
        self, product_repo: ProductRepository, db_session: AsyncSession, tenant_id: uuid.UUID
    ) -> None:
        other_tenant = uuid.uuid7()
        other_user_id = await _create_test_user(db_session, other_tenant)
        await _create_product(product_repo, tenant_id, self._user_id, name="Mine")
        await _create_product(product_repo, other_tenant, other_user_id, name="Other")
        items, total = await product_repo.get_by_tenant(tenant_id)
        assert total == 1
        assert items[0].name == "Mine"
