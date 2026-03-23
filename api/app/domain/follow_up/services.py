from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.domain.follow_up.entities import FollowUp, ScriptTemplate
from app.domain.follow_up.enums import FollowUpMethod, ScriptScene
from app.domain.follow_up.exceptions import (
    FollowUpNotFoundError,
    ScriptTemplateNotFoundError,
    SystemTemplateCannotBeDeletedError,
)
from app.domain.follow_up.repository import AbstractFollowUpRepository, AbstractScriptTemplateRepository


class FollowUpService:
    """纯跟进领域逻辑 — 无跨域依赖。"""

    def __init__(self, follow_up_repo: AbstractFollowUpRepository) -> None:
        self._repo = follow_up_repo

    async def create_follow_up(
        self,
        *,
        customer_id: uuid.UUID,
        content: str,
        method: FollowUpMethod,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        contact_id: uuid.UUID | None = None,
        stage: str | None = None,
        customer_response: str | None = None,
        next_follow_at: datetime | None = None,
        attachment_urls: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> FollowUp:
        """创建跟进记录。调用方（应用层）负责客户存在性检查和 last_follow_at 更新。"""
        follow_up = FollowUp.create(
            customer_id=customer_id,
            content=content,
            method=method,
            tenant_id=tenant_id,
            created_by=created_by,
            contact_id=contact_id,
            stage=stage,
            customer_response=customer_response,
            next_follow_at=next_follow_at,
            attachment_urls=attachment_urls,
            tags=tags,
        )
        return await self._repo.create(follow_up)

    async def get_follow_up(self, tenant_id: uuid.UUID, follow_up_id: uuid.UUID) -> FollowUp:
        follow_up = await self._repo.get_by_id(tenant_id, follow_up_id)
        if follow_up is None:
            raise FollowUpNotFoundError(str(follow_up_id))
        return follow_up

    async def update_follow_up(
        self,
        *,
        tenant_id: uuid.UUID,
        follow_up_id: uuid.UUID,
        **kwargs: object,
    ) -> FollowUp:
        follow_up = await self._repo.get_by_id(tenant_id, follow_up_id)
        if follow_up is None:
            raise FollowUpNotFoundError(str(follow_up_id))
        for key, value in kwargs.items():
            setattr(follow_up, key, value)
        follow_up.updated_at = datetime.now(UTC)
        return await self._repo.update(follow_up)

    async def soft_delete_follow_up(self, *, tenant_id: uuid.UUID, follow_up_id: uuid.UUID) -> None:
        follow_up = await self._repo.get_by_id(tenant_id, follow_up_id)
        if follow_up is None:
            raise FollowUpNotFoundError(str(follow_up_id))
        await self._repo.soft_delete(tenant_id, follow_up_id)

    async def list_by_customer(
        self,
        tenant_id: uuid.UUID,
        customer_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[FollowUp], int]:
        return await self._repo.get_by_customer_id(tenant_id, customer_id, page=page, page_size=page_size)

    async def list_by_tenant(
        self,
        tenant_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 20,
        tags: list[str] | None = None,
        created_by: uuid.UUID | None = None,
    ) -> tuple[list[FollowUp], int]:
        return await self._repo.get_by_tenant(
            tenant_id, page=page, page_size=page_size, tags=tags, created_by=created_by
        )


class ScriptTemplateService:
    def __init__(self, template_repo: AbstractScriptTemplateRepository) -> None:
        self._repo = template_repo

    async def create_template(
        self,
        *,
        scene: ScriptScene,
        title: str,
        content: str,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID | None = None,
        language: str = "zh-CN",
        position: int = 0,
        is_system: bool = False,
    ) -> ScriptTemplate:
        template = ScriptTemplate.create(
            scene=scene,
            title=title,
            content=content,
            tenant_id=tenant_id,
            created_by=created_by,
            language=language,
            position=position,
            is_system=is_system,
        )
        return await self._repo.create(template)

    async def update_template(
        self,
        *,
        tenant_id: uuid.UUID,
        template_id: uuid.UUID,
        **kwargs: object,
    ) -> ScriptTemplate:
        template = await self._repo.get_by_id(tenant_id, template_id)
        if template is None:
            raise ScriptTemplateNotFoundError(str(template_id))
        for key, value in kwargs.items():
            setattr(template, key, value)
        template.updated_at = datetime.now(UTC)
        return await self._repo.update(template)

    async def delete_template(self, *, tenant_id: uuid.UUID, template_id: uuid.UUID) -> None:
        template = await self._repo.get_by_id(tenant_id, template_id)
        if template is None:
            raise ScriptTemplateNotFoundError(str(template_id))
        if template.is_system:
            raise SystemTemplateCannotBeDeletedError(str(template_id))
        await self._repo.delete(tenant_id, template_id)

    async def get_all(self, tenant_id: uuid.UUID, *, scene: str | None = None) -> list[ScriptTemplate]:
        return await self._repo.get_all(tenant_id, scene=scene)
