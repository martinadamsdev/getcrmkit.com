from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from app.domain.product.entities import (
    CustomizationOption,
    PricingTier,
    Product,
    ProductCategory,
    ProductVariant,
)
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
from app.domain.product.repository import (
    AbstractCustomizationOptionRepository,
    AbstractPricingTierRepository,
    AbstractProductCategoryRepository,
    AbstractProductRepository,
    AbstractProductVariantRepository,
)
from app.domain.product.value_objects import ProductFilter


class PricingService:
    """Tiered pricing logic — finds the matching multiplier for a given quantity."""

    def __init__(self, pricing_tier_repo: AbstractPricingTierRepository) -> None:
        self._repo = pricing_tier_repo

    async def get_multiplier(self, tenant_id: uuid.UUID, qty: int) -> Decimal:
        """
        Return the multiplier for the given quantity.
        Match rule: min_qty <= qty <= max_qty (max_qty=None means no upper limit).
        No match -> return Decimal("1.0000") (original price, no markup).
        """
        tiers = await self._repo.get_all(tenant_id)
        for tier in sorted(tiers, key=lambda t: t.min_qty):
            if qty >= tier.min_qty and (tier.max_qty is None or qty <= tier.max_qty):
                return tier.multiplier
        return Decimal("1.0000")


class ProductService:
    def __init__(self, product_repo: AbstractProductRepository) -> None:
        self._repo = product_repo

    async def create_product(
        self,
        *,
        name: str,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        **kwargs: Any,
    ) -> Product:
        product = Product.create(name=name, tenant_id=tenant_id, created_by=created_by, **kwargs)
        return await self._repo.create(product)

    async def get_product(self, *, tenant_id: uuid.UUID, product_id: uuid.UUID) -> Product:
        product = await self._repo.get_by_id(tenant_id, product_id)
        if product is None:
            raise ProductNotFoundError(str(product_id))
        return product

    async def update_product(
        self,
        *,
        tenant_id: uuid.UUID,
        product_id: uuid.UUID,
        **kwargs: Any,
    ) -> Product:
        product = await self._repo.get_by_id(tenant_id, product_id)
        if product is None:
            raise ProductNotFoundError(str(product_id))
        for key, value in kwargs.items():
            setattr(product, key, value)
        product.updated_at = datetime.now(UTC)
        return await self._repo.update(product)

    async def soft_delete_product(self, *, tenant_id: uuid.UUID, product_id: uuid.UUID) -> None:
        product = await self._repo.get_by_id(tenant_id, product_id)
        if product is None:
            raise ProductNotFoundError(str(product_id))
        await self._repo.soft_delete(tenant_id, product_id)

    async def list_products(
        self,
        tenant_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        filters: ProductFilter | None = None,
    ) -> tuple[list[Product], int]:
        return await self._repo.get_by_tenant(tenant_id, page, page_size, filters=filters)


class ProductVariantService:
    def __init__(
        self,
        variant_repo: AbstractProductVariantRepository,
        product_repo: AbstractProductRepository,
    ) -> None:
        self._variant_repo = variant_repo
        self._product_repo = product_repo

    async def create_variant(
        self,
        *,
        product_id: uuid.UUID,
        variant_name: str,
        tenant_id: uuid.UUID,
        **kwargs: Any,
    ) -> ProductVariant:
        product = await self._product_repo.get_by_id(tenant_id, product_id)
        if product is None:
            raise ProductNotFoundError(str(product_id))
        # ProductVariant does not inherit BaseEntity — strip audit fields
        kwargs.pop("created_by", None)
        variant = ProductVariant.create(
            product_id=product_id,
            variant_name=variant_name,
            tenant_id=tenant_id,
            **kwargs,
        )
        return await self._variant_repo.create(variant)

    async def get_variant(self, *, tenant_id: uuid.UUID, variant_id: uuid.UUID) -> ProductVariant:
        variant = await self._variant_repo.get_by_id(tenant_id, variant_id)
        if variant is None:
            raise VariantNotFoundError(str(variant_id))
        return variant

    async def list_by_product(self, *, tenant_id: uuid.UUID, product_id: uuid.UUID) -> list[ProductVariant]:
        return await self._variant_repo.get_by_product_id(tenant_id, product_id)

    async def update_variant(
        self,
        *,
        tenant_id: uuid.UUID,
        variant_id: uuid.UUID,
        **kwargs: Any,
    ) -> ProductVariant:
        variant = await self._variant_repo.get_by_id(tenant_id, variant_id)
        if variant is None:
            raise VariantNotFoundError(str(variant_id))
        for key, value in kwargs.items():
            setattr(variant, key, value)
        variant.updated_at = datetime.now(UTC)
        return await self._variant_repo.update(variant)

    async def delete_variant(self, *, tenant_id: uuid.UUID, variant_id: uuid.UUID) -> None:
        variant = await self._variant_repo.get_by_id(tenant_id, variant_id)
        if variant is None:
            raise VariantNotFoundError(str(variant_id))
        await self._variant_repo.delete(tenant_id, variant_id)


class ProductCategoryService:
    def __init__(self, category_repo: AbstractProductCategoryRepository) -> None:
        self._repo = category_repo

    async def create_category(
        self,
        *,
        name: str,
        tenant_id: uuid.UUID,
        parent_id: uuid.UUID | None = None,
        position: int = 0,
    ) -> ProductCategory:
        level = 1
        if parent_id is not None:
            parent = await self._repo.get_by_id(tenant_id, parent_id)
            if parent is None:
                raise CategoryNotFoundError(str(parent_id))
            if parent.level >= MAX_CATEGORY_DEPTH:
                raise MaxCategoryDepthError()
            level = parent.level + 1

        cat = ProductCategory(
            name=name,
            parent_id=parent_id,
            level=level,
            position=position,
            tenant_id=tenant_id,
        )
        cat.validate_depth()
        return await self._repo.create(cat)

    async def update_category(
        self,
        *,
        tenant_id: uuid.UUID,
        category_id: uuid.UUID,
        **kwargs: Any,
    ) -> ProductCategory:
        cat = await self._repo.get_by_id(tenant_id, category_id)
        if cat is None:
            raise CategoryNotFoundError(str(category_id))
        for key, value in kwargs.items():
            setattr(cat, key, value)
        return await self._repo.update(cat)

    async def delete_category(self, *, tenant_id: uuid.UUID, category_id: uuid.UUID) -> None:
        """Hard delete. Rejects if has children or has products."""
        cat = await self._repo.get_by_id(tenant_id, category_id)
        if cat is None:
            raise CategoryNotFoundError(str(category_id))
        if await self._repo.has_children(tenant_id, category_id):
            raise CategoryHasChildrenError(str(category_id))
        if await self._repo.has_products(tenant_id, category_id):
            raise CategoryInUseError(str(category_id))
        await self._repo.delete(tenant_id, category_id)

    async def get_all(self, tenant_id: uuid.UUID) -> list[ProductCategory]:
        return await self._repo.get_all(tenant_id)


class PricingTierService:
    def __init__(self, pricing_tier_repo: AbstractPricingTierRepository) -> None:
        self._repo = pricing_tier_repo

    async def create_tier(
        self,
        *,
        tenant_id: uuid.UUID,
        min_qty: int,
        multiplier: Decimal,
        name: str | None = None,
        max_qty: int | None = None,
        is_default: bool = False,
        position: int = 0,
    ) -> PricingTier:
        tier = PricingTier(
            name=name,
            min_qty=min_qty,
            max_qty=max_qty,
            multiplier=multiplier,
            is_default=is_default,
            position=position,
            tenant_id=tenant_id,
        )
        return await self._repo.create(tier)

    async def update_tier(
        self,
        *,
        tenant_id: uuid.UUID,
        tier_id: uuid.UUID,
        **kwargs: Any,
    ) -> PricingTier:
        tier = await self._repo.get_by_id(tenant_id, tier_id)
        if tier is None:
            raise PricingTierNotFoundError(str(tier_id))
        for key, value in kwargs.items():
            setattr(tier, key, value)
        tier.updated_at = datetime.now(UTC)
        return await self._repo.update(tier)

    async def delete_tier(self, *, tenant_id: uuid.UUID, tier_id: uuid.UUID) -> None:
        tier = await self._repo.get_by_id(tenant_id, tier_id)
        if tier is None:
            raise PricingTierNotFoundError(str(tier_id))
        await self._repo.delete(tenant_id, tier_id)

    async def get_all(self, tenant_id: uuid.UUID) -> list[PricingTier]:
        return await self._repo.get_all(tenant_id)


class CustomizationOptionService:
    def __init__(self, option_repo: AbstractCustomizationOptionRepository) -> None:
        self._repo = option_repo

    async def create_option(
        self,
        *,
        name: str,
        tenant_id: uuid.UUID,
        description: str | None = None,
        extra_cost: Decimal = Decimal("0"),
        extra_currency: str = "CNY",
        is_active: bool = True,
    ) -> CustomizationOption:
        option = CustomizationOption.create(
            name=name,
            tenant_id=tenant_id,
            description=description,
            extra_cost=extra_cost,
            extra_currency=extra_currency,
            is_active=is_active,
        )
        return await self._repo.create(option)

    async def update_option(
        self,
        *,
        tenant_id: uuid.UUID,
        option_id: uuid.UUID,
        **kwargs: Any,
    ) -> CustomizationOption:
        option = await self._repo.get_by_id(tenant_id, option_id)
        if option is None:
            raise CustomizationOptionNotFoundError(str(option_id))
        for key, value in kwargs.items():
            setattr(option, key, value)
        option.updated_at = datetime.now(UTC)
        return await self._repo.update(option)

    async def delete_option(self, *, tenant_id: uuid.UUID, option_id: uuid.UUID) -> None:
        option = await self._repo.get_by_id(tenant_id, option_id)
        if option is None:
            raise CustomizationOptionNotFoundError(str(option_id))
        await self._repo.delete(tenant_id, option_id)

    async def get_all(self, tenant_id: uuid.UUID) -> list[CustomizationOption]:
        return await self._repo.get_all(tenant_id)


MAX_CATEGORY_DEPTH = 3
