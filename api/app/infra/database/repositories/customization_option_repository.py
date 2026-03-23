from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import CustomizationOption
from app.domain.product.repository import AbstractCustomizationOptionRepository
from app.infra.database.models.product import CustomizationOptionModel


class CustomizationOptionRepository(AbstractCustomizationOptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, option: CustomizationOption) -> CustomizationOption:
        model = self._to_model(option)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, option_id: uuid.UUID) -> CustomizationOption | None:
        stmt = select(CustomizationOptionModel).where(
            CustomizationOptionModel.id == option_id,
            CustomizationOptionModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID) -> list[CustomizationOption]:
        stmt = (
            select(CustomizationOptionModel)
            .where(CustomizationOptionModel.tenant_id == tenant_id)
            .order_by(CustomizationOptionModel.created_at)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def update(self, option: CustomizationOption) -> CustomizationOption:
        stmt = select(CustomizationOptionModel).where(
            CustomizationOptionModel.id == option.id,
            CustomizationOptionModel.tenant_id == option.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = option.name
        model.description = option.description
        model.extra_cost = option.extra_cost
        model.extra_currency = option.extra_currency
        model.is_active = option.is_active
        model.updated_at = option.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, option_id: uuid.UUID) -> None:
        stmt = select(CustomizationOptionModel).where(
            CustomizationOptionModel.id == option_id,
            CustomizationOptionModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_model(option: CustomizationOption) -> CustomizationOptionModel:
        return CustomizationOptionModel(
            id=option.id,
            tenant_id=option.tenant_id,
            name=option.name,
            description=option.description,
            extra_cost=option.extra_cost,
            extra_currency=option.extra_currency,
            is_active=option.is_active,
            created_at=option.created_at,
            updated_at=option.updated_at,
        )

    @staticmethod
    def _to_entity(model: CustomizationOptionModel) -> CustomizationOption:
        return CustomizationOption(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            description=model.description,
            extra_cost=model.extra_cost,
            extra_currency=model.extra_currency,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
