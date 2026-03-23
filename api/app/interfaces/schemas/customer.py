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


# Duplicate checking
class CheckDuplicateRequest(BaseModel):
    name: str
    email: str | None = None


class DuplicateMatchResponse(BaseModel):
    customer_id: uuid.UUID
    customer_name: str
    match_type: str
    matched_value: str


class CheckDuplicateResponse(BaseModel):
    duplicates: list[DuplicateMatchResponse]


# 360° view
class Customer360StatsResponse(BaseModel):
    contact_count: int
    follow_up_count: int
    quotation_count: int
    order_count: int
    last_follow_at: datetime | None
    total_order_amount: float | None


class Customer360Response(BaseModel):
    customer: CustomerResponse
    grade: CustomerGradeResponse | None
    tags: list[TagResponse]
    contacts: list[ContactResponse]
    follow_ups: list[dict[str, Any]] = Field(default_factory=list)
    quotations: list[dict[str, Any]] = Field(default_factory=list)
    orders: list[dict[str, Any]] = Field(default_factory=list)
    stats: Customer360StatsResponse


# Saved views
class CreateSavedViewRequest(BaseModel):
    name: str
    entity_type: str = "customer"
    filter_config: dict[str, Any]
    is_default: bool = False
    position: int = 0


class UpdateSavedViewRequest(BaseModel):
    name: str | None = None
    filter_config: dict[str, Any] | None = None
    is_default: bool | None = None
    position: int | None = None


class SavedViewResponse(BaseModel):
    id: uuid.UUID
    name: str
    entity_type: str
    filter_config: dict[str, Any]
    is_default: bool
    position: int
    created_at: datetime
    updated_at: datetime


# Import/Export
class ImportCustomerResponse(BaseModel):
    job_id: uuid.UUID


class ExportCustomerRequest(BaseModel):
    filter_config: dict[str, Any] | None = None


class ExportCustomerResponse(BaseModel):
    job_id: uuid.UUID


# Data Jobs
class DataJobResponse(BaseModel):
    id: uuid.UUID
    entity_type: str
    job_type: str
    file_name: str
    status: str
    total_rows: int
    processed_rows: int
    success_count: int
    error_count: int
    result_file_url: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
