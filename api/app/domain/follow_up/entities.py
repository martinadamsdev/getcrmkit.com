from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.follow_up.enums import FollowUpMethod, ScriptScene
from app.domain.follow_up.events import FollowUpCreated
from app.domain.follow_up.exceptions import FollowUpContentRequiredError
from app.domain.shared.entity import BaseEntity


@dataclass
class FollowUp(BaseEntity):
    customer_id: uuid.UUID = field(default_factory=uuid.uuid7)
    contact_id: uuid.UUID | None = None
    method: FollowUpMethod = FollowUpMethod.EMAIL
    stage: str | None = None
    content: str = ""
    customer_response: str | None = None
    next_follow_at: datetime | None = None
    attachment_urls: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def create(
        cls,
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
        if not content or not content.strip():
            raise FollowUpContentRequiredError()

        follow_up = cls(
            customer_id=customer_id,
            contact_id=contact_id,
            method=method,
            stage=stage,
            content=content.strip(),
            customer_response=customer_response,
            next_follow_at=next_follow_at,
            attachment_urls=attachment_urls or [],
            tags=tags or [],
            tenant_id=tenant_id,
            created_by=created_by,
        )

        follow_up.add_event(
            FollowUpCreated(
                follow_up_id=follow_up.id,
                customer_id=customer_id,
                tenant_id=tenant_id,
                created_by=created_by,
            )
        )

        return follow_up

    @property
    def is_reminder_due(self) -> bool:
        """纯业务规则：下次跟进时间已到期且记录未被软删除。"""
        if self.next_follow_at is None or self.is_deleted:
            return False
        return datetime.now(UTC) >= self.next_follow_at


@dataclass
class ScriptTemplate:
    """话术模板 — 无软删除，系统模板受 is_system 保护。"""

    id: uuid.UUID = field(default_factory=uuid.uuid7)
    scene: ScriptScene = ScriptScene.FIRST_CONTACT
    title: str = ""
    content: str = ""
    language: str = "zh-CN"
    position: int = 0
    is_system: bool = False
    tenant_id: uuid.UUID = field(default_factory=uuid.uuid7)
    created_by: uuid.UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
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
        from app.domain.follow_up.exceptions import ScriptTemplateTitleRequiredError

        if not title or not title.strip():
            raise ScriptTemplateTitleRequiredError()

        return cls(
            scene=scene,
            title=title.strip(),
            content=content,
            language=language,
            position=position,
            is_system=is_system,
            tenant_id=tenant_id,
            created_by=created_by,
        )
