import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import DataJob
from app.domain.customer.enums import DataJobStatus
from app.infra.database.repositories.data_job_repository import DataJobRepository


def make_job(
    tenant_id: uuid.UUID,
    user_id: uuid.UUID | None = None,
    file_name: str = "customers.csv",
) -> DataJob:
    now = datetime.now(UTC)
    return DataJob(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        user_id=user_id or uuid.uuid7(),
        entity_type="customer",
        job_type="import",
        file_name=file_name,
        file_path="/uploads/customers.csv",
        status=DataJobStatus.PENDING,
        total_rows=0,
        processed_rows=0,
        success_count=0,
        error_count=0,
        error_details=[],
        created_at=now,
        updated_at=now,
    )


class TestDataJobRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = DataJobRepository(db_session)

        job = make_job(tenant_id, file_name="import.csv")
        created = await repo.create(job)

        fetched = await repo.get_by_id(tenant_id, created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.file_name == "import.csv"
        assert fetched.status == DataJobStatus.PENDING
        assert fetched.job_type == "import"

    async def test_get_by_id_wrong_tenant_returns_none(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        other_tenant = uuid.uuid7()
        repo = DataJobRepository(db_session)

        job = await repo.create(make_job(tenant_id))
        result = await repo.get_by_id(other_tenant, job.id)
        assert result is None

    async def test_update_status(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = DataJobRepository(db_session)

        job = await repo.create(make_job(tenant_id))
        assert job.status == DataJobStatus.PENDING

        now = datetime.now(UTC)
        job.status = DataJobStatus.PROCESSING
        job.started_at = now
        job.total_rows = 100
        job.updated_at = now
        updated = await repo.update(job)

        assert updated.status == DataJobStatus.PROCESSING
        assert updated.started_at == now
        assert updated.total_rows == 100

    async def test_update_to_completed(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = DataJobRepository(db_session)

        job = await repo.create(make_job(tenant_id))
        now = datetime.now(UTC)
        job.status = DataJobStatus.COMPLETED
        job.total_rows = 50
        job.processed_rows = 50
        job.success_count = 48
        job.error_count = 2
        job.error_details = [{"row": 3, "error": "invalid email"}]
        job.completed_at = now
        job.updated_at = now
        updated = await repo.update(job)

        assert updated.status == DataJobStatus.COMPLETED
        assert updated.success_count == 48
        assert updated.error_count == 2
        assert len(updated.error_details) == 1
        assert updated.completed_at == now

    async def test_tenant_isolation(self, db_session: AsyncSession) -> None:
        tenant_a = uuid.uuid7()
        tenant_b = uuid.uuid7()
        repo = DataJobRepository(db_session)

        job_a = await repo.create(make_job(tenant_a, file_name="a.csv"))
        job_b = await repo.create(make_job(tenant_b, file_name="b.csv"))

        # Each tenant can only see their own jobs
        assert await repo.get_by_id(tenant_a, job_a.id) is not None
        assert await repo.get_by_id(tenant_a, job_b.id) is None
        assert await repo.get_by_id(tenant_b, job_b.id) is not None
        assert await repo.get_by_id(tenant_b, job_a.id) is None
