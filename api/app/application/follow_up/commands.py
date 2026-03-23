from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.domain.customer.exceptions import CustomerNotFoundError
from app.domain.customer.repository import AbstractCustomerRepository
from app.domain.follow_up.entities import FollowUp
from app.domain.follow_up.enums import FollowUpMethod
from app.domain.follow_up.repository import AbstractFollowUpRepository
from app.domain.follow_up.services import FollowUpService
from app.infra.database.repositories.notification_repository import NotificationRepository


class CreateFollowUpHandler:
    """跨域编排：检查客户存在 -> 创建跟进 -> 更新 last_follow_at。"""

    def __init__(
        self,
        follow_up_service: FollowUpService,
        customer_repo: AbstractCustomerRepository,
    ) -> None:
        self._follow_up_service = follow_up_service
        self._customer_repo = customer_repo

    async def handle(
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
        # 1. 检查客户是否存在（跨域）
        customer = await self._customer_repo.get_by_id(tenant_id, customer_id)
        if customer is None:
            raise CustomerNotFoundError(str(customer_id))

        # 2. 通过领域服务创建跟进记录
        follow_up = await self._follow_up_service.create_follow_up(
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

        # 3. 更新客户的 last_follow_at（跨域副作用）
        customer.last_follow_at = datetime.now(UTC)
        customer.updated_at = datetime.now(UTC)
        await self._customer_repo.update(customer)

        return follow_up


class ReminderHandler:
    """扫描到期跟进 → 写入 notifications 表。由 SAQ 定时任务调用。"""

    def __init__(
        self,
        follow_up_repo: AbstractFollowUpRepository,
        notification_repo: NotificationRepository,
    ) -> None:
        self._follow_up_repo = follow_up_repo
        self._notification_repo = notification_repo

    async def check_and_notify(self) -> int:
        """扫描所有到期提醒，创建通知记录。返回创建的通知数。"""
        now = datetime.now(UTC)
        due_follow_ups = await self._follow_up_repo.find_due_reminders(before=now)

        count = 0
        for fu in due_follow_ups:
            if not fu.is_reminder_due:
                continue
            if fu.created_by is None:
                continue

            await self._notification_repo.create(
                tenant_id=fu.tenant_id,
                user_id=fu.created_by,
                type="follow_up_reminder",
                title="跟进提醒",
                content="客户跟进已到期，请及时跟进",
                ref_type="follow_up",
                ref_id=fu.id,
            )

            # 清除 next_follow_at 避免重复通知
            fu.next_follow_at = None
            await self._follow_up_repo.update(fu)
            count += 1

        return count
