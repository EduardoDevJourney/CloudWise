from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlmodel import Field, SQLModel


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
    outputs: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    started_at: datetime | None = Field(default=None, sa_column=Column(DateTime, nullable=True))
    finished_at: datetime | None = Field(default=None, sa_column=Column(DateTime, nullable=True))


class DimDataModel(SQLModel, table=True):
    __tablename__ = "dim_data"

    data_id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=False))
    data: date = Field(sa_column=Column(Date, nullable=False, unique=True))
    ano: int = Field(sa_column=Column(Integer, nullable=False))
    trimestre: int = Field(sa_column=Column(Integer, nullable=False))
    mes: int = Field(sa_column=Column(Integer, nullable=False))
    dia: int = Field(sa_column=Column(Integer, nullable=False))
    dia_semana: int = Field(sa_column=Column(Integer, nullable=False))
    ano_mes: str = Field(sa_column=Column(String(7), nullable=False, index=True))


class DimServicoModel(SQLModel, table=True):
    __tablename__ = "dim_servico"

    servico_id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    nome: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    categoria: str = Field(sa_column=Column(String(100), nullable=False))


class DimAssinaturaModel(SQLModel, table=True):
    __tablename__ = "dim_assinatura"

    assinatura_id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    codigo: str = Field(sa_column=Column(String(128), nullable=False, unique=True))
    nome: str = Field(sa_column=Column(String(255), nullable=False))


class FatoCustoModel(SQLModel, table=True):
    __tablename__ = "fact_custo"

    id: str = Field(sa_column=Column(String(36), primary_key=True))
    data_id: int = Field(sa_column=Column(Integer, ForeignKey("dim_data.data_id"), nullable=False, index=True))
    servico_id: int = Field(
        sa_column=Column(Integer, ForeignKey("dim_servico.servico_id"), nullable=False, index=True)
    )
    assinatura_id: int = Field(
        sa_column=Column(Integer, ForeignKey("dim_assinatura.assinatura_id"), nullable=False, index=True)
    )
    custo: float = Field(sa_column=Column(Float, nullable=False))
    tags: str = Field(sa_column=Column(Text, nullable=False))


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(sa_column=Column(String(128), primary_key=True))
    email: str = Field(sa_column=Column(String(255), nullable=False, index=True))
    role: str = Field(sa_column=Column(String(64), nullable=False))
    active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False))
