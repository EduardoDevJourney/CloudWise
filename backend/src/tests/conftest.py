import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

# has to run before the app is imported: throwaway SQLite db, dev mode, ignores the real .env
_db_dir = tempfile.mkdtemp(prefix="cloudwise-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ["APP_ENV"] = "development"

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session

from infra.database.seed import seed_costs
from infra.database.session import engine
from infra.database.sqlmodel.models import UserModel
from infra.http.main import create_app


BACKEND_DIR = Path(__file__).resolve().parents[2]


def migrate(revision: str = "head", direction: str = "upgrade") -> None:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    getattr(command, direction)(config, revision)


@pytest.fixture(scope="session", autouse=True)
def migrated_db():
    migrate()
    with Session(engine) as session:
        seed_costs(session)


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def login():
    """Returns dev headers for the user, storing their role in the database."""

    def _login(user_id: str, role: str, active: bool = True) -> dict[str, str]:
        with Session(engine) as session:
            session.merge(
                UserModel(
                    id=user_id,
                    email=f"{user_id}@test.local",
                    role=role,
                    active=active,
                    created_at=datetime.now(UTC),
                )
            )
            session.commit()
        return {"X-Dev-User-Id": user_id, "X-Dev-User-Email": f"{user_id}@test.local"}

    return _login
