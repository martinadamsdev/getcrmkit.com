import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.product.entities import ProductVariant
from app.domain.product.exceptions import ProductNotFoundError, VariantNameRequiredError, VariantNotFoundError
from app.domain.product.services import ProductVariantService
from app.interfaces.api.deps import get_current_user, get_db, get_product_variant_service
from app.interfaces.schemas.product import CreateVariantRequest, UpdateVariantRequest, VariantResponse

router = APIRouter(prefix="/api/v1/products/{product_id}/variants", tags=["product-variants"])


def _variant_response(v: ProductVariant) -> VariantResponse:
    return VariantResponse(
        id=v.id,
        product_id=v.product_id,
        variant_name=v.variant_name,
        sku=v.sku,
        material=v.material,
        color=v.color,
        color_code=v.color_code,
        size=v.size,
        cost_price=v.cost_price,
        cost_currency=v.cost_currency,
        is_active=v.is_active,
        created_at=v.created_at,
        updated_at=v.updated_at,
    )


@router.post("", response_model=VariantResponse, status_code=201)
async def create_variant(
    product_id: uuid.UUID,
    body: CreateVariantRequest,
    current_user: User = Depends(get_current_user),
    service: ProductVariantService = Depends(get_product_variant_service),
    session: AsyncSession = Depends(get_db),
) -> VariantResponse:
    try:
        variant = await service.create_variant(
            product_id=product_id,
            variant_name=body.variant_name,
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            sku=body.sku,
            material=body.material,
            color=body.color,
            color_code=body.color_code,
            size=body.size,
            cost_price=body.cost_price,
            cost_currency=body.cost_currency,
            is_active=body.is_active,
        )
        await session.commit()
        return _variant_response(variant)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except VariantNameRequiredError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.get("", response_model=list[VariantResponse])
async def list_variants(
    product_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ProductVariantService = Depends(get_product_variant_service),
) -> list[VariantResponse]:
    variants = await service.list_by_product(tenant_id=current_user.tenant_id, product_id=product_id)
    return [_variant_response(v) for v in variants]


@router.put("/{variant_id}", response_model=VariantResponse)
async def update_variant(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    body: UpdateVariantRequest,
    current_user: User = Depends(get_current_user),
    service: ProductVariantService = Depends(get_product_variant_service),
    session: AsyncSession = Depends(get_db),
) -> VariantResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        variant = await service.update_variant(
            tenant_id=current_user.tenant_id,
            variant_id=variant_id,
            **updates,
        )
        await session.commit()
        return _variant_response(variant)
    except VariantNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{variant_id}", status_code=204)
async def delete_variant(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ProductVariantService = Depends(get_product_variant_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_variant(tenant_id=current_user.tenant_id, variant_id=variant_id)
        await session.commit()
    except VariantNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
