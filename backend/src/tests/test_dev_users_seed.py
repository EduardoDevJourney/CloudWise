from sqlmodel import Session, SQLModel, create_engine, select

from domain.auth.roles import ROLE_ADMIN, ROLE_PROVISIONER, ROLE_VIEWER
from infra.database.seed import seed_dev_users
from infra.database.sqlmodel.models import UserModel


def _session() -> Session:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_seeds_one_user_per_role():
    with _session() as session:
        seed_dev_users(session)
        roles = {u.id: u.role for u in session.exec(select(UserModel)).all()}

    assert roles == {
        "dev-viewer": ROLE_VIEWER,
        "dev-provisioner": ROLE_PROVISIONER,
        "dev-user": ROLE_ADMIN,
    }


def test_does_not_overwrite_existing_users():
    with _session() as session:
        seed_dev_users(session)
        viewer = session.get(UserModel, "dev-viewer")
        viewer.role = ROLE_PROVISIONER
        session.add(viewer)
        session.commit()

        seed_dev_users(session)

        assert session.get(UserModel, "dev-viewer").role == ROLE_PROVISIONER
        assert len(session.exec(select(UserModel)).all()) == 3
