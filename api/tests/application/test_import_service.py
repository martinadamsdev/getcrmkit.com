import uuid
from unittest.mock import AsyncMock

import pytest

from app.application.customer.import_service import CustomerImportService
from app.domain.customer.enums import DataJobStatus


@pytest.fixture
def deps():
    return {
        "job_repo": AsyncMock(),
        "customer_repo": AsyncMock(),
        "contact_repo": AsyncMock(),
        "duplicate_checker": AsyncMock(),
        "task_queue": AsyncMock(),
    }


@pytest.fixture
def deps_with_create(deps):
    deps["job_repo"].create.side_effect = lambda j: j
    return deps


class TestCustomerImportService:
    async def test_start_import_creates_job(self, deps_with_create):
        svc = CustomerImportService(**deps_with_create)
        job = await svc.start_import(
            tenant_id=uuid.uuid7(),
            user_id=uuid.uuid7(),
            file_name="test.xlsx",
            file_path="/tmp/test.xlsx",
        )
        assert job.status == DataJobStatus.PENDING
        assert job.job_type == "import"
        deps_with_create["job_repo"].create.assert_called_once()
        deps_with_create["task_queue"].enqueue.assert_called_once()
