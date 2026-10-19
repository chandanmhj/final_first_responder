"""Shared FastAPI dependencies."""
from fastapi import Depends, Header, Request

from ..core.errors import Unauthorized
from ..core.security import AuthUser
from ..state import Services


def get_services(request: Request) -> Services:
    """The service container created at startup."""
    return request.app.state.services


def current_user(authorization: str | None = Header(default=None), services: Services = Depends(get_services)) -> AuthUser:
    """Authenticated user from the Authorization: Bearer header."""
    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif not services.settings.auth_disabled:
        raise Unauthorized("Please log in.")
    return services.verifier.verify(token)


def rate_limited(user: AuthUser = Depends(current_user), services: Services = Depends(get_services)) -> AuthUser:
    """Authenticated user who has not exceeded the per-minute limit."""
    services.limiter.check(user.id)
    return user
