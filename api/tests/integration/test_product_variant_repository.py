import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import Product, ProductVariant
from app.infra.database.models.user import UserModel
from app.infra.database.repositories.product_repository import ProductRepository
from app.infra.database.repositories.product_variant_repository import ProductVariantRepository


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
def product_repo(db_session: AsyncSession):
    return ProductRepository(db_session)


@pytest.fixture
def variant_repo(db_session: AsyncSession):
    return ProductVariantRepository(db_session)


class TestProductVariantRepository:
    @pytest.fixture(autouse=True)
    async def _setup_user(self, db_session: AsyncSession, tenant_id: uuid.UUID) -> None:
        self._user_id = await _create_test_user(db_session, tenant_id)

    async def _create_product(self, repo: ProductRepository, tenant_id: uuid.UUID) -> Product:
        p = Product.create(name="Widget", tenant_id=tenant_id, created_by=self._user_id)
        return await repo.create(p)

    async def test_create_and_get_by_id(
        self, product_repo: ProductRepository, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID
    ) -> None:
        product = await self._create_product(product_repo, tenant_id)
        v = ProductVariant.create(
            product_id=product.id,
            variant_name="Red / L",
            tenant_id=tenant_id,
            color_code="#FF0000",
        )
        created = await variant_repo.create(v)
        result = await variant_repo.get_by_id(tenant_id, created.id)
        assert result is not None
        assert result.variant_name == "Red / L"
        assert result.color_code == "#FF0000"

    async def test_get_by_product_id(
        self, product_repo: ProductRepository, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID
    ) -> None:
        product = await self._create_product(product_repo, tenant_id)
        for name in ["Red / L", "Blue / M"]:
            v = ProductVariant.create(
                product_id=product.id,
                variant_name=name,
                tenant_id=tenant_id,
            )
            await variant_repo.create(v)
        variants = await variant_repo.get_by_product_id(tenant_id, product.id)
        assert len(variants) == 2

    async def test_update(
        self, product_repo: ProductRepository, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID
    ) -> None:
        product = await self._create_product(product_repo, tenant_id)
        v = ProductVariant.create(
            product_id=product.id,
            variant_name="Red / L",
            tenant_id=tenant_id,
        )
        created = await variant_repo.create(v)
        created.variant_name = "Red / XL"
        updated = await variant_repo.update(created)
        assert updated.variant_name == "Red / XL"

    async def test_delete(
        self, product_repo: ProductRepository, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID
    ) -> None:
        product = await self._create_product(product_repo, tenant_id)
        v = ProductVariant.create(
            product_id=product.id,
            variant_name="Red / L",
            tenant_id=tenant_id,
        )
        created = await variant_repo.create(v)
        await variant_repo.delete(tenant_id, created.id)
        result = await variant_repo.get_by_id(tenant_id, created.id)
        assert result is None

    async def test_get_by_sku(
        self, product_repo: ProductRepository, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID
    ) -> None:
        product = await self._create_product(product_repo, tenant_id)
        v = ProductVariant.create(
            product_id=product.id,
            variant_name="Red / L",
            tenant_id=tenant_id,
            sku="VAR-001",
        )
        await variant_repo.create(v)
        result = await variant_repo.get_by_sku(tenant_id, "VAR-001")
        assert result is not None
        assert result.variant_name == "Red / L"

    async def test_get_by_sku_not_found(self, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID) -> None:
        result = await variant_repo.get_by_sku(tenant_id, "NONEXIST")
        assert result is None

    async def test_tenant_isolation(
        self,
        product_repo: ProductRepository,
        variant_repo: ProductVariantRepository,
        db_session: AsyncSession,
        tenant_id: uuid.UUID,
    ) -> None:
        other_tenant = uuid.uuid7()
        product = await self._create_product(product_repo, tenant_id)
        v = ProductVariant.create(
            product_id=product.id,
            variant_name="Red / L",
            tenant_id=tenant_id,
        )
        created = await variant_repo.create(v)

        # Other tenant cannot see this variant
        result = await variant_repo.get_by_id(other_tenant, created.id)
        assert result is None

    async def test_independent_sku_and_cost(
        self, product_repo: ProductRepository, variant_repo: ProductVariantRepository, tenant_id: uuid.UUID
    ) -> None:
        """AC-0.6.3: variant has independent SKU + cost_price + color_code."""
        product = await self._create_product(product_repo, tenant_id)
        v = ProductVariant.create(
            product_id=product.id,
            variant_name="Red / L",
            tenant_id=tenant_id,
            sku="VAR-COST-001",
            cost_price=Decimal("25.50"),
            cost_currency="USD",
            color_code="#FF0000",
        )
        created = await variant_repo.create(v)
        result = await variant_repo.get_by_id(tenant_id, created.id)
        assert result is not None
        assert result.sku == "VAR-COST-001"
        assert result.cost_price == Decimal("25.50")
        assert result.cost_currency == "USD"
        assert result.color_code == "#FF0000"
