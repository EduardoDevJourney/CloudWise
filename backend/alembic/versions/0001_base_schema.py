"""base schema

Revision ID: 0001
Revises:
Create Date: 2026-11-22
"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=128), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "templates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("params_schema", sa.Text(), nullable=False),
        sa.Column("azure_sku", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_index("ix_templates_slug", "templates", ["slug"])

    op.create_table(
        "provision_requests",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("template_id", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("request_data", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("outputs", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_provision_requests_user_id", "provision_requests", ["user_id"])
    op.create_index("ix_provision_requests_template_id", "provision_requests", ["template_id"])
    op.create_index("ix_provision_requests_status", "provision_requests", ["status"])

    op.create_table(
        "dim_data",
        sa.Column("data_id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("data", sa.Date(), nullable=False, unique=True),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("trimestre", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("dia_semana", sa.Integer(), nullable=False),
        sa.Column("ano_mes", sa.String(length=7), nullable=False),
    )
    op.create_index("ix_dim_data_ano_mes", "dim_data", ["ano_mes"])

    op.create_table(
        "dim_servico",
        sa.Column("servico_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(length=255), nullable=False, unique=True),
        sa.Column("categoria", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "dim_assinatura",
        sa.Column("assinatura_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("codigo", sa.String(length=128), nullable=False, unique=True),
        sa.Column("nome", sa.String(length=255), nullable=False),
    )

    op.create_table(
        "fact_custo",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("data_id", sa.Integer(), sa.ForeignKey("dim_data.data_id"), nullable=False),
        sa.Column(
            "servico_id", sa.Integer(), sa.ForeignKey("dim_servico.servico_id"), nullable=False
        ),
        sa.Column(
            "assinatura_id",
            sa.Integer(),
            sa.ForeignKey("dim_assinatura.assinatura_id"),
            nullable=False,
        ),
        sa.Column("custo", sa.Float(), nullable=False),
        sa.Column("tags", sa.Text(), nullable=False),
    )
    op.create_index("ix_fact_custo_data_id", "fact_custo", ["data_id"])
    op.create_index("ix_fact_custo_servico_id", "fact_custo", ["servico_id"])
    op.create_index("ix_fact_custo_assinatura_id", "fact_custo", ["assinatura_id"])


def downgrade() -> None:
    op.drop_table("fact_custo")
    op.drop_table("dim_assinatura")
    op.drop_table("dim_servico")
    op.drop_table("dim_data")
    op.drop_table("provision_requests")
    op.drop_table("templates")
    op.drop_table("users")
