from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ProvisionRequestCreateDTO(BaseModel):
    template_id: str
    resource_name: str
    environment: str
    location: str = "eastus"


class ProvisionRequestReadDTO(BaseModel):
    id: str
    user_id: str
    template_id: str
    status: str
    request_data: dict[str, Any]
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    execution_seconds: float | None
    outputs: dict[str, Any]


class TemplateReadDTO(BaseModel):
    id: str
    slug: str
    name: str
    description: str
    params_schema: dict[str, Any]
    azure_sku: str


class CostRecordReadDTO(BaseModel):
    id: str
    subscription_id: str
    cost: float
    date: str
    resource_type: str
    tags: dict[str, Any]


class CostSeriesDayDTO(BaseModel):
    date: str
    total_cost: float
    by_service: dict[str, float]


class DashboardSummaryDTO(BaseModel):
    total_cost: float
    top_service: str
    subscription_count: int


class CloudWiseDashboardDTO(BaseModel):
    granularity: str
    series: list[CostSeriesDayDTO]
    summary: DashboardSummaryDTO


class HealthDTO(BaseModel):
    status: str = "ok"


class PolicyReadDTO(BaseModel):
    locations: list[str]
    environments: list[str]
    resource_name_pattern: str


class MeDTO(BaseModel):
    id: str
    email: str
    role: str


class UserReadDTO(BaseModel):
    id: str
    email: str
    role: str
    active: bool
    created_at: datetime


class UserUpdateDTO(BaseModel):
    role: str | None = None
    active: bool | None = None
