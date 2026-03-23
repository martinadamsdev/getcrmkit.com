from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.follow_up.entities import FollowUp, ScriptTemplate


class AbstractFollowUpRepository(ABC):
    @abstractmethod
    async def create(self, follow_up: FollowUp) -> FollowUp: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, follow_up_id: uuid.UUID) -> FollowUp | None: ...

    @abstractmethod
    async def get_by_customer_id(
        self,
        tenant_id: uuid.UUID,
        customer_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[FollowUp], int]: ...

    @abstractmethod
    async def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 20,
        tags: list[str] | None = None,
        created_by: uuid.UUID | None = None,
    ) -> tuple[list[FollowUp], int]: ...

    @abstractmethod
    async def update(self, follow_up: FollowUp) -> FollowUp: ...

    @abstractmethod
    async def soft_delete(self, tenant_id: uuid.UUID, follow_up_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def find_due_reminders(
        self,
        before: datetime,
        limit: int = 100,
    ) -> list[FollowUp]: ...


class AbstractScriptTemplateRepository(ABC):
    @abstractmethod
    async def create(self, template: ScriptTemplate) -> ScriptTemplate: ...

    @abstractmethod
    async def get_by_id(self, tenant_id: uuid.UUID, template_id: uuid.UUID) -> ScriptTemplate | None: ...

    @abstractmethod
    async def get_all(self, tenant_id: uuid.UUID, *, scene: str | None = None) -> list[ScriptTemplate]: ...

    @abstractmethod
    async def update(self, template: ScriptTemplate) -> ScriptTemplate: ...

    @abstractmethod
    async def delete(self, tenant_id: uuid.UUID, template_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int: ...
