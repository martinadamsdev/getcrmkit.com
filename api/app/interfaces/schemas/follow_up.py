import uuid
from datetime import datetime

from pydantic import BaseModel, Field

# --- FollowUp ---


class CreateFollowUpRequest(BaseModel):
    customer_id: uuid.UUID
    contact_id: uuid.UUID | None = None
    method: str  # FollowUpMethod 值
    stage: str | None = None  # FollowUpStage 值（可选）
    content: str
    customer_response: str | None = None
    next_follow_at: datetime | None = None
    attachment_urls: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class UpdateFollowUpRequest(BaseModel):
    content: str | None = None
    customer_response: str | None = None
    next_follow_at: datetime | None = None
    attachment_urls: list[str] | None = None
    tags: list[str] | None = None


class FollowUpResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    contact_id: uuid.UUID | None
    method: str
    stage: str | None
    content: str
    customer_response: str | None
    next_follow_at: datetime | None
    attachment_urls: list[str]
    tags: list[str]
    created_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


# --- ScriptTemplate ---


class CreateScriptTemplateRequest(BaseModel):
    scene: str
    title: str
    content: str
    language: str = "zh-CN"
    position: int = 0


class UpdateScriptTemplateRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    language: str | None = None
    position: int | None = None


class ScriptTemplateResponse(BaseModel):
    id: uuid.UUID
    scene: str
    title: str
    content: str
    language: str
    position: int
    is_system: bool
    created_at: datetime
    updated_at: datetime


# --- Report ---


class ReportItemResponse(BaseModel):
    date: str
    total_count: int
    method_breakdown: dict[str, int]


class FollowUpReportResponse(BaseModel):
    period: str
    start_date: str
    end_date: str
    total: int
    items: list[ReportItemResponse]
