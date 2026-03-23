"""SAQ 定时任务：每 15 分钟扫描到期跟进，创建站内通知。"""

from typing import Any

from saq import CronJob

from app.application.follow_up.commands import ReminderHandler
from app.infra.database.connection import async_session_factory
from app.infra.database.repositories.follow_up_repository import FollowUpRepository
from app.infra.database.repositories.notification_repository import NotificationRepository


async def check_follow_up_reminders(ctx: dict[str, Any]) -> None:
    """SAQ task：扫描到期跟进 → 写入 notifications 表。"""
    async with async_session_factory() as session:
        handler = ReminderHandler(
            follow_up_repo=FollowUpRepository(session),
            notification_repo=NotificationRepository(session),
        )
        count = await handler.check_and_notify()
        await session.commit()
        if count > 0:
            print(f"[follow_up_reminders] Created {count} notifications")


# 注册到 SAQ worker 的 cron_jobs
follow_up_cron_jobs = [
    CronJob(  # type: ignore[type-var]
        check_follow_up_reminders,
        cron="*/15 * * * *",  # 每 15 分钟
    ),
]
