from app.domain.customer.enums import DataJobStatus, JobType, MatchType


class TestDataJobStatus:
    def test_values(self):
        assert DataJobStatus.PENDING == "pending"
        assert DataJobStatus.PROCESSING == "processing"
        assert DataJobStatus.COMPLETED == "completed"
        assert DataJobStatus.FAILED == "failed"

    def test_count(self):
        assert len(DataJobStatus) == 4


class TestJobType:
    def test_values(self):
        assert JobType.IMPORT == "import"
        assert JobType.EXPORT == "export"


class TestMatchType:
    def test_values(self):
        assert MatchType.NAME_EXACT == "name_exact"
        assert MatchType.EMAIL_DOMAIN == "email_domain"
        assert MatchType.EMAIL_EXACT == "email_exact"
