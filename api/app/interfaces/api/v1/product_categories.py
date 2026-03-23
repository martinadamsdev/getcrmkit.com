import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.product.entities import ProductCategory
from app.domain.product.exceptions import (
    CategoryHasChildrenError,
    CategoryInUseError,
    CategoryNotFoundError,
    MaxCategoryDepthError,
)
from app.domain.product.services import ProductCategoryService
from app.interfaces.api.deps import get_current_user, get_db, get_product_category_service
from app.interfaces.schemas.product import CategoryResponse, CreateCategoryRequest, UpdateCategoryRequest

router = APIRouter(prefix="/api/v1/product-categories", tags=["product-categories"])


def _category_response(c: ProductCategory) -> CategoryResponse:
    return CategoryResponse(
        id=c.id,
        name=c.name,
        parent_id=c.parent_id,
        level=c.level,
        position=c.position,
        created_at=c.created_at,
    )


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    body: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),
    service: ProductCategoryService = Depends(get_product_category_service),
    session: AsyncSession = Depends(get_db),
) -> CategoryResponse:
    try:
        cat = await service.create_category(
            name=body.name,
            tenant_id=current_user.tenant_id,
            parent_id=body.parent_id,
            position=body.position,
        )
        await session.commit()
        return _category_response(cat)
    except MaxCategoryDepthError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.get("", response_model=list[CategoryResponse])
async def list_categories(
    current_user: User = Depends(get_current_user),
    service: ProductCategoryService = Depends(get_product_category_service),
) -> list[CategoryResponse]:
    categories = await service.get_all(current_user.tenant_id)
    return [_category_response(c) for c in categories]


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: uuid.UUID,
    body: UpdateCategoryRequest,
    current_user: User = Depends(get_current_user),
    service: ProductCategoryService = Depends(get_product_category_service),
    session: AsyncSession = Depends(get_db),
) -> CategoryResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        cat = await service.update_category(
            tenant_id=current_user.tenant_id,
            category_id=category_id,
            **updates,
        )
        await session.commit()
        return _category_response(cat)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ProductCategoryService = Depends(get_product_category_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_category(tenant_id=current_user.tenant_id, category_id=category_id)
        await session.commit()
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except CategoryHasChildrenError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e
    except CategoryInUseError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e
