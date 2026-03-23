from enum import StrEnum


class FollowUpStage(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUOTED = "quoted"
    SAMPLE_SENT = "sample_sent"
    NEGOTIATING = "negotiating"
    ORDERED = "ordered"
    LOST = "lost"
