import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.follow_up.commands import CreateFollowUpHandler
from app.application.follow_up.queries import ReportQueryService
from app.domain.auth.entities import User
from app.domain.follow_up.entities import FollowUp
from app.domain.follow_up.enums import FollowUpMethod
from app.domain.follow_up.exceptions import FollowUpContentRequiredError, FollowUpNotFoundError
from app.domain.follow_up.services import FollowUpService
from app.interfaces.api.deps import get_current_user, get_db, get_follow_up_handler, get_follow_up_service
from app.interfaces.schemas.customer import PaginatedResponse
from app.interfaces.schemas.follow_up import (
    CreateFollowUpRequest,
    FollowUpReportResponse,
    FollowUpResponse,
    ReportItemResponse,
    UpdateFollowUpRequest,
)

router = APIRouter(prefix="/api/v1/follow-ups", tags=["follow-ups"])


def _follow_up_response(fu: FollowUp) -> FollowUpResponse:
    return FollowUpResponse(
        id=fu.id,
        customer_id=fu.customer_id,
        contact_id=fu.contact_id,
        method=fu.method.value,
        stage=fu.stage,
        content=fu.content,
        customer_response=fu.customer_response,
        next_follow_at=fu.next_follow_at,
        attachment_urls=fu.attachment_urls,
        tags=fu.tags,
        created_by=fu.created_by,
        created_at=fu.created_at,
        updated_at=fu.updated_at,
    )


# --- Static path endpoints (MUST be before /{follow_up_id}) ---


@router.get("/report", response_model=FollowUpReportResponse)
async def get_report(
    period: Literal["daily", "weekly", "monthly", "yearly"] = "daily",
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> FollowUpReportResponse:
    service = ReportQueryService(session)
    report = await service.get_report(
        tenant_id=current_user.tenant_id,
        period=period,
        created_by=current_user.id,
    )
    return FollowUpReportResponse(
        period=report.period,
        start_date=report.start_date,
        end_date=report.end_date,
        total=report.total,
        items=[
            ReportItemResponse(
                date=item.date,
                total_count=item.total_count,
                method_breakdown=item.method_breakdown,
            )
            for item in report.items
        ],
    )


@router.post("", response_model=FollowUpResponse, status_code=201)
async def create_follow_up(
    body: CreateFollowUpRequest,
    current_user: User = Depends(get_current_user),
    handler: CreateFollowUpHandler = Depends(get_follow_up_handler),
    session: AsyncSession = Depends(get_db),
) -> FollowUpResponse:
    from app.domain.customer.exceptions import CustomerNotFoundError

    try:
        follow_up = await handler.handle(
            customer_id=body.customer_id,
            content=body.content,
            method=FollowUpMethod(body.method),
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            contact_id=body.contact_id,
            stage=body.stage,
            customer_response=body.customer_response,
            next_follow_at=body.next_follow_at,
            attachment_urls=body.attachment_urls,
            tags=body.tags,
        )
        await session.commit()
        return _follow_up_response(follow_up)
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except FollowUpContentRequiredError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.get("", response_model=PaginatedResponse[FollowUpResponse])
async def list_follow_ups(
    page: int = 1,
    page_size: int = 20,
    tags: list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    service: FollowUpService = Depends(get_follow_up_service),
) -> PaginatedResponse[FollowUpResponse]:
    items, total = await service.list_by_tenant(
        current_user.tenant_id,
        page=page,
        page_size=page_size,
        tags=tags,
        created_by=None,
    )
    return PaginatedResponse(
        items=[_follow_up_response(fu) for fu in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{follow_up_id}", response_model=FollowUpResponse)
async def get_follow_up(
    follow_up_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: FollowUpService = Depends(get_follow_up_service),
) -> FollowUpResponse:
    try:
        follow_up = await service.get_follow_up(current_user.tenant_id, follow_up_id)
        return _follow_up_response(follow_up)
    except FollowUpNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.put("/{follow_up_id}", response_model=FollowUpResponse)
async def update_follow_up(
    follow_up_id: uuid.UUID,
    body: UpdateFollowUpRequest,
    current_user: User = Depends(get_current_user),
    service: FollowUpService = Depends(get_follow_up_service),
    session: AsyncSession = Depends(get_db),
) -> FollowUpResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        follow_up = await service.update_follow_up(
            tenant_id=current_user.tenant_id,
            follow_up_id=follow_up_id,
            **updates,
        )
        await session.commit()
        return _follow_up_response(follow_up)
    except FollowUpNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{follow_up_id}", status_code=204)
async def delete_follow_up(
    follow_up_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: FollowUpService = Depends(get_follow_up_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.soft_delete_follow_up(
            tenant_id=current_user.tenant_id,
            follow_up_id=follow_up_id,
        )
        await session.commit()
    except FollowUpNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
