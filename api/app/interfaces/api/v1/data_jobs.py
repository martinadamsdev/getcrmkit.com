import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.domain.auth.entities import User
from app.infra.database.repositories.data_job_repository import DataJobRepository
from app.interfaces.api.deps import get_current_user, get_data_job_repo
from app.interfaces.schemas.customer import DataJobResponse

router = APIRouter(prefix="/api/v1/data-jobs", tags=["data-jobs"])


@router.get("/{job_id}", response_model=DataJobResponse)
async def get_data_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    repo: DataJobRepository = Depends(get_data_job_repo),
) -> DataJobResponse:
    job = await repo.get_by_id(current_user.tenant_id, job_id)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "DATA_JOB_NOT_FOUND", "message": f"Data job not found: {job_id}"},
        )
    return DataJobResponse(
        id=job.id,
        entity_type=job.entity_type,
        job_type=job.job_type,
        file_name=job.file_name,
        status=job.status.value,
        total_rows=job.total_rows,
        processed_rows=job.processed_rows,
        success_count=job.success_count,
        error_count=job.error_count,
        result_file_url=job.result_file_url,
        started_at=job.started_at,
        completed_at=job.completed_at,
        created_at=job.created_at,
    )
