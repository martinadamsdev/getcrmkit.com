import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.customer.entities import SavedView
from app.domain.customer.exceptions import DuplicateViewNameError, SavedViewNotFoundError
from app.domain.customer.services import SavedViewService
from app.interfaces.api.deps import get_current_user, get_db, get_saved_view_service
from app.interfaces.schemas.customer import (
    CreateSavedViewRequest,
    SavedViewResponse,
    UpdateSavedViewRequest,
)

router = APIRouter(prefix="/api/v1/saved-views", tags=["saved-views"])


def _view_response(view: SavedView) -> SavedViewResponse:
    return SavedViewResponse(
        id=view.id,
        name=view.name,
        entity_type=view.entity_type,
        filter_config=view.filter_config,
        is_default=view.is_default,
        position=view.position,
        created_at=view.created_at,
        updated_at=view.updated_at,
    )


@router.get("", response_model=list[SavedViewResponse])
async def list_saved_views(
    entity_type: str = "customer",
    current_user: User = Depends(get_current_user),
    service: SavedViewService = Depends(get_saved_view_service),
) -> list[SavedViewResponse]:
    views = await service.get_all(tenant_id=current_user.tenant_id, user_id=current_user.id, entity_type=entity_type)
    return [_view_response(v) for v in views]


@router.post("", response_model=SavedViewResponse, status_code=201)
async def create_saved_view(
    body: CreateSavedViewRequest,
    current_user: User = Depends(get_current_user),
    service: SavedViewService = Depends(get_saved_view_service),
    session: AsyncSession = Depends(get_db),
) -> SavedViewResponse:
    try:
        view = await service.create_view(
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            name=body.name,
            entity_type=body.entity_type,
            filter_config=body.filter_config,
            is_default=body.is_default,
            position=body.position,
        )
        await session.commit()
        return _view_response(view)
    except DuplicateViewNameError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e


@router.put("/{view_id}", response_model=SavedViewResponse)
async def update_saved_view(
    view_id: uuid.UUID,
    body: UpdateSavedViewRequest,
    current_user: User = Depends(get_current_user),
    service: SavedViewService = Depends(get_saved_view_service),
    session: AsyncSession = Depends(get_db),
) -> SavedViewResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        view = await service.update_view(
            id=view_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            **updates,
        )
        await session.commit()
        return _view_response(view)
    except SavedViewNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except DuplicateViewNameError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{view_id}", status_code=204)
async def delete_saved_view(
    view_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SavedViewService = Depends(get_saved_view_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_view(
            id=view_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
        )
        await session.commit()
    except SavedViewNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
