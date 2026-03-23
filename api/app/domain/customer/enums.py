from enum import StrEnum


class FollowUpStage(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUOTED = "quoted"
    SAMPLE_SENT = "sample_sent"
    NEGOTIATING = "negotiating"
    ORDERED = "ordered"
    LOST = "lost"


class DataJobStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobType(StrEnum):
    IMPORT = "import"
    EXPORT = "export"


class MatchType(StrEnum):
    NAME_EXACT = "name_exact"
    EMAIL_DOMAIN = "email_domain"
    EMAIL_EXACT = "email_exact"
