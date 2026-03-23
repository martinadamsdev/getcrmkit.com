import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

# --- Product ---


class CreateProductRequest(BaseModel):
    name: str
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
    custom_fields: dict[str, object] = Field(default_factory=dict)


class UpdateProductRequest(BaseModel):
    name: str | None = None
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
    cost_currency: str | None = None
    selling_price: Decimal | None = None
    selling_currency: str | None = None
    is_active: bool | None = None
    custom_fields: dict[str, object] | None = None


class ProductResponse(BaseModel):
    id: uuid.UUID
    name: str
    sku: str | None
    category_id: uuid.UUID | None
    description: str | None
    image_url: str | None
    material: str | None
    dimensions: str | None
    weight: Decimal | None
    color: str | None
    packing: str | None
    cost_price: Decimal | None
    cost_currency: str
    selling_price: Decimal | None
    selling_currency: str
    is_active: bool
    custom_fields: dict[str, object]
    created_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


# --- ProductVariant ---


class CreateVariantRequest(BaseModel):
    variant_name: str
    sku: str | None = None
    material: str | None = None
    color: str | None = None
    color_code: str | None = None
    size: str | None = None
    cost_price: Decimal | None = None
    cost_currency: str = "CNY"
    is_active: bool = True


class UpdateVariantRequest(BaseModel):
    variant_name: str | None = None
    sku: str | None = None
    material: str | None = None
    color: str | None = None
    color_code: str | None = None
    size: str | None = None
    cost_price: Decimal | None = None
    cost_currency: str | None = None
    is_active: bool | None = None


class VariantResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    variant_name: str
    sku: str | None
    material: str | None
    color: str | None
    color_code: str | None
    size: str | None
    cost_price: Decimal | None
    cost_currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- ProductCategory ---


class CreateCategoryRequest(BaseModel):
    name: str
    parent_id: uuid.UUID | None = None
    position: int = 0


class UpdateCategoryRequest(BaseModel):
    name: str | None = None
    position: int | None = None


class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    parent_id: uuid.UUID | None
    level: int
    position: int
    created_at: datetime


# --- PricingTier ---


class CreatePricingTierRequest(BaseModel):
    name: str | None = None
    min_qty: int
    max_qty: int | None = None
    multiplier: Decimal
    is_default: bool = False
    position: int = 0


class UpdatePricingTierRequest(BaseModel):
    name: str | None = None
    min_qty: int | None = None
    max_qty: int | None = None
    multiplier: Decimal | None = None
    is_default: bool | None = None
    position: int | None = None


class PricingTierResponse(BaseModel):
    id: uuid.UUID
    name: str | None
    min_qty: int
    max_qty: int | None
    multiplier: Decimal
    is_default: bool
    position: int
    created_at: datetime
    updated_at: datetime


class GetMultiplierResponse(BaseModel):
    qty: int
    multiplier: Decimal


# --- CustomizationOption ---


class CreateCustomizationOptionRequest(BaseModel):
    name: str
    description: str | None = None
    extra_cost: Decimal = Decimal("0")
    extra_currency: str = "CNY"
    is_active: bool = True


class UpdateCustomizationOptionRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    extra_cost: Decimal | None = None
    extra_currency: str | None = None
    is_active: bool | None = None


class CustomizationOptionResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    extra_cost: Decimal
    extra_currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- Import/Export ---


class ExportProductRequest(BaseModel):
    keyword: str | None = None
    category_id: uuid.UUID | None = None
    is_active: bool | None = None
