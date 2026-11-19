import os
import tempfile

# Isola os testes: banco SQLite temporário e modo desenvolvimento, independente do .env.
_db_dir = tempfile.mkdtemp(prefix="cloudwise-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ["APP_ENV"] = "development"

import pytest
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session

from infra.database.seed import seed_database
from infra.database.session import create_db_and_tables, engine
from infra.http.main import create_app


@pytest.fixture
def app():
    create_db_and_tables()
    with Session(engine) as session:
        seed_database(session)
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
