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
from infra.database.sqlmodel.models import UserModel
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


@pytest.fixture
def login():
    """Devolve headers de dev para o usuário, gravando o papel dele no banco."""

    def _login(user_id: str, role: str, active: bool = True) -> dict[str, str]:
        from datetime import datetime

        with Session(engine) as session:
            session.merge(
                UserModel(
                    id=user_id,
                    email=f"{user_id}@test.local",
                    role=role,
                    active=active,
                    created_at=datetime.utcnow(),
                )
            )
            session.commit()
        return {"X-Dev-User-Id": user_id, "X-Dev-User-Email": f"{user_id}@test.local"}

    return _login
