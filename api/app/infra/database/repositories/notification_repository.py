from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database.models.follow_up import NotificationModel


class NotificationRepository:
    """Stub — only create method for v0.5.0."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        type: str,
        title: str,
        content: str,
        ref_type: str | None = None,
        ref_id: uuid.UUID | None = None,
    ) -> uuid.UUID:
        now = datetime.now(UTC)
        model = NotificationModel(
            id=uuid.uuid7(),
            tenant_id=tenant_id,
            user_id=user_id,
            type=type,
            title=title,
            content=content,
            ref_type=ref_type,
            ref_id=ref_id,
            is_read=False,
            created_at=now,
            updated_at=now,
        )
        self._session.add(model)
        await self._session.flush()
        return model.id
