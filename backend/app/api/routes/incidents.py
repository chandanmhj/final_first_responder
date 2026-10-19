"""Incidents, their events, and the handover report."""
from fastapi import APIRouter, Depends

from ...core.errors import NotFound
from ...core.security import AuthUser
from ...schemas.handover import EventIn
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api/incidents")


@router.get("")
def list_incidents(user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """The user's incidents, newest first."""
    out = []
    for i in services.repo.list_incidents(user.id):
        c = services.store.conditions.get(i["condition"])
        out.append({"id": i["id"], "title": c.title if c else i["condition"], "started_at": i["started_at"], "status": i.get("status")})
    return out


@router.post("/{incident_id}/events")
def add_event(incident_id: str, body: EventIn, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Record something that happened (for example 'called 108' or a note)."""
    if not services.repo.get_incident(user.id, incident_id):
        raise NotFound("Incident not found.")
    e = services.repo.add_event(user.id, incident_id, body.event_type, {"text": body.text or ""}, body.occurred_at)
    return {"id": e["id"], "occurred_at": e["occurred_at"]}


@router.get("/{incident_id}/handover")
def handover(incident_id: str, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """The ISBAR handover report as data and as plain text."""
    if not services.repo.get_incident(user.id, incident_id):
        raise NotFound("Incident not found.")
    return services.chat.build_handover(user.id, incident_id)
