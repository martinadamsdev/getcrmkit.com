import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.shared.task_queue import AbstractTaskQueue
from app.domain.auth.entities import User
from app.domain.customer.entities import DataJob
from app.domain.customer.enums import DataJobStatus
from app.domain.product.entities import Product
from app.domain.product.exceptions import ProductNameRequiredError, ProductNotFoundError
from app.domain.product.services import ProductService
from app.domain.product.value_objects import ProductFilter
from app.infra.database.repositories.data_job_repository import DataJobRepository
from app.interfaces.api.deps import get_current_user, get_db, get_product_service, get_task_queue
from app.interfaces.schemas.customer import PaginatedResponse
from app.interfaces.schemas.product import (
    CreateProductRequest,
    ExportProductRequest,
    ProductResponse,
    UpdateProductRequest,
)

router = APIRouter(prefix="/api/v1/products", tags=["products"])


def _product_response(p: Product) -> ProductResponse:
    return ProductResponse(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category_id=p.category_id,
        description=p.description,
        image_url=p.image_url,
        material=p.material,
        dimensions=p.dimensions,
        weight=p.weight,
        color=p.color,
        packing=p.packing,
        cost_price=p.cost_price,
        cost_currency=p.cost_currency,
        selling_price=p.selling_price,
        selling_currency=p.selling_currency,
        is_active=p.is_active,
        custom_fields=p.custom_fields,
        created_by=p.created_by,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )


# --- Static path endpoints (MUST be before /{product_id}) ---


@router.post("/import", status_code=202)
async def import_products(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    task_queue: AbstractTaskQueue = Depends(get_task_queue),
) -> dict[str, str]:
    import tempfile

    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=422, detail={"code": "INVALID_FILE", "message": "Only .xlsx files accepted"})

    contents = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp.write(contents)

    job_repo = DataJobRepository(session)
    job = DataJob(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        entity_type="product",
        job_type="import",
        file_name=file.filename,
        file_path=tmp.name,
        status=DataJobStatus.PENDING,
        created_by=current_user.id,
    )
    job = await job_repo.create(job)
    await session.commit()
    await task_queue.enqueue("process_product_import", job_id=str(job.id))
    return {"job_id": str(job.id)}


@router.post("/export", status_code=202)
async def export_products(
    body: ExportProductRequest | None = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    task_queue: AbstractTaskQueue = Depends(get_task_queue),
) -> dict[str, str]:
    job_repo = DataJobRepository(session)
    filter_config = body.model_dump(exclude_none=True) if body else None
    job = DataJob(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        entity_type="product",
        job_type="export",
        file_name="products_export.xlsx",
        filter_config=filter_config if filter_config else None,
        status=DataJobStatus.PENDING,
        created_by=current_user.id,
    )
    job = await job_repo.create(job)
    await session.commit()
    await task_queue.enqueue("process_product_export", job_id=str(job.id))
    return {"job_id": str(job.id)}


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    body: CreateProductRequest,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
    session: AsyncSession = Depends(get_db),
) -> ProductResponse:
    try:
        product = await service.create_product(
            name=body.name,
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            sku=body.sku,
            category_id=body.category_id,
            description=body.description,
            image_url=body.image_url,
            material=body.material,
            dimensions=body.dimensions,
            weight=body.weight,
            color=body.color,
            packing=body.packing,
            cost_price=body.cost_price,
            cost_currency=body.cost_currency,
            selling_price=body.selling_price,
            selling_currency=body.selling_currency,
            is_active=body.is_active,
            custom_fields=body.custom_fields,
        )
        await session.commit()
        return _product_response(product)
    except ProductNameRequiredError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.get("", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    category_id: uuid.UUID | None = None,
    is_active: bool | None = None,
    min_cost: Decimal | None = None,
    max_cost: Decimal | None = None,
    min_selling: Decimal | None = None,
    max_selling: Decimal | None = None,
    sort_by: str = "created_at",
    sort: str = "desc",
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
) -> PaginatedResponse[ProductResponse]:
    filters = ProductFilter(
        keyword=keyword,
        category_id=category_id,
        is_active=is_active,
        min_cost=min_cost,
        max_cost=max_cost,
        min_selling=min_selling,
        max_selling=max_selling,
        sort_by=sort_by,  # type: ignore[arg-type]
        sort=sort,  # type: ignore[arg-type]
    )
    items, total = await service.list_products(current_user.tenant_id, page=page, page_size=page_size, filters=filters)
    return PaginatedResponse(
        items=[_product_response(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    try:
        product = await service.get_product(tenant_id=current_user.tenant_id, product_id=product_id)
        return _product_response(product)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    body: UpdateProductRequest,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
    session: AsyncSession = Depends(get_db),
) -> ProductResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        product = await service.update_product(
            tenant_id=current_user.tenant_id,
            product_id=product_id,
            **updates,
        )
        await session.commit()
        return _product_response(product)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.soft_delete_product(tenant_id=current_user.tenant_id, product_id=product_id)
        await session.commit()
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
