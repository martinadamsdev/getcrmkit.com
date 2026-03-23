import tempfile
import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.customer.export_service import CustomerExportService
from app.application.customer.import_service import CustomerImportService
from app.application.customer.queries import Customer360QueryService
from app.domain.auth.entities import User
from app.domain.customer.entities import Contact, Customer, CustomerGrade, Tag
from app.domain.customer.enums import FollowUpStage
from app.domain.customer.exceptions import CustomerNameRequiredError, CustomerNotFoundError
from app.domain.customer.services import CustomerGradeService, CustomerService, DuplicateChecker, TagService
from app.domain.customer.value_objects import CustomerFilter
from app.interfaces.api.deps import (
    get_360_query_service,
    get_current_user,
    get_customer_service,
    get_db,
    get_duplicate_checker,
    get_export_service,
    get_grade_service,
    get_import_service,
    get_tag_service,
)
from app.interfaces.schemas.customer import (
    CheckDuplicateRequest,
    CheckDuplicateResponse,
    ContactResponse,
    CreateCustomerRequest,
    Customer360Response,
    Customer360StatsResponse,
    CustomerGradeResponse,
    CustomerResponse,
    DuplicateMatchResponse,
    ExportCustomerRequest,
    ExportCustomerResponse,
    ImportCustomerResponse,
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


def _contact_response(contact: Contact) -> ContactResponse:
    return ContactResponse(
        id=contact.id,
        customer_id=contact.customer_id,
        name=contact.name,
        title=contact.title,
        email=contact.email,
        phone=contact.phone,
        whatsapp=contact.whatsapp,
        skype=contact.skype,
        linkedin=contact.linkedin,
        wechat=contact.wechat,
        is_primary=contact.is_primary,
        notes=contact.notes,
        custom_fields=contact.custom_fields,
        created_at=contact.created_at,
        updated_at=contact.updated_at,
    )


def _customer_response(
    customer: Customer, grade: CustomerGrade | None = None, tags: list[Tag] | None = None
) -> CustomerResponse:
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


# --- Static path endpoints (MUST be before /{customer_id}) ---


@router.post("/check-duplicate", response_model=CheckDuplicateResponse)
async def check_duplicate(
    body: CheckDuplicateRequest,
    current_user: User = Depends(get_current_user),
    checker: DuplicateChecker = Depends(get_duplicate_checker),
) -> CheckDuplicateResponse:
    matches = await checker.check(
        tenant_id=current_user.tenant_id,
        name=body.name,
        email=body.email,
    )
    return CheckDuplicateResponse(
        duplicates=[
            DuplicateMatchResponse(
                customer_id=m.customer_id,
                customer_name=m.customer_name,
                match_type=m.match_type,
                matched_value=m.matched_value,
            )
            for m in matches
        ]
    )


ALLOWED_IMPORT_EXTENSIONS = {".xlsx", ".xls", ".csv"}


@router.post("/import", response_model=ImportCustomerResponse, status_code=202)
async def import_customers(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    service: CustomerImportService = Depends(get_import_service),
    session: AsyncSession = Depends(get_db),
) -> ImportCustomerResponse:
    file_name = file.filename or ""
    ext = ""
    if "." in file_name:
        ext = "." + file_name.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_IMPORT_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail={"code": "INVALID_IMPORT_FILE", "message": f"Invalid import file: {file_name}"},
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    job = await service.start_import(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        file_name=file_name,
        file_path=tmp_path,
    )
    await session.commit()
    return ImportCustomerResponse(job_id=job.id)


@router.post("/export", response_model=ExportCustomerResponse, status_code=202)
async def export_customers(
    body: ExportCustomerRequest | None = None,
    current_user: User = Depends(get_current_user),
    service: CustomerExportService = Depends(get_export_service),
    session: AsyncSession = Depends(get_db),
) -> ExportCustomerResponse:
    filter_config = body.filter_config if body else None
    job = await service.start_export(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        filter_config=filter_config,
    )
    await session.commit()
    return ExportCustomerResponse(job_id=job.id)


@router.get("", response_model=PaginatedResponse[CustomerResponse])
async def list_customers(
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    grade_id: uuid.UUID | None = None,
    source: str | None = None,
    follow_status: str | None = None,
    country: str | None = None,
    industry: str | None = None,
    tag_ids: list[uuid.UUID] | None = Query(default=None),
    owner_id: uuid.UUID | None = None,
    sort_by: Literal["created_at", "name", "last_follow_at"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
) -> PaginatedResponse[CustomerResponse]:
    filters = None
    if (
        any([keyword, grade_id, source, follow_status, country, industry, tag_ids, owner_id])
        or sort_by != "created_at"
        or sort_order != "desc"
    ):
        filters = CustomerFilter(
            keyword=keyword,
            grade_id=grade_id,
            source=source,
            follow_status=FollowUpStage(follow_status) if follow_status else None,
            country=country,
            industry=industry,
            tag_ids=tag_ids or [],
            owner_id=owner_id,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    items, total = await service.list_customers(current_user.tenant_id, page, page_size, filters=filters)
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


@router.get("/{customer_id}/360", response_model=Customer360Response)
async def get_customer_360(
    customer_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: Customer360QueryService = Depends(get_360_query_service),
) -> Customer360Response:
    try:
        view = await service.get_360_view(customer_id, current_user.tenant_id)
        return Customer360Response(
            customer=_customer_response(view.customer, grade=view.grade, tags=view.tags),
            grade=_grade_response(view.grade) if view.grade else None,
            tags=[_tag_response(t) for t in view.tags],
            contacts=[_contact_response(c) for c in view.contacts],
            follow_ups=view.follow_ups,
            quotations=view.quotations,
            orders=view.orders,
            stats=Customer360StatsResponse(
                contact_count=view.stats.contact_count,
                follow_up_count=view.stats.follow_up_count,
                quotation_count=view.stats.quotation_count,
                order_count=view.stats.order_count,
                last_follow_at=view.stats.last_follow_at,
                total_order_amount=float(view.stats.total_order_amount) if view.stats.total_order_amount else None,
            ),
        )
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
