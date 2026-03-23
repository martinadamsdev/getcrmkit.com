from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.product.entities import (
    CustomizationOption,
    PricingTier,
    Product,
    ProductCategory,
    ProductVariant,
)
from app.domain.product.value_objects import ProductFilter


class AbstractProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, product_id: uuid.UUID) -> Product | None: ...

    @abstractmethod
    async def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        filters: ProductFilter | None = None,
    ) -> tuple[list[Product], int]: ...

    @abstractmethod
    async def update(self, product: Product) -> Product: ...

    @abstractmethod
    async def soft_delete(self, tenant_id: uuid.UUID, product_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_sku(self, tenant_id: uuid.UUID, sku: str) -> Product | None: ...

    @abstractmethod
    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int: ...

    @abstractmethod
    async def get_by_category(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> list[Product]: ...


class AbstractProductVariantRepository(ABC):
    @abstractmethod
    async def create(self, variant: ProductVariant) -> ProductVariant: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, variant_id: uuid.UUID) -> ProductVariant | None: ...

    @abstractmethod
    async def get_by_product_id(self, tenant_id: uuid.UUID, product_id: uuid.UUID) -> list[ProductVariant]: ...

    @abstractmethod
    async def update(self, variant: ProductVariant) -> ProductVariant: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, variant_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_sku(self, tenant_id: uuid.UUID, sku: str) -> ProductVariant | None: ...


class AbstractProductCategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: ProductCategory) -> ProductCategory: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> ProductCategory | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID) -> list[ProductCategory]: ...

    @abstractmethod
    async def get_children(self, tenant_id: uuid.UUID, parent_id: uuid.UUID) -> list[ProductCategory]: ...

    @abstractmethod
    async def get_tree(self, tenant_id: uuid.UUID) -> list[ProductCategory]: ...

    @abstractmethod
    async def update(self, category: ProductCategory) -> ProductCategory: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def has_products(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> bool: ...

    @abstractmethod
    async def has_children(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> bool: ...


class AbstractPricingTierRepository(ABC):
    @abstractmethod
    async def create(self, tier: PricingTier) -> PricingTier: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, tier_id: uuid.UUID) -> PricingTier | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID) -> list[PricingTier]: ...

    @abstractmethod
    async def update(self, tier: PricingTier) -> PricingTier: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, tier_id: uuid.UUID) -> None: ...


class AbstractCustomizationOptionRepository(ABC):
    @abstractmethod
    async def create(self, option: CustomizationOption) -> CustomizationOption: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, option_id: uuid.UUID) -> CustomizationOption | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID) -> list[CustomizationOption]: ...

    @abstractmethod
    async def update(self, option: CustomizationOption) -> CustomizationOption: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, option_id: uuid.UUID) -> None: ...
