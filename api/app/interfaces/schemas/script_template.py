import uuid
from datetime import datetime

from pydantic import BaseModel


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
