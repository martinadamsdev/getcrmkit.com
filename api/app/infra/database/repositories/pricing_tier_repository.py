from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import PricingTier
from app.domain.product.repository import AbstractPricingTierRepository
from app.infra.database.models.product import PricingTierModel


class PricingTierRepository(AbstractPricingTierRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, tier: PricingTier) -> PricingTier:
        model = self._to_model(tier)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, tier_id: uuid.UUID) -> PricingTier | None:
        stmt = select(PricingTierModel).where(
            PricingTierModel.id == tier_id,
            PricingTierModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID) -> list[PricingTier]:
        stmt = (
            select(PricingTierModel).where(PricingTierModel.tenant_id == tenant_id).order_by(PricingTierModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def update(self, tier: PricingTier) -> PricingTier:
        stmt = select(PricingTierModel).where(
            PricingTierModel.id == tier.id,
            PricingTierModel.tenant_id == tier.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = tier.name
        model.min_qty = tier.min_qty
        model.max_qty = tier.max_qty
        model.multiplier = tier.multiplier
        model.is_default = tier.is_default
        model.position = tier.position
        model.updated_at = tier.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, tier_id: uuid.UUID) -> None:
        stmt = select(PricingTierModel).where(
            PricingTierModel.id == tier_id,
            PricingTierModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_model(tier: PricingTier) -> PricingTierModel:
        return PricingTierModel(
            id=tier.id,
            tenant_id=tier.tenant_id,
            name=tier.name,
            min_qty=tier.min_qty,
            max_qty=tier.max_qty,
            multiplier=tier.multiplier,
            is_default=tier.is_default,
            position=tier.position,
            created_at=tier.created_at,
            updated_at=tier.updated_at,
        )

    @staticmethod
    def _to_entity(model: PricingTierModel) -> PricingTier:
        return PricingTier(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            min_qty=model.min_qty,
            max_qty=model.max_qty,
            multiplier=model.multiplier,
            is_default=model.is_default,
            position=model.position,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
