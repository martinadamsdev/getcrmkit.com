import uuid
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class CreateCustomerGradeRequest(BaseModel):
    name: str
    label: str | None = None
    color: str = "#3B82F6"
    position: int = 0


class UpdateCustomerGradeRequest(BaseModel):
    name: str | None = None
    label: str | None = None
    color: str | None = None
    position: int | None = None


class CustomerGradeResponse(BaseModel):
    id: uuid.UUID
    name: str
    label: str | None
    color: str
    position: int
    created_at: datetime
    updated_at: datetime


class CreateTagRequest(BaseModel):
    name: str
    color: str = "#3B82F6"
    group_name: str | None = None
    position: int = 0


class UpdateTagRequest(BaseModel):
    name: str | None = None
    color: str | None = None
    group_name: str | None = None
    position: int | None = None


class TagResponse(BaseModel):
    id: uuid.UUID
    name: str
    color: str
    group_name: str | None
    position: int
    created_at: datetime
    updated_at: datetime


class TagCustomerRequest(BaseModel):
    tag_id: uuid.UUID


class CreateContactRequest(BaseModel):
    name: str
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    skype: str | None = None
    linkedin: str | None = None
    wechat: str | None = None
    notes: str | None = None
    custom_fields: dict[str, Any] = Field(default_factory=dict)


class UpdateContactRequest(BaseModel):
    name: str | None = None
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    skype: str | None = None
    linkedin: str | None = None
    wechat: str | None = None
    notes: str | None = None
    custom_fields: dict[str, Any] | None = None


class ContactResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    name: str
    title: str | None
    email: str | None
    phone: str | None
    whatsapp: str | None
    skype: str | None
    linkedin: str | None
    wechat: str | None
    is_primary: bool
    notes: str | None
    custom_fields: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class CreateCustomerRequest(BaseModel):
    name: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    address: str | None = None
    industry: str | None = None
    company_size: str | None = None
    website: str | None = None
    source: str | None = None
    grade_id: uuid.UUID | None = None
    follow_status: str = "new"
    main_products: str | None = None
    annual_volume: str | None = None
    current_supplier: str | None = None
    decision_process: str | None = None
    custom_fields: dict[str, Any] = Field(default_factory=dict)


class UpdateCustomerRequest(BaseModel):
    name: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    address: str | None = None
    industry: str | None = None
    company_size: str | None = None
    website: str | None = None
    source: str | None = None
    grade_id: uuid.UUID | None = None
    follow_status: str | None = None
    main_products: str | None = None
    annual_volume: str | None = None
    current_supplier: str | None = None
    decision_process: str | None = None
    custom_fields: dict[str, Any] | None = None


class CustomerResponse(BaseModel):
    id: uuid.UUID
    name: str
    country: str | None
    region: str | None
    city: str | None
    address: str | None
    industry: str | None
    company_size: str | None
    website: str | None
    source: str | None
    grade_id: uuid.UUID | None
    grade: CustomerGradeResponse | None = None
    follow_status: str
    main_products: str | None
    annual_volume: str | None
    current_supplier: str | None
    decision_process: str | None
    owner_id: uuid.UUID | None
    claimed_at: datetime | None
    last_follow_at: datetime | None
    custom_fields: dict[str, Any]
    tags: list[TagResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
