import json
from datetime import date, datetime
from typing import Any
from uuid import UUID

from sqlmodel import Field, SQLModel, Column, JSON


class TemplateModel(SQLModel, table=True):
    __tablename__ = "templates"

    id: str = Field(primary_key=True)
    name: str
    params_schema: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    azure_sku: str
    slug: str = Field(index=True)


class ProvisionRequestModel(SQLModel, table=True):
    __tablename__ = "provision_requests"

    id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    template_id: str = Field(index=True)
    status: str = Field(index=True)
    request_data: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    error_message: str | None = None
    created_at: datetime
    execution_time: datetime | None = None


class CostRecordModel(SQLModel, table=True):
    __tablename__ = "cost_records"

    id: str = Field(primary_key=True)
    subscription_id: str = Field(index=True)
    cost: float
    record_date: date = Field(index=True)
    resource_type: str
    tags: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class CostDimModel(SQLModel, table=True):
    __tablename__ = "cost_dims"

    id: str = Field(primary_key=True)
    record_date: date = Field(index=True)
    category: str
    service_name: str
