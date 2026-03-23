import uuid
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.domain.product.entities import CustomizationOption, Product, ProductCategory, ProductVariant
from app.domain.product.exceptions import (
    CategoryHasChildrenError,
    CategoryInUseError,
    CategoryNotFoundError,
    CustomizationOptionNotFoundError,
    MaxCategoryDepthError,
    PricingTierNotFoundError,
    ProductNotFoundError,
    VariantNotFoundError,
)
from app.domain.product.services import (
    CustomizationOptionService,
    PricingTierService,
    ProductCategoryService,
    ProductService,
    ProductVariantService,
)

# --- ProductService ---


@pytest.fixture
def product_repo():
    repo = AsyncMock()
    repo.create = AsyncMock(side_effect=lambda p: p)
    repo.update = AsyncMock(side_effect=lambda p: p)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.soft_delete = AsyncMock()
    repo.get_by_tenant = AsyncMock(return_value=([], 0))
    return repo


class TestProductService:
    async def test_create_product(self, product_repo):
        svc = ProductService(product_repo=product_repo)
        p = await svc.create_product(
            name="Widget",
            tenant_id=uuid.uuid7(),
            created_by=uuid.uuid7(),
        )
        assert p.name == "Widget"
        product_repo.create.assert_called_once()

    async def test_get_product(self, product_repo):
        existing = Product.create(name="Widget", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        product_repo.get_by_id.return_value = existing
        svc = ProductService(product_repo=product_repo)
        result = await svc.get_product(tenant_id=existing.tenant_id, product_id=existing.id)
        assert result.name == "Widget"

    async def test_get_product_not_found_raises(self, product_repo):
        svc = ProductService(product_repo=product_repo)
        with pytest.raises(ProductNotFoundError):
            await svc.get_product(tenant_id=uuid.uuid7(), product_id=uuid.uuid7())

    async def test_update_product(self, product_repo):
        existing = Product.create(name="Widget", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        product_repo.get_by_id.return_value = existing
        svc = ProductService(product_repo=product_repo)
        result = await svc.update_product(
            tenant_id=existing.tenant_id,
            product_id=existing.id,
            name="Widget Pro",
        )
        assert result.name == "Widget Pro"

    async def test_soft_delete_product(self, product_repo):
        existing = Product.create(name="Widget", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        product_repo.get_by_id.return_value = existing
        svc = ProductService(product_repo=product_repo)
        await svc.soft_delete_product(tenant_id=existing.tenant_id, product_id=existing.id)
        product_repo.soft_delete.assert_called_once()

    async def test_soft_delete_not_found_raises(self, product_repo):
        svc = ProductService(product_repo=product_repo)
        with pytest.raises(ProductNotFoundError):
            await svc.soft_delete_product(tenant_id=uuid.uuid7(), product_id=uuid.uuid7())

    async def test_list_products(self, product_repo):
        product_repo.get_by_tenant.return_value = ([], 0)
        svc = ProductService(product_repo=product_repo)
        items, total = await svc.list_products(tenant_id=uuid.uuid7())
        assert items == []
        assert total == 0


# --- ProductVariantService ---


@pytest.fixture
def variant_repo():
    repo = AsyncMock()
    repo.create = AsyncMock(side_effect=lambda v: v)
    repo.update = AsyncMock(side_effect=lambda v: v)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.get_by_product_id = AsyncMock(return_value=[])
    repo.delete = AsyncMock()
    return repo


class TestProductVariantService:
    async def test_create_variant(self, product_repo, variant_repo):
        existing_product = Product.create(name="Widget", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        product_repo.get_by_id.return_value = existing_product
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        v = await svc.create_variant(
            product_id=existing_product.id,
            variant_name="Red / Large",
            tenant_id=existing_product.tenant_id,
        )
        assert v.variant_name == "Red / Large"
        variant_repo.create.assert_called_once()

    async def test_create_variant_product_not_found(self, product_repo, variant_repo):
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        with pytest.raises(ProductNotFoundError):
            await svc.create_variant(
                product_id=uuid.uuid7(),
                variant_name="Red / Large",
                tenant_id=uuid.uuid7(),
            )

    async def test_get_variant(self, product_repo, variant_repo):
        existing = ProductVariant.create(product_id=uuid.uuid7(), variant_name="X", tenant_id=uuid.uuid7())
        variant_repo.get_by_id.return_value = existing
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        result = await svc.get_variant(tenant_id=existing.tenant_id, variant_id=existing.id)
        assert result.variant_name == "X"

    async def test_get_variant_not_found(self, product_repo, variant_repo):
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        with pytest.raises(VariantNotFoundError):
            await svc.get_variant(tenant_id=uuid.uuid7(), variant_id=uuid.uuid7())

    async def test_update_variant(self, product_repo, variant_repo):
        existing = ProductVariant.create(product_id=uuid.uuid7(), variant_name="X", tenant_id=uuid.uuid7())
        variant_repo.get_by_id.return_value = existing
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        result = await svc.update_variant(tenant_id=existing.tenant_id, variant_id=existing.id, variant_name="Y")
        assert result.variant_name == "Y"

    async def test_update_variant_not_found(self, product_repo, variant_repo):
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        with pytest.raises(VariantNotFoundError):
            await svc.update_variant(tenant_id=uuid.uuid7(), variant_id=uuid.uuid7(), variant_name="Y")

    async def test_delete_variant(self, product_repo, variant_repo):
        existing = ProductVariant.create(product_id=uuid.uuid7(), variant_name="X", tenant_id=uuid.uuid7())
        variant_repo.get_by_id.return_value = existing
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        await svc.delete_variant(tenant_id=existing.tenant_id, variant_id=existing.id)
        variant_repo.delete.assert_called_once()

    async def test_delete_variant_not_found(self, product_repo, variant_repo):
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        with pytest.raises(VariantNotFoundError):
            await svc.delete_variant(tenant_id=uuid.uuid7(), variant_id=uuid.uuid7())

    async def test_list_by_product(self, product_repo, variant_repo):
        svc = ProductVariantService(variant_repo=variant_repo, product_repo=product_repo)
        result = await svc.list_by_product(tenant_id=uuid.uuid7(), product_id=uuid.uuid7())
        assert result == []


# --- ProductCategoryService ---


@pytest.fixture
def category_repo():
    repo = AsyncMock()
    repo.create = AsyncMock(side_effect=lambda c: c)
    repo.update = AsyncMock(side_effect=lambda c: c)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.delete = AsyncMock()
    repo.get_all = AsyncMock(return_value=[])
    repo.has_children = AsyncMock(return_value=False)
    repo.has_products = AsyncMock(return_value=False)
    return repo


class TestProductCategoryService:
    async def test_create_root_category(self, category_repo):
        svc = ProductCategoryService(category_repo=category_repo)
        cat = await svc.create_category(
            name="Electronics",
            tenant_id=uuid.uuid7(),
        )
        assert cat.name == "Electronics"
        assert cat.level == 1
        category_repo.create.assert_called_once()

    async def test_create_child_category(self, category_repo):
        parent = ProductCategory(name="Electronics", level=1, tenant_id=uuid.uuid7())
        category_repo.get_by_id.return_value = parent
        svc = ProductCategoryService(category_repo=category_repo)
        cat = await svc.create_category(
            name="Phones",
            tenant_id=parent.tenant_id,
            parent_id=parent.id,
        )
        assert cat.level == 2
        assert cat.parent_id == parent.id

    async def test_create_exceeds_depth_raises(self, category_repo):
        parent = ProductCategory(name="Level 3", level=3, tenant_id=uuid.uuid7())
        category_repo.get_by_id.return_value = parent
        svc = ProductCategoryService(category_repo=category_repo)
        with pytest.raises(MaxCategoryDepthError):
            await svc.create_category(
                name="Level 4",
                tenant_id=parent.tenant_id,
                parent_id=parent.id,
            )

    async def test_create_with_invalid_parent_raises(self, category_repo):
        svc = ProductCategoryService(category_repo=category_repo)
        with pytest.raises(CategoryNotFoundError):
            await svc.create_category(
                name="Orphan",
                tenant_id=uuid.uuid7(),
                parent_id=uuid.uuid7(),
            )

    async def test_delete_category(self, category_repo):
        existing = ProductCategory(name="Electronics", tenant_id=uuid.uuid7())
        category_repo.get_by_id.return_value = existing
        svc = ProductCategoryService(category_repo=category_repo)
        await svc.delete_category(tenant_id=existing.tenant_id, category_id=existing.id)
        category_repo.delete.assert_called_once()

    async def test_delete_not_found_raises(self, category_repo):
        svc = ProductCategoryService(category_repo=category_repo)
        with pytest.raises(CategoryNotFoundError):
            await svc.delete_category(tenant_id=uuid.uuid7(), category_id=uuid.uuid7())

    async def test_delete_with_children_raises(self, category_repo):
        existing = ProductCategory(name="Electronics", tenant_id=uuid.uuid7())
        category_repo.get_by_id.return_value = existing
        category_repo.has_children.return_value = True
        svc = ProductCategoryService(category_repo=category_repo)
        with pytest.raises(CategoryHasChildrenError):
            await svc.delete_category(tenant_id=existing.tenant_id, category_id=existing.id)

    async def test_delete_with_products_raises(self, category_repo):
        existing = ProductCategory(name="Electronics", tenant_id=uuid.uuid7())
        category_repo.get_by_id.return_value = existing
        category_repo.has_products.return_value = True
        svc = ProductCategoryService(category_repo=category_repo)
        with pytest.raises(CategoryInUseError):
            await svc.delete_category(tenant_id=existing.tenant_id, category_id=existing.id)

    async def test_update_category(self, category_repo):
        existing = ProductCategory(name="Electronics", tenant_id=uuid.uuid7())
        category_repo.get_by_id.return_value = existing
        svc = ProductCategoryService(category_repo=category_repo)
        result = await svc.update_category(tenant_id=existing.tenant_id, category_id=existing.id, name="Electronics V2")
        assert result.name == "Electronics V2"

    async def test_update_not_found_raises(self, category_repo):
        svc = ProductCategoryService(category_repo=category_repo)
        with pytest.raises(CategoryNotFoundError):
            await svc.update_category(tenant_id=uuid.uuid7(), category_id=uuid.uuid7(), name="X")


# --- PricingTierService ---


@pytest.fixture
def tier_repo():
    repo = AsyncMock()
    repo.create = AsyncMock(side_effect=lambda t: t)
    repo.update = AsyncMock(side_effect=lambda t: t)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.get_all = AsyncMock(return_value=[])
    repo.delete = AsyncMock()
    return repo


class TestPricingTierService:
    async def test_create_tier(self, tier_repo):
        svc = PricingTierService(pricing_tier_repo=tier_repo)
        tier = await svc.create_tier(
            tenant_id=uuid.uuid7(),
            min_qty=1,
            max_qty=99,
            multiplier=Decimal("1.5000"),
        )
        assert tier.min_qty == 1
        assert tier.multiplier == Decimal("1.5000")
        tier_repo.create.assert_called_once()

    async def test_update_tier(self, tier_repo):
        from app.domain.product.entities import PricingTier

        existing = PricingTier(min_qty=1, max_qty=99, multiplier=Decimal("1.5000"), tenant_id=uuid.uuid7())
        tier_repo.get_by_id.return_value = existing
        svc = PricingTierService(pricing_tier_repo=tier_repo)
        result = await svc.update_tier(tenant_id=existing.tenant_id, tier_id=existing.id, multiplier=Decimal("1.8000"))
        assert result.multiplier == Decimal("1.8000")

    async def test_update_not_found_raises(self, tier_repo):
        svc = PricingTierService(pricing_tier_repo=tier_repo)
        with pytest.raises(PricingTierNotFoundError):
            await svc.update_tier(tenant_id=uuid.uuid7(), tier_id=uuid.uuid7(), multiplier=Decimal("1.0"))

    async def test_delete_tier(self, tier_repo):
        from app.domain.product.entities import PricingTier

        existing = PricingTier(min_qty=1, max_qty=99, multiplier=Decimal("1.5000"), tenant_id=uuid.uuid7())
        tier_repo.get_by_id.return_value = existing
        svc = PricingTierService(pricing_tier_repo=tier_repo)
        await svc.delete_tier(tenant_id=existing.tenant_id, tier_id=existing.id)
        tier_repo.delete.assert_called_once()

    async def test_delete_not_found_raises(self, tier_repo):
        svc = PricingTierService(pricing_tier_repo=tier_repo)
        with pytest.raises(PricingTierNotFoundError):
            await svc.delete_tier(tenant_id=uuid.uuid7(), tier_id=uuid.uuid7())

    async def test_get_all(self, tier_repo):
        svc = PricingTierService(pricing_tier_repo=tier_repo)
        result = await svc.get_all(tenant_id=uuid.uuid7())
        assert result == []


# --- CustomizationOptionService ---


@pytest.fixture
def option_repo():
    repo = AsyncMock()
    repo.create = AsyncMock(side_effect=lambda o: o)
    repo.update = AsyncMock(side_effect=lambda o: o)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.delete = AsyncMock()
    repo.get_all = AsyncMock(return_value=[])
    return repo


class TestCustomizationOptionService:
    async def test_create_option(self, option_repo):
        svc = CustomizationOptionService(option_repo=option_repo)
        opt = await svc.create_option(
            name="Logo Printing",
            tenant_id=uuid.uuid7(),
            extra_cost=Decimal("3.00"),
        )
        assert opt.name == "Logo Printing"
        option_repo.create.assert_called_once()

    async def test_update_option(self, option_repo):
        existing = CustomizationOption.create(name="Logo", tenant_id=uuid.uuid7())
        option_repo.get_by_id.return_value = existing
        svc = CustomizationOptionService(option_repo=option_repo)
        result = await svc.update_option(
            tenant_id=existing.tenant_id,
            option_id=existing.id,
            name="Logo Printing V2",
        )
        assert result.name == "Logo Printing V2"

    async def test_update_not_found_raises(self, option_repo):
        svc = CustomizationOptionService(option_repo=option_repo)
        with pytest.raises(CustomizationOptionNotFoundError):
            await svc.update_option(
                tenant_id=uuid.uuid7(),
                option_id=uuid.uuid7(),
                name="X",
            )

    async def test_delete_option(self, option_repo):
        existing = CustomizationOption.create(name="Logo", tenant_id=uuid.uuid7())
        option_repo.get_by_id.return_value = existing
        svc = CustomizationOptionService(option_repo=option_repo)
        await svc.delete_option(tenant_id=existing.tenant_id, option_id=existing.id)
        option_repo.delete.assert_called_once()

    async def test_delete_not_found_raises(self, option_repo):
        svc = CustomizationOptionService(option_repo=option_repo)
        with pytest.raises(CustomizationOptionNotFoundError):
            await svc.delete_option(tenant_id=uuid.uuid7(), option_id=uuid.uuid7())

    async def test_get_all(self, option_repo):
        svc = CustomizationOptionService(option_repo=option_repo)
        result = await svc.get_all(tenant_id=uuid.uuid7())
        assert result == []
