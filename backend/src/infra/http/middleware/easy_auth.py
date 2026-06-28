import base64
import json
from dataclasses import dataclass

from fastapi import Request


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
        roles = [c["val"] for c in payload.get("claims", []) if c.get("typ") == "roles"]
        return AuthUser(
            user_id=claims.get("oid", claims.get("sub", "unknown")),
            email=claims.get("preferred_username", claims.get("email", "")),
            roles=roles,
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def _parse_dev_headers(request: Request) -> AuthUser | None:
    user_id = request.headers.get("X-Dev-User-Id")
    if not user_id:
        return None
    email = request.headers.get("X-Dev-User-Email", f"{user_id}@dev.local")
    roles_header = request.headers.get("X-Dev-User-Roles", "runops.provisioner")
    roles = [r.strip() for r in roles_header.split(",") if r.strip()]
    return AuthUser(user_id=user_id, email=email, roles=roles)


def get_current_user(request: Request) -> AuthUser:
    user = _parse_principal_header(request) or _parse_dev_headers(request)
    if user is None:
        return AuthUser(
            user_id="anonymous",
            email="anonymous@dev.local",
            roles=["runops.provisioner"],
        )
    return user
