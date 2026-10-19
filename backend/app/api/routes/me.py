"""Current user's profile (name and role)."""
from fastapi import APIRouter, Depends

from ...core.errors import AppError
from ...core.security import AuthUser
from ...schemas.session import ProfileUpdate
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api")


@router.get("/me")
def get_me(user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """The profile, or an empty profile with role null for a new user."""
    p = services.repo.get_profile(user.id) or {}
    return {"id": user.id, "email": user.email, "full_name": p.get("full_name"), "role": p.get("role"),
            "cert_number": p.get("cert_number"), "attested_at": p.get("attested_at")}


@router.put("/me")
def put_me(body: ProfileUpdate, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Update the profile. Certified first responder needs the 'I am trained' confirmation."""
    patch = {k: v for k, v in body.model_dump().items() if v is not None and k != "attested"}
    if body.role == "responder":
        existing = services.repo.get_profile(user.id) or {}
        if not (body.attested or existing.get("attested_at")):
            raise AppError("Please confirm that you are a trained first responder.")
        if body.attested:
            from datetime import datetime, timezone
            patch["attested_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    p = services.repo.upsert_profile(user.id, patch)
    return {"id": user.id, "email": user.email, "full_name": p.get("full_name"), "role": p.get("role"),
            "cert_number": p.get("cert_number"), "attested_at": p.get("attested_at")}
