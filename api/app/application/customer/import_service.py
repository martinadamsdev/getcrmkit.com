from __future__ import annotations

import uuid

from app.application.shared.task_queue import AbstractTaskQueue
from app.domain.customer.entities import DataJob
from app.domain.customer.enums import DataJobStatus
from app.domain.customer.repository import (
    AbstractContactRepository,
    AbstractCustomerRepository,
    AbstractDataJobRepository,
)
from app.domain.customer.services import DuplicateChecker


class CustomerImportService:
    def __init__(
        self,
        job_repo: AbstractDataJobRepository,
        customer_repo: AbstractCustomerRepository,
        contact_repo: AbstractContactRepository,
        duplicate_checker: DuplicateChecker,
        task_queue: AbstractTaskQueue,
    ) -> None:
        self._job_repo = job_repo
        self._customer_repo = customer_repo
        self._contact_repo = contact_repo
        self._duplicate_checker = duplicate_checker
        self._task_queue = task_queue

    async def start_import(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        file_name: str,
        file_path: str,
    ) -> DataJob:
        job = DataJob(
            tenant_id=tenant_id,
            user_id=user_id,
            job_type="import",
            file_name=file_name,
            file_path=file_path,
            status=DataJobStatus.PENDING,
            created_by=user_id,
        )
        job = await self._job_repo.create(job)
        await self._task_queue.enqueue("process_customer_import", job_id=str(job.id))
        return job
