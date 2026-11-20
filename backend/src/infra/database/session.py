from collections.abc import AsyncGenerator, Generator

from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine

from infra.config import get_settings

settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, echo=settings.app_env == "development", connect_args=connect_args)


def _add_missing_columns() -> None:
    """Migração mínima (sem Alembic): acrescenta colunas novas em tabelas já existentes."""
    inspector = inspect(engine)
    with engine.begin() as conn:
        for table in SQLModel.metadata.sorted_tables:
            if not inspector.has_table(table.name):
                continue
            existing = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name not in existing and column.nullable:
                    col_type = column.type.compile(dialect=engine.dialect)
                    conn.execute(text(f"ALTER TABLE {table.name} ADD {column.name} {col_type} NULL"))


def create_db_and_tables() -> None:
    import infra.database.sqlmodel.models  # noqa: F401  (registra as tabelas no metadata)

    SQLModel.metadata.create_all(engine)
    _add_missing_columns()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
