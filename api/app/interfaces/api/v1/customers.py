import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.customer.entities import Customer, CustomerGrade, Tag
from app.domain.customer.exceptions import CustomerNameRequiredError, CustomerNotFoundError
from app.domain.customer.services import CustomerGradeService, CustomerService, TagService
from app.interfaces.api.deps import get_current_user, get_customer_service, get_db, get_grade_service, get_tag_service
from app.interfaces.schemas.customer import (
    CreateCustomerRequest,
    CustomerGradeResponse,
    CustomerResponse,
    PaginatedResponse,
    TagResponse,
    UpdateCustomerRequest,
)

router = APIRouter(prefix="/api/v1/customers", tags=["customers"])


def _grade_response(grade: CustomerGrade) -> CustomerGradeResponse:
    return CustomerGradeResponse(
        id=grade.id,
        name=grade.name,
        label=grade.label,
        color=grade.color,
        position=grade.position,
        created_at=grade.created_at,
        updated_at=grade.updated_at,
    )


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


def _customer_response(customer: Customer, grade: CustomerGrade | None = None, tags: list[Tag] | None = None) -> CustomerResponse:
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        country=customer.country,
        region=customer.region,
        city=customer.city,
        address=customer.address,
        industry=customer.industry,
        company_size=customer.company_size,
        website=customer.website,
        source=customer.source,
        grade_id=customer.grade_id,
        grade=_grade_response(grade) if grade else None,
        follow_status=customer.follow_status.value,
        main_products=customer.main_products,
        annual_volume=customer.annual_volume,
        current_supplier=customer.current_supplier,
        decision_process=customer.decision_process,
        owner_id=customer.owner_id,
        claimed_at=customer.claimed_at,
        last_follow_at=customer.last_follow_at,
        custom_fields=customer.custom_fields,
        tags=[_tag_response(t) for t in (tags or [])],
        created_at=customer.created_at,
        updated_at=customer.updated_at,
    )


@router.get("", response_model=PaginatedResponse[CustomerResponse])
async def list_customers(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
) -> PaginatedResponse[CustomerResponse]:
    items, total = await service.list_customers(current_user.tenant_id, page, page_size)
    return PaginatedResponse(
        items=[_customer_response(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    body: CreateCustomerRequest,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
    session: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    try:
        customer = await service.create_customer(
            name=body.name,
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            owner_id=current_user.id,
            country=body.country,
            region=body.region,
            city=body.city,
            address=body.address,
            industry=body.industry,
            company_size=body.company_size,
            website=body.website,
            source=body.source,
            grade_id=body.grade_id,
            main_products=body.main_products,
            annual_volume=body.annual_volume,
            current_supplier=body.current_supplier,
            decision_process=body.decision_process,
            custom_fields=body.custom_fields,
        )
        await session.commit()
        return _customer_response(customer)
    except CustomerNameRequiredError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
    grade_service: CustomerGradeService = Depends(get_grade_service),
    tag_service: TagService = Depends(get_tag_service),
) -> CustomerResponse:
    try:
        customer = await service.get_customer(current_user.tenant_id, customer_id)
        grade = None
        if customer.grade_id:
            grade = await grade_service.get_grade(current_user.tenant_id, customer.grade_id)
        tags = await tag_service.get_tags_for_customer(current_user.tenant_id, customer.id)
        return _customer_response(customer, grade=grade, tags=tags)
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: uuid.UUID,
    body: UpdateCustomerRequest,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
    session: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        customer = await service.update_customer(
            tenant_id=current_user.tenant_id,
            customer_id=customer_id,
            **updates,
        )
        await session.commit()
        return _customer_response(customer)
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.soft_delete_customer(
            tenant_id=current_user.tenant_id,
            customer_id=customer_id,
        )
        await session.commit()
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
