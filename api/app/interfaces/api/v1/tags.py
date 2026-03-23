import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.customer.entities import Tag
from app.domain.customer.exceptions import CustomerNotFoundError, DuplicateTagError, TagNotFoundError
from app.domain.customer.services import TagService
from app.interfaces.api.deps import get_current_user, get_db, get_tag_service
from app.interfaces.schemas.customer import (
    CreateTagRequest,
    TagCustomerRequest,
    TagResponse,
    UpdateTagRequest,
)

router = APIRouter(prefix="/api/v1/tags", tags=["tags"])
customer_tags_router = APIRouter(prefix="/api/v1/customers", tags=["tags"])


def _tag_response(tag: Tag) -> TagResponse:
    return TagResponse(
        id=tag.id,
        name=tag.name,
        color=tag.color,
        group_name=tag.group_name,
        position=tag.position,
        created_at=tag.created_at,
        updated_at=tag.updated_at,
    )


@router.get("", response_model=list[TagResponse])
async def list_tags(
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
) -> list[TagResponse]:
    tags = await service.get_all(current_user.tenant_id)
    return [_tag_response(t) for t in tags]


@router.post("", response_model=TagResponse, status_code=201)
async def create_tag(
    body: CreateTagRequest,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
    session: AsyncSession = Depends(get_db),
) -> TagResponse:
    try:
        tag = await service.create_tag(
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            name=body.name,
            color=body.color,
            group_name=body.group_name,
            position=body.position,
        )
        await session.commit()
        return _tag_response(tag)
    except DuplicateTagError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: uuid.UUID,
    body: UpdateTagRequest,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
    session: AsyncSession = Depends(get_db),
) -> TagResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        tag = await service.update_tag(
            tenant_id=current_user.tenant_id,
            tag_id=tag_id,
            **updates,
        )
        await session.commit()
        return _tag_response(tag)
    except TagNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_tag(tenant_id=current_user.tenant_id, tag_id=tag_id)
        await session.commit()
    except TagNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@customer_tags_router.post("/{customer_id}/tags", status_code=201)
async def tag_customer(
    customer_id: uuid.UUID,
    body: TagCustomerRequest,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
    session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    try:
        await service.tag_customer(
            tenant_id=current_user.tenant_id,
            customer_id=customer_id,
            tag_id=body.tag_id,
        )
        await session.commit()
        return {}
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except TagNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@customer_tags_router.delete("/{customer_id}/tags/{tag_id}", status_code=204)
async def untag_customer(
    customer_id: uuid.UUID,
    tag_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    await service.untag_customer(
        tenant_id=current_user.tenant_id,
        customer_id=customer_id,
        tag_id=tag_id,
    )
    await session.commit()
