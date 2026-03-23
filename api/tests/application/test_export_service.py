import uuid
from unittest.mock import AsyncMock

import pytest

from app.application.customer.export_service import CustomerExportService
from app.domain.customer.enums import DataJobStatus


@pytest.fixture
def deps():
    return {
        "job_repo": AsyncMock(),
        "customer_repo": AsyncMock(),
        "contact_repo": AsyncMock(),
        "grade_repo": AsyncMock(),
        "task_queue": AsyncMock(),
    }


@pytest.fixture
def deps_with_create(deps):
    deps["job_repo"].create.side_effect = lambda j: j
    return deps


class TestCustomerExportService:
    async def test_start_export_creates_job(self, deps_with_create):
        svc = CustomerExportService(**deps_with_create)
        job = await svc.start_export(
            tenant_id=uuid.uuid7(),
            user_id=uuid.uuid7(),
            filter_config={"source": "alibaba"},
        )
        assert job.status == DataJobStatus.PENDING
        assert job.job_type == "export"
        deps_with_create["job_repo"].create.assert_called_once()
        deps_with_create["task_queue"].enqueue.assert_called_once()

    async def test_start_export_no_filter(self, deps_with_create):
        svc = CustomerExportService(**deps_with_create)
        job = await svc.start_export(tenant_id=uuid.uuid7(), user_id=uuid.uuid7())
        assert job.filter_config is None
