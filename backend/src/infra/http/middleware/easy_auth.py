import base64
import json
from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

from domain.auth.application.use_cases.manage_users import ResolveUserUseCase
from infra.config import get_settings
from infra.database.repositories.sql_repositories import SQLUsersRepository
from infra.database.session import get_session


@dataclass(frozen=True, slots=True)
class AuthUser:
    user_id: str
    email: str
    roles: list[str]


def _parse_principal_header(request: Request) -> AuthUser | None:
    principal_b64 = request.headers.get("X-MS-CLIENT-PRINCIPAL")
    if not principal_b64:
        return None
    try:
        payload = json.loads(base64.b64decode(principal_b64))
        claims = {c["typ"]: c["val"] for c in payload.get("claims", [])}
        return AuthUser(
            user_id=claims.get("oid", claims.get("sub", "unknown")),
            email=claims.get("preferred_username", claims.get("email", "")),
            roles=[],
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def _parse_dev_headers(request: Request) -> AuthUser | None:
    if get_settings().app_env != "development":
        return None
    user_id = request.headers.get("X-Dev-User-Id")
    if not user_id:
        return None
    email = request.headers.get("X-Dev-User-Email", f"{user_id}@dev.local")
    return AuthUser(user_id=user_id, email=email, roles=[])


async def get_current_user(
    request: Request, session: Session = Depends(get_session)
) -> AuthUser:
    # App Service Easy Auth validates the token; roles come from our `users` table,
    # whatever roles the token carries are ignored.
    identity = _parse_principal_header(request) or _parse_dev_headers(request)
    if identity is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    resolver = ResolveUserUseCase(
        SQLUsersRepository(session), get_settings().admin_emails.split(",")
    )
    user = await resolver.execute(identity.user_id, identity.email)
    if not user.active:
        raise HTTPException(status_code=403, detail="User blocked")
    return AuthUser(user_id=user.id, email=user.email, roles=[user.role])


def require_role(*allowed: str) -> Callable[[AuthUser], AuthUser]:
    def dependency(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if not any(role in user.roles for role in allowed):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user

    return dependency
