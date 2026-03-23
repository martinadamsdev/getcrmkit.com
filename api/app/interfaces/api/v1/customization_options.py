import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.product.entities import CustomizationOption
from app.domain.product.exceptions import CustomizationOptionNameRequiredError, CustomizationOptionNotFoundError
from app.domain.product.services import CustomizationOptionService
from app.interfaces.api.deps import get_current_user, get_customization_option_service, get_db
from app.interfaces.schemas.product import (
    CreateCustomizationOptionRequest,
    CustomizationOptionResponse,
    UpdateCustomizationOptionRequest,
)

router = APIRouter(prefix="/api/v1/customization-options", tags=["customization-options"])


def _option_response(o: CustomizationOption) -> CustomizationOptionResponse:
    return CustomizationOptionResponse(
        id=o.id,
        name=o.name,
        description=o.description,
        extra_cost=o.extra_cost,
        extra_currency=o.extra_currency,
        is_active=o.is_active,
        created_at=o.created_at,
        updated_at=o.updated_at,
    )


@router.post("", response_model=CustomizationOptionResponse, status_code=201)
async def create_option(
    body: CreateCustomizationOptionRequest,
    current_user: User = Depends(get_current_user),
    service: CustomizationOptionService = Depends(get_customization_option_service),
    session: AsyncSession = Depends(get_db),
) -> CustomizationOptionResponse:
    try:
        option = await service.create_option(
            name=body.name,
            tenant_id=current_user.tenant_id,
            description=body.description,
            extra_cost=body.extra_cost,
            extra_currency=body.extra_currency,
            is_active=body.is_active,
        )
        await session.commit()
        return _option_response(option)
    except CustomizationOptionNameRequiredError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.get("", response_model=list[CustomizationOptionResponse])
async def list_options(
    current_user: User = Depends(get_current_user),
    service: CustomizationOptionService = Depends(get_customization_option_service),
) -> list[CustomizationOptionResponse]:
    options = await service.get_all(current_user.tenant_id)
    return [_option_response(o) for o in options]


@router.put("/{option_id}", response_model=CustomizationOptionResponse)
async def update_option(
    option_id: uuid.UUID,
    body: UpdateCustomizationOptionRequest,
    current_user: User = Depends(get_current_user),
    service: CustomizationOptionService = Depends(get_customization_option_service),
    session: AsyncSession = Depends(get_db),
) -> CustomizationOptionResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        option = await service.update_option(
            tenant_id=current_user.tenant_id,
            option_id=option_id,
            **updates,
        )
        await session.commit()
        return _option_response(option)
    except CustomizationOptionNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{option_id}", status_code=204)
async def delete_option(
    option_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CustomizationOptionService = Depends(get_customization_option_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_option(tenant_id=current_user.tenant_id, option_id=option_id)
        await session.commit()
    except CustomizationOptionNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
