"""Nearest suitable hospitals."""
from fastapi import APIRouter, Depends, Query

from ...core.security import AuthUser
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api/hospitals")


@router.get("/nearby")
def nearby(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180), condition: str | None = None,
           limit: int = Query(default=5, ge=1, le=10), user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Hospitals ranked for the emergency type and distance."""
    return services.hospitals.nearby(lat, lon, condition, limit)
