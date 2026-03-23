from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database.models.follow_up import FollowUpModel


@dataclass(frozen=True)
class FollowUpReportItem:
    date: str  # YYYY-MM-DD / YYYY-Www / YYYY-MM / YYYY
    total_count: int
    method_breakdown: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class FollowUpReport:
    period: str  # daily / weekly / monthly / yearly
    start_date: str
    end_date: str
    total: int
    items: list[FollowUpReportItem] = field(default_factory=list)


class ReportQueryService:
    """CQRS 读模型 -- 直接查询数据库，不经过领域仓储。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_report(
        self,
        tenant_id: uuid.UUID,
        period: Literal["daily", "weekly", "monthly", "yearly"],
        *,
        created_by: uuid.UUID | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> FollowUpReport:
        now = datetime.now(UTC)

        if start_date is None or end_date is None:
            start_date, end_date = self._default_range(period, now)

        conditions = [
            FollowUpModel.tenant_id == tenant_id,
            FollowUpModel.deleted_at.is_(None),
            FollowUpModel.created_at >= start_date,
            FollowUpModel.created_at <= end_date,
        ]
        if created_by is not None:
            conditions.append(FollowUpModel.created_by == created_by)

        # 总数
        count_stmt = select(func.count()).select_from(FollowUpModel).where(*conditions)
        total = (await self._session.execute(count_stmt)).scalar_one()

        # 按周期分组 + 方式分组
        date_trunc_key = {
            "daily": "day",
            "weekly": "week",
            "monthly": "month",
            "yearly": "year",
        }[period]

        group_stmt = (
            select(
                func.date_trunc(date_trunc_key, FollowUpModel.created_at).label("period_start"),
                FollowUpModel.method,
                func.count().label("cnt"),
            )
            .where(*conditions)
            .group_by("period_start", FollowUpModel.method)
            .order_by("period_start")
        )
        rows = (await self._session.execute(group_stmt)).all()

        # 聚合为 FollowUpReportItem
        items_map: dict[str, FollowUpReportItem] = {}
        for row in rows:
            key = row.period_start.strftime("%Y-%m-%d")
            if key not in items_map:
                items_map[key] = FollowUpReportItem(date=key, total_count=0, method_breakdown={})
            item = items_map[key]
            # frozen dataclass, 需要用 object.__setattr__
            object.__setattr__(item, "total_count", item.total_count + row.cnt)
            item.method_breakdown[row.method] = row.cnt

        return FollowUpReport(
            period=period,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            total=total,
            items=list(items_map.values()),
        )

    @staticmethod
    def _default_range(period: str, now: datetime) -> tuple[datetime, datetime]:
        if period == "daily":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "weekly":
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "monthly":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
        else:  # yearly
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
        return start, end


class TimelineQueryService:
    """客户跟进时间线查询 -- 按时间倒序返回。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_timeline(
        self,
        customer_id: uuid.UUID,
        tenant_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        conditions = [
            FollowUpModel.customer_id == customer_id,
            FollowUpModel.tenant_id == tenant_id,
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
        items: list[dict[str, Any]] = [
            {
                "id": str(m.id),
                "method": m.method,
                "stage": m.stage,
                "content": m.content,
                "customer_response": m.customer_response,
                "next_follow_at": m.next_follow_at.isoformat() if m.next_follow_at else None,
                "attachment_urls": m.attachment_urls or [],
                "tags": m.tags or [],
                "created_by": str(m.created_by),
                "created_at": m.created_at.isoformat(),
            }
            for m in result.scalars()
        ]
        return items, total
