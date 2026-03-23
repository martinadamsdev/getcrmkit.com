from __future__ import annotations

import uuid
from typing import Any

from app.application.shared.task_queue import AbstractTaskQueue
from app.domain.customer.entities import DataJob
from app.domain.customer.enums import DataJobStatus
from app.domain.customer.repository import (
    AbstractContactRepository,
    AbstractCustomerGradeRepository,
    AbstractCustomerRepository,
    AbstractDataJobRepository,
)


class CustomerExportService:
    def __init__(
        self,
        job_repo: AbstractDataJobRepository,
        customer_repo: AbstractCustomerRepository,
        contact_repo: AbstractContactRepository,
        grade_repo: AbstractCustomerGradeRepository,
        task_queue: AbstractTaskQueue,
    ) -> None:
        self._job_repo = job_repo
        self._customer_repo = customer_repo
        self._contact_repo = contact_repo
        self._grade_repo = grade_repo
        self._task_queue = task_queue

    async def start_export(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        filter_config: dict[str, Any] | None = None,
    ) -> DataJob:
        job = DataJob(
            tenant_id=tenant_id,
            user_id=user_id,
            job_type="export",
            file_name="customers_export.xlsx",
            filter_config=filter_config,
            status=DataJobStatus.PENDING,
            created_by=user_id,
        )
        job = await self._job_repo.create(job)
        await self._task_queue.enqueue("process_customer_export", job_id=str(job.id))
        return job
