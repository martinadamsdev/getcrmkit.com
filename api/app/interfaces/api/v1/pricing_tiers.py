import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.product.entities import PricingTier
from app.domain.product.exceptions import PricingTierNotFoundError
from app.domain.product.services import PricingService, PricingTierService
from app.interfaces.api.deps import get_current_user, get_db, get_pricing_service, get_pricing_tier_service
from app.interfaces.schemas.product import (
    CreatePricingTierRequest,
    GetMultiplierResponse,
    PricingTierResponse,
    UpdatePricingTierRequest,
)

router = APIRouter(prefix="/api/v1/pricing-tiers", tags=["pricing-tiers"])


def _tier_response(t: PricingTier) -> PricingTierResponse:
    return PricingTierResponse(
        id=t.id,
        name=t.name,
        min_qty=t.min_qty,
        max_qty=t.max_qty,
        multiplier=t.multiplier,
        is_default=t.is_default,
        position=t.position,
        created_at=t.created_at,
        updated_at=t.updated_at,
    )


@router.get("/multiplier")
async def get_multiplier(
    qty: int,
    current_user: User = Depends(get_current_user),
    service: PricingService = Depends(get_pricing_service),
) -> GetMultiplierResponse:
    """No match returns multiplier=1.0000 (original price, no markup)."""
    multiplier = await service.get_multiplier(tenant_id=current_user.tenant_id, qty=qty)
    return GetMultiplierResponse(qty=qty, multiplier=multiplier)


@router.post("", response_model=PricingTierResponse, status_code=201)
async def create_pricing_tier(
    body: CreatePricingTierRequest,
    current_user: User = Depends(get_current_user),
    service: PricingTierService = Depends(get_pricing_tier_service),
    session: AsyncSession = Depends(get_db),
) -> PricingTierResponse:
    tier = await service.create_tier(
        tenant_id=current_user.tenant_id,
        name=body.name,
        min_qty=body.min_qty,
        max_qty=body.max_qty,
        multiplier=body.multiplier,
        is_default=body.is_default,
        position=body.position,
    )
    await session.commit()
    return _tier_response(tier)


@router.get("", response_model=list[PricingTierResponse])
async def list_pricing_tiers(
    current_user: User = Depends(get_current_user),
    service: PricingTierService = Depends(get_pricing_tier_service),
) -> list[PricingTierResponse]:
    tiers = await service.get_all(current_user.tenant_id)
    return [_tier_response(t) for t in tiers]


@router.put("/{tier_id}", response_model=PricingTierResponse)
async def update_pricing_tier(
    tier_id: uuid.UUID,
    body: UpdatePricingTierRequest,
    current_user: User = Depends(get_current_user),
    service: PricingTierService = Depends(get_pricing_tier_service),
    session: AsyncSession = Depends(get_db),
) -> PricingTierResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        tier = await service.update_tier(
            tenant_id=current_user.tenant_id,
            tier_id=tier_id,
            **updates,
        )
        await session.commit()
        return _tier_response(tier)
    except PricingTierNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{tier_id}", status_code=204)
async def delete_pricing_tier(
    tier_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: PricingTierService = Depends(get_pricing_tier_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_tier(tenant_id=current_user.tenant_id, tier_id=tier_id)
        await session.commit()
    except PricingTierNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
