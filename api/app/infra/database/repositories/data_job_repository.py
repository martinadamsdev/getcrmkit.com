from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import DataJob
from app.domain.customer.enums import DataJobStatus
from app.domain.customer.repository import AbstractDataJobRepository
from app.infra.database.models.data_job import DataJobModel


class DataJobRepository(AbstractDataJobRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, job: DataJob) -> DataJob:
        model = self._to_model(job)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, job_id: uuid.UUID) -> DataJob | None:
        stmt = select(DataJobModel).where(
            DataJobModel.id == job_id,
            DataJobModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_job_id(self, job_id: uuid.UUID) -> DataJob | None:
        """Fetch a job by id only — for use in worker context where tenant_id is unknown."""
        stmt = select(DataJobModel).where(DataJobModel.id == job_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, job: DataJob) -> DataJob:
        stmt = select(DataJobModel).where(
            DataJobModel.id == job.id,
            DataJobModel.tenant_id == job.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.status = job.status.value
        model.total_rows = job.total_rows
        model.processed_rows = job.processed_rows
        model.success_count = job.success_count
        model.error_count = job.error_count
        model.result_file_url = job.result_file_url
        model.error_details = job.error_details
        model.started_at = job.started_at
        model.completed_at = job.completed_at
        model.updated_by = job.updated_by
        model.updated_at = job.updated_at
        await self._session.flush()
        return self._to_entity(model)

    @staticmethod
    def _to_model(job: DataJob) -> DataJobModel:
        return DataJobModel(
            id=job.id,
            tenant_id=job.tenant_id,
            user_id=job.user_id,
            entity_type=job.entity_type,
            job_type=job.job_type,
            file_name=job.file_name,
            file_path=job.file_path,
            status=job.status.value,
            total_rows=job.total_rows,
            processed_rows=job.processed_rows,
            success_count=job.success_count,
            error_count=job.error_count,
            result_file_url=job.result_file_url,
            error_details=job.error_details,
            filter_config=job.filter_config,
            started_at=job.started_at,
            completed_at=job.completed_at,
            created_by=job.created_by,
            updated_by=job.updated_by,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )

    @staticmethod
    def _to_entity(model: DataJobModel) -> DataJob:
        return DataJob(
            id=model.id,
            tenant_id=model.tenant_id,
            user_id=model.user_id,
            entity_type=model.entity_type,
            job_type=model.job_type,
            file_name=model.file_name,
            file_path=model.file_path,
            status=DataJobStatus(model.status),
            total_rows=model.total_rows,
            processed_rows=model.processed_rows,
            success_count=model.success_count,
            error_count=model.error_count,
            result_file_url=model.result_file_url,
            error_details=model.error_details if model.error_details is not None else [],
            filter_config=model.filter_config,
            started_at=model.started_at,
            completed_at=model.completed_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
