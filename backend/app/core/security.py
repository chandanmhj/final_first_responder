"""Verify Supabase access tokens by asking Supabase Auth who the token belongs to."""
import time
from dataclasses import dataclass

import httpx

from ..config import Settings
from .errors import Unauthorized


@dataclass
class AuthUser:
    """The signed-in user."""

    id: str
    email: str | None = None


class TokenVerifier:
    """Validates a bearer token against Supabase Auth, with a short cache."""

    def __init__(self, settings: Settings, ttl: float = 60.0):
        self.settings = settings
        self.ttl = ttl
        self._cache: dict[str, tuple[float, AuthUser]] = {}

    def verify(self, token: str) -> AuthUser:
        """Return the user for a valid token or raise Unauthorized."""
        s = self.settings
        if s.auth_disabled and s.env != "production":
            return AuthUser(id="00000000-0000-0000-0000-000000000001", email="dev@example.com")
        if not token:
            raise Unauthorized("Missing access token.")
        hit = self._cache.get(token)
        if hit and time.monotonic() - hit[0] < self.ttl:
            return hit[1]
        if not s.supabase_url:
            raise Unauthorized("Authentication is not configured on the server.")
        try:
            r = httpx.get(
                f"{s.supabase_url.rstrip('/')}/auth/v1/user",
                headers={"Authorization": f"Bearer {token}", "apikey": s.supabase_anon_key or s.supabase_service_role_key},
                timeout=8.0,
            )
        except httpx.HTTPError as exc:
            raise Unauthorized("Could not reach the authentication service.") from exc
        if r.status_code != 200:
            raise Unauthorized("Invalid or expired session. Please log in again.")
        data = r.json()
        user = AuthUser(id=data["id"], email=data.get("email"))
        self._cache[token] = (time.monotonic(), user)
        return user
