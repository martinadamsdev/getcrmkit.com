import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.customer.entities import CustomerGrade
from app.domain.customer.exceptions import CustomerGradeNotFoundError, GradeInUseError
from app.domain.customer.services import CustomerGradeService
from app.interfaces.api.deps import get_current_user, get_db, get_grade_service
from app.interfaces.schemas.customer import (
    CreateCustomerGradeRequest,
    CustomerGradeResponse,
    UpdateCustomerGradeRequest,
)

router = APIRouter(prefix="/api/v1/customer-grades", tags=["customer-grades"])


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


@router.get("", response_model=list[CustomerGradeResponse])
async def list_grades(
    current_user: User = Depends(get_current_user),
    service: CustomerGradeService = Depends(get_grade_service),
) -> list[CustomerGradeResponse]:
    grades = await service.get_all(tenant_id=current_user.tenant_id)
    return [_grade_response(g) for g in grades]


@router.post("", response_model=CustomerGradeResponse, status_code=201)
async def create_grade(
    body: CreateCustomerGradeRequest,
    current_user: User = Depends(get_current_user),
    service: CustomerGradeService = Depends(get_grade_service),
    session: AsyncSession = Depends(get_db),
) -> CustomerGradeResponse:
    grade = await service.create_grade(
        tenant_id=current_user.tenant_id,
        created_by=current_user.id,
        name=body.name,
        label=body.label,
        color=body.color,
        position=body.position,
    )
    await session.commit()
    return _grade_response(grade)


@router.put("/{grade_id}", response_model=CustomerGradeResponse)
async def update_grade(
    grade_id: uuid.UUID,
    body: UpdateCustomerGradeRequest,
    current_user: User = Depends(get_current_user),
    service: CustomerGradeService = Depends(get_grade_service),
    session: AsyncSession = Depends(get_db),
) -> CustomerGradeResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        grade = await service.update_grade(
            tenant_id=current_user.tenant_id,
            grade_id=grade_id,
            **updates,
        )
        await session.commit()
        return _grade_response(grade)
    except CustomerGradeNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{grade_id}", status_code=204)
async def delete_grade(
    grade_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: CustomerGradeService = Depends(get_grade_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_grade(tenant_id=current_user.tenant_id, grade_id=grade_id)
        await session.commit()
    except CustomerGradeNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except GradeInUseError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e
