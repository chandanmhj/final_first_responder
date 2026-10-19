"""Media lookup for a step."""
from fastapi import APIRouter, Depends

from ...core.security import AuthUser
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api/media")


@router.get("/step/{step_id}")
def step_media(step_id: str, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Video and image URLs for a step (null when there is none)."""
    return services.media.resolve(step_id)
