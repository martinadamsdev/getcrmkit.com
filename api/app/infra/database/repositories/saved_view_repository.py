from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import SavedView
from app.domain.customer.repository import AbstractSavedViewRepository
from app.infra.database.models.saved_view import SavedViewModel


class SavedViewRepository(AbstractSavedViewRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, view: SavedView) -> SavedView:
        model = self._to_model(view)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, user_id: uuid.UUID, view_id: uuid.UUID) -> SavedView | None:
        stmt = select(SavedViewModel).where(
            SavedViewModel.id == view_id,
            SavedViewModel.tenant_id == tenant_id,
            SavedViewModel.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID, user_id: uuid.UUID, entity_type: str) -> list[SavedView]:
        stmt = (
            select(SavedViewModel)
            .where(
                SavedViewModel.tenant_id == tenant_id,
                SavedViewModel.user_id == user_id,
                SavedViewModel.entity_type == entity_type,
            )
            .order_by(SavedViewModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def get_by_name(
        self,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        entity_type: str,
        name: str,
    ) -> SavedView | None:
        stmt = select(SavedViewModel).where(
            SavedViewModel.tenant_id == tenant_id,
            SavedViewModel.user_id == user_id,
            SavedViewModel.entity_type == entity_type,
            SavedViewModel.name == name,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, view: SavedView) -> SavedView:
        stmt = select(SavedViewModel).where(
            SavedViewModel.id == view.id,
            SavedViewModel.tenant_id == view.tenant_id,
            SavedViewModel.user_id == view.user_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = view.name
        model.filter_config = view.filter_config
        model.is_default = view.is_default
        model.position = view.position
        model.updated_by = view.updated_by
        model.updated_at = view.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, user_id: uuid.UUID, view_id: uuid.UUID) -> None:
        stmt = select(SavedViewModel).where(
            SavedViewModel.id == view_id,
            SavedViewModel.tenant_id == tenant_id,
            SavedViewModel.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_model(view: SavedView) -> SavedViewModel:
        return SavedViewModel(
            id=view.id,
            tenant_id=view.tenant_id,
            user_id=view.user_id,
            entity_type=view.entity_type,
            name=view.name,
            filter_config=view.filter_config,
            is_default=view.is_default,
            position=view.position,
            created_by=view.created_by,
            updated_by=view.updated_by,
            created_at=view.created_at,
            updated_at=view.updated_at,
        )

    @staticmethod
    def _to_entity(model: SavedViewModel) -> SavedView:
        return SavedView(
            id=model.id,
            tenant_id=model.tenant_id,
            user_id=model.user_id,
            entity_type=model.entity_type,
            name=model.name,
            filter_config=model.filter_config,
            is_default=model.is_default,
            position=model.position,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
