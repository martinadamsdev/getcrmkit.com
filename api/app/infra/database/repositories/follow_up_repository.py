from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.follow_up.entities import FollowUp, ScriptTemplate
from app.domain.follow_up.enums import FollowUpMethod, ScriptScene
from app.domain.follow_up.repository import AbstractFollowUpRepository, AbstractScriptTemplateRepository
from app.infra.database.models.follow_up import FollowUpModel, ScriptTemplateModel


class FollowUpRepository(AbstractFollowUpRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, follow_up: FollowUp) -> FollowUp:
        model = self._to_model(follow_up)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, follow_up_id: uuid.UUID) -> FollowUp | None:
        stmt = select(FollowUpModel).where(
            FollowUpModel.id == follow_up_id,
            FollowUpModel.tenant_id == tenant_id,
            FollowUpModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_customer_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[FollowUp], int]:
        conditions = [
            FollowUpModel.tenant_id == tenant_id,
            FollowUpModel.customer_id == customer_id,
            FollowUpModel.deleted_at.is_(None),
        ]

        count_stmt = select(func.count()).select_from(FollowUpModel).where(*conditions)
        total = (await self._session.execute(count_stmt)).scalar_one()

        stmt = (
            select(FollowUpModel)
            .where(*conditions)
            .order_by(FollowUpModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        items = [self._to_entity(m) for m in result.scalars()]
        return items, total

    async def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 20,
        tags: list[str] | None = None,
        created_by: uuid.UUID | None = None,
    ) -> tuple[list[FollowUp], int]:
        conditions = [
            FollowUpModel.tenant_id == tenant_id,
            FollowUpModel.deleted_at.is_(None),
        ]

        if tags:
            # PostgreSQL array overlap operator: tags && ARRAY[:tags]
            from sqlalchemy import Text, cast
            from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY

            conditions.append(
                FollowUpModel.tags.op("&&")(cast(tags, PG_ARRAY(Text)))
            )

        if created_by is not None:
            conditions.append(FollowUpModel.created_by == created_by)

        count_stmt = select(func.count()).select_from(FollowUpModel).where(*conditions)
        total = (await self._session.execute(count_stmt)).scalar_one()

        stmt = (
            select(FollowUpModel)
            .where(*conditions)
            .order_by(FollowUpModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        items = [self._to_entity(m) for m in result.scalars()]
        return items, total

    async def update(self, follow_up: FollowUp) -> FollowUp:
        stmt = select(FollowUpModel).where(
            FollowUpModel.id == follow_up.id,
            FollowUpModel.tenant_id == follow_up.tenant_id,
            FollowUpModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.method = follow_up.method.value
        model.stage = follow_up.stage
        model.content = follow_up.content
        model.customer_response = follow_up.customer_response
        model.next_follow_at = follow_up.next_follow_at
        model.attachment_urls = follow_up.attachment_urls
        model.tags = follow_up.tags
        model.contact_id = follow_up.contact_id
        model.updated_by = follow_up.updated_by
        model.updated_at = follow_up.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def soft_delete(self, tenant_id: uuid.UUID, follow_up_id: uuid.UUID) -> None:
        stmt = select(FollowUpModel).where(
            FollowUpModel.id == follow_up_id,
            FollowUpModel.tenant_id == tenant_id,
            FollowUpModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.deleted_at = datetime.now(UTC)
        await self._session.flush()

    async def find_due_reminders(
        self,
        before: datetime,
        limit: int = 100,
    ) -> list[FollowUp]:
        stmt = (
            select(FollowUpModel)
            .where(
                FollowUpModel.next_follow_at <= before,
                FollowUpModel.next_follow_at.isnot(None),
                FollowUpModel.deleted_at.is_(None),
            )
            .order_by(FollowUpModel.next_follow_at.asc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    @staticmethod
    def _to_model(follow_up: FollowUp) -> FollowUpModel:
        return FollowUpModel(
            id=follow_up.id,
            tenant_id=follow_up.tenant_id,
            customer_id=follow_up.customer_id,
            contact_id=follow_up.contact_id,
            method=follow_up.method.value,
            stage=follow_up.stage,
            content=follow_up.content,
            customer_response=follow_up.customer_response,
            next_follow_at=follow_up.next_follow_at,
            attachment_urls=follow_up.attachment_urls,
            tags=follow_up.tags,
            created_by=follow_up.created_by,
            updated_by=follow_up.updated_by,
            created_at=follow_up.created_at,
            updated_at=follow_up.updated_at,
            deleted_at=follow_up.deleted_at,
        )

    @staticmethod
    def _to_entity(model: FollowUpModel) -> FollowUp:
        return FollowUp(
            id=model.id,
            tenant_id=model.tenant_id,
            customer_id=model.customer_id,
            contact_id=model.contact_id,
            method=FollowUpMethod(model.method),
            stage=model.stage,
            content=model.content,
            customer_response=model.customer_response,
            next_follow_at=model.next_follow_at,
            attachment_urls=model.attachment_urls or [],
            tags=model.tags or [],
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )


class ScriptTemplateRepository(AbstractScriptTemplateRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, template: ScriptTemplate) -> ScriptTemplate:
        model = self._to_model(template)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, template_id: uuid.UUID) -> ScriptTemplate | None:
        stmt = select(ScriptTemplateModel).where(
            ScriptTemplateModel.id == template_id,
            ScriptTemplateModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID, *, scene: str | None = None) -> list[ScriptTemplate]:
        conditions = [ScriptTemplateModel.tenant_id == tenant_id]
        if scene is not None:
            conditions.append(ScriptTemplateModel.scene == scene)
        stmt = (
            select(ScriptTemplateModel)
            .where(*conditions)
            .order_by(ScriptTemplateModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def update(self, template: ScriptTemplate) -> ScriptTemplate:
        stmt = select(ScriptTemplateModel).where(
            ScriptTemplateModel.id == template.id,
            ScriptTemplateModel.tenant_id == template.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.scene = template.scene.value
        model.title = template.title
        model.content = template.content
        model.language = template.language
        model.position = template.position
        model.is_system = template.is_system
        model.updated_at = template.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, template_id: uuid.UUID) -> None:
        stmt = select(ScriptTemplateModel).where(
            ScriptTemplateModel.id == template_id,
            ScriptTemplateModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ScriptTemplateModel)
            .where(ScriptTemplateModel.tenant_id == tenant_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    def _to_model(template: ScriptTemplate) -> ScriptTemplateModel:
        return ScriptTemplateModel(
            id=template.id,
            tenant_id=template.tenant_id,
            scene=template.scene.value,
            title=template.title,
            content=template.content,
            language=template.language,
            position=template.position,
            is_system=template.is_system,
            created_by=template.created_by,
            created_at=template.created_at,
            updated_at=template.updated_at,
        )

    @staticmethod
    def _to_entity(model: ScriptTemplateModel) -> ScriptTemplate:
        return ScriptTemplate(
            id=model.id,
            tenant_id=model.tenant_id,
            scene=ScriptScene(model.scene),
            title=model.title,
            content=model.content,
            language=model.language,
            position=model.position,
            is_system=model.is_system,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
