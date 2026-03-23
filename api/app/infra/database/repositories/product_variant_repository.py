from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import ProductVariant
from app.domain.product.repository import AbstractProductVariantRepository
from app.infra.database.models.product import ProductVariantModel


class ProductVariantRepository(AbstractProductVariantRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, variant: ProductVariant) -> ProductVariant:
        model = self._to_model(variant)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, variant_id: uuid.UUID) -> ProductVariant | None:
        stmt = select(ProductVariantModel).where(
            ProductVariantModel.id == variant_id,
            ProductVariantModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_product_id(self, tenant_id: uuid.UUID, product_id: uuid.UUID) -> list[ProductVariant]:
        stmt = (
            select(ProductVariantModel)
            .where(
                ProductVariantModel.product_id == product_id,
                ProductVariantModel.tenant_id == tenant_id,
            )
            .order_by(ProductVariantModel.created_at)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def update(self, variant: ProductVariant) -> ProductVariant:
        stmt = select(ProductVariantModel).where(
            ProductVariantModel.id == variant.id,
            ProductVariantModel.tenant_id == variant.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.variant_name = variant.variant_name
        model.sku = variant.sku
        model.material = variant.material
        model.color = variant.color
        model.color_code = variant.color_code
        model.size = variant.size
        model.cost_price = variant.cost_price
        model.cost_currency = variant.cost_currency
        model.is_active = variant.is_active
        model.updated_at = variant.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, variant_id: uuid.UUID) -> None:
        stmt = select(ProductVariantModel).where(
            ProductVariantModel.id == variant_id,
            ProductVariantModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    async def get_by_sku(self, tenant_id: uuid.UUID, sku: str) -> ProductVariant | None:
        stmt = select(ProductVariantModel).where(
            ProductVariantModel.tenant_id == tenant_id,
            ProductVariantModel.sku == sku,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_model(variant: ProductVariant) -> ProductVariantModel:
        return ProductVariantModel(
            id=variant.id,
            tenant_id=variant.tenant_id,
            product_id=variant.product_id,
            variant_name=variant.variant_name,
            sku=variant.sku,
            material=variant.material,
            color=variant.color,
            color_code=variant.color_code,
            size=variant.size,
            cost_price=variant.cost_price,
            cost_currency=variant.cost_currency,
            is_active=variant.is_active,
            created_at=variant.created_at,
            updated_at=variant.updated_at,
        )

    @staticmethod
    def _to_entity(model: ProductVariantModel) -> ProductVariant:
        return ProductVariant(
            id=model.id,
            tenant_id=model.tenant_id,
            product_id=model.product_id,
            variant_name=model.variant_name,
            sku=model.sku,
            material=model.material,
            color=model.color,
            color_code=model.color_code,
            size=model.size,
            cost_price=model.cost_price,
            cost_currency=model.cost_currency,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
