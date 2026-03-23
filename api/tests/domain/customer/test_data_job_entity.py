import uuid

from app.domain.customer.entities import DataJob
from app.domain.customer.enums import DataJobStatus


class TestDataJob:
    def test_create_with_defaults(self):
        job = DataJob(user_id=uuid.uuid7())
        assert job.entity_type == "customer"
        assert job.job_type == ""
        assert job.file_name == ""
        assert job.status == DataJobStatus.PENDING
        assert job.total_rows == 0
        assert job.processed_rows == 0
        assert job.success_count == 0
        assert job.error_count == 0
        assert job.result_file_url is None
        assert job.error_details == []
        assert job.filter_config is None
        assert job.started_at is None
        assert job.completed_at is None

    def test_create_import_job(self):
        uid = uuid.uuid7()
        job = DataJob(user_id=uid, job_type="import", file_name="customers.xlsx", file_path="/tmp/customers.xlsx")
        assert job.user_id == uid
        assert job.job_type == "import"
        assert job.file_name == "customers.xlsx"

    def test_create_export_job(self):
        uid = uuid.uuid7()
        config = {"source": "alibaba"}
        job = DataJob(user_id=uid, job_type="export", file_name="export.xlsx", filter_config=config)
        assert job.job_type == "export"
        assert job.filter_config == config
