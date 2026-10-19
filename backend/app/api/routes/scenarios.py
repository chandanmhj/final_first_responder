"""List the emergencies the app knows (for the quick-start grid)."""
from fastapi import APIRouter, Depends

from ...core.security import AuthUser
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api/scenarios")


@router.get("/conditions")
def conditions(user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Condition ids and titles."""
    return [{"id": c.id, "title": c.title} for c in services.store.conditions.values()]
