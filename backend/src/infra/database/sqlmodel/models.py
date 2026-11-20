import json
from datetime import date, datetime
from typing import Any

from sqlalchemy import Boolean, Column, Date, DateTime, Float, String, Text
from sqlmodel import Field, SQLModel


def _json_loads(value: str | dict[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return json.loads(value)


class TemplateModel(SQLModel, table=True):
    __tablename__ = "templates"

    id: str = Field(sa_column=Column(String(36), primary_key=True))
    name: str = Field(sa_column=Column(String(255), nullable=False))
    params_schema: str = Field(sa_column=Column(Text, nullable=False))
    azure_sku: str = Field(sa_column=Column(String(100), nullable=False))
    slug: str = Field(sa_column=Column(String(100), nullable=False, index=True))
    description: str | None = Field(default=None, sa_column=Column(Text, nullable=True))


class ProvisionRequestModel(SQLModel, table=True):
    __tablename__ = "provision_requests"

    id: str = Field(sa_column=Column(String(36), primary_key=True))
    user_id: str = Field(sa_column=Column(String(128), nullable=False, index=True))
    template_id: str = Field(sa_column=Column(String(100), nullable=False, index=True))
    status: str = Field(sa_column=Column(String(32), nullable=False, index=True))
    request_data: str = Field(sa_column=Column(Text, nullable=False))
    error_message: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False))
    started_at: datetime | None = Field(default=None, sa_column=Column(DateTime, nullable=True))
    finished_at: datetime | None = Field(default=None, sa_column=Column(DateTime, nullable=True))


class CostRecordModel(SQLModel, table=True):
    __tablename__ = "cost_records"

    id: str = Field(sa_column=Column(String(36), primary_key=True))
    subscription_id: str = Field(sa_column=Column(String(128), nullable=False, index=True))
    cost: float = Field(sa_column=Column(Float, nullable=False))
    record_date: date = Field(sa_column=Column(Date, nullable=False, index=True))
    resource_type: str = Field(sa_column=Column(String(255), nullable=False))
    tags: str = Field(sa_column=Column(Text, nullable=False))


class CostDimModel(SQLModel, table=True):
    __tablename__ = "cost_dims"

    id: str = Field(sa_column=Column(String(36), primary_key=True))
    record_date: date = Field(sa_column=Column(Date, nullable=False, index=True))
    category: str = Field(sa_column=Column(String(100), nullable=False))
    service_name: str = Field(sa_column=Column(String(255), nullable=False))


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(sa_column=Column(String(128), primary_key=True))
    email: str = Field(sa_column=Column(String(255), nullable=False, index=True))
    role: str = Field(sa_column=Column(String(64), nullable=False))
    active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False))
