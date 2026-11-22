from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect, text
from sqlmodel import SQLModel

import infra.database.sqlmodel.models  # noqa: F401

ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"
TABLES = {
    "users",
    "templates",
    "provision_requests",
    "dim_data",
    "dim_servico",
    "dim_assinatura",
    "fact_custo",
}


@pytest.fixture
def db(tmp_path):
    return create_engine(f"sqlite:///{tmp_path}/migrations.db")


def run(engine, direction: str, revision: str) -> None:
    config = Config(str(ALEMBIC_INI))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        getattr(command, direction)(config, revision)


def test_upgrade_creates_the_schema_and_the_template_catalog(db):
    run(db, "upgrade", "head")

    assert TABLES <= set(inspect(db).get_table_names())
    with db.connect() as conn:
        slugs = {row[0] for row in conn.execute(text("SELECT slug FROM templates"))}
    assert slugs == {"rg-storage", "rg-keyvault"}


def test_downgrade_to_base_removes_every_table_and_upgrade_works_again(db):
    run(db, "upgrade", "head")
    run(db, "downgrade", "base")

    assert set(inspect(db).get_table_names()) <= {"alembic_version"}

    run(db, "upgrade", "head")
    assert TABLES <= set(inspect(db).get_table_names())


def test_models_and_migrations_have_no_drift(db):
    run(db, "upgrade", "head")

    with db.connect() as conn:
        diff = compare_metadata(
            MigrationContext.configure(conn, opts={"compare_type": True}), SQLModel.metadata
        )

    assert diff == []
