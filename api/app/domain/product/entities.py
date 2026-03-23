from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from app.domain.product.events import ProductCreated
from app.domain.product.exceptions import (
    CustomizationOptionNameRequiredError,
    MaxCategoryDepthError,
    ProductNameRequiredError,
    VariantNameRequiredError,
)
from app.domain.shared.entity import BaseEntity

MAX_CATEGORY_DEPTH = 3


@dataclass
class Product(BaseEntity):
    name: str = ""
    sku: str | None = None
    category_id: uuid.UUID | None = None
    description: str | None = None
    image_url: str | None = None
    material: str | None = None
    dimensions: str | None = None
    weight: Decimal | None = None
    color: str | None = None
    packing: str | None = None
    cost_price: Decimal | None = None
    cost_currency: str = "CNY"
    selling_price: Decimal | None = None
    selling_currency: str = "USD"
    is_active: bool = True
    custom_fields: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        **kwargs: Any,
    ) -> Product:
        if not name or not name.strip():
            raise ProductNameRequiredError()
        product = cls(
            name=name.strip(),
            tenant_id=tenant_id,
            created_by=created_by,
            **kwargs,
        )
        product.add_event(
            ProductCreated(
                product_id=product.id,
                tenant_id=tenant_id,
                created_by=created_by,
            )
        )
        return product


@dataclass
class ProductCategory:
    """Product category — config entity, hard delete, no BaseEntity."""

    id: uuid.UUID = field(default_factory=uuid.uuid7)
    tenant_id: uuid.UUID = field(default_factory=uuid.uuid7)
    name: str = ""
    parent_id: uuid.UUID | None = None
    level: int = 1
    position: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def validate_depth(self) -> None:
        if self.level > MAX_CATEGORY_DEPTH:
            raise MaxCategoryDepthError()


@dataclass
class ProductVariant:
    """Product variant — no soft delete, CASCADE with parent Product."""

    id: uuid.UUID = field(default_factory=uuid.uuid7)
    tenant_id: uuid.UUID = field(default_factory=uuid.uuid7)
    product_id: uuid.UUID = field(default_factory=uuid.uuid7)
    variant_name: str = ""
    sku: str | None = None
    material: str | None = None
    color: str | None = None
    color_code: str | None = None
    size: str | None = None
    cost_price: Decimal | None = None
    cost_currency: str = "CNY"
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        product_id: uuid.UUID,
        variant_name: str,
        tenant_id: uuid.UUID,
        **kwargs: Any,
    ) -> ProductVariant:
        if not variant_name or not variant_name.strip():
            raise VariantNameRequiredError()
        return cls(
            product_id=product_id,
            variant_name=variant_name.strip(),
            tenant_id=tenant_id,
            **kwargs,
        )


@dataclass
class PricingTier:
    """Global tiered pricing rule — hard delete, config entity."""

    id: uuid.UUID = field(default_factory=uuid.uuid7)
    tenant_id: uuid.UUID = field(default_factory=uuid.uuid7)
    name: str | None = None
    min_qty: int = 0
    max_qty: int | None = None
    multiplier: Decimal = field(default_factory=lambda: Decimal("1.0000"))
    is_default: bool = False
    position: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class CustomizationOption:
    """Customization option — hard delete, config entity."""

    id: uuid.UUID = field(default_factory=uuid.uuid7)
    tenant_id: uuid.UUID = field(default_factory=uuid.uuid7)
    name: str = ""
    description: str | None = None
    extra_cost: Decimal = field(default_factory=lambda: Decimal("0"))
    extra_currency: str = "CNY"
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        name: str,
        tenant_id: uuid.UUID,
        description: str | None = None,
        extra_cost: Decimal = Decimal("0"),
        extra_currency: str = "CNY",
        is_active: bool = True,
    ) -> CustomizationOption:
        if not name or not name.strip():
            raise CustomizationOptionNameRequiredError()
        return cls(
            name=name.strip(),
            tenant_id=tenant_id,
            description=description,
            extra_cost=extra_cost,
            extra_currency=extra_currency,
            is_active=is_active,
        )
