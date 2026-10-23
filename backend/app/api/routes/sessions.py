"""Conversation list and history."""
from fastapi import APIRouter, Depends

from ...core.errors import NotFound
from ...core.security import AuthUser
from ...schemas.session import SessionPatch
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api/sessions")


@router.get("")
def list_sessions(user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """The user's conversations: pinned first, then newest first."""
    out = []
    for s in services.repo.list_sessions(user.id):
        st = s.get("state") or {}
        cond = services.store.conditions.get(st.get("condition")) if st.get("condition") else None
        out.append({"id": s["id"], "title": s["title"], "updated_at": s["updated_at"], "status": st.get("status", "idle"),
                    "condition": cond.title if cond else None, "incident_id": st.get("incident_id"),
                    "pinned": bool(s.get("pinned"))})
    out.sort(key=lambda x: not x["pinned"])  # stable sort keeps newest-first within each group
    return out


@router.get("/{session_id}/messages")
def messages(session_id: str, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """All messages in a conversation, plus where the scenario stands."""
    s = services.repo.get_session(user.id, session_id)
    if not s:
        raise NotFound("Conversation not found.")
    return {"session": {"id": s["id"], "title": s["title"], "state": s.get("state") or {}},
            "messages": services.repo.list_messages(user.id, session_id)}


@router.patch("/{session_id}")
def patch(session_id: str, body: SessionPatch, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Rename and/or pin a conversation."""
    data = body.model_dump(exclude_none=True)
    if not data or not services.repo.update_session(user.id, session_id, data):
        raise NotFound("Conversation not found.")
    return {"ok": True}


@router.delete("/{session_id}")
def delete(session_id: str, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Delete a conversation and its messages."""
    if not services.repo.delete_session(user.id, session_id):
        raise NotFound("Conversation not found.")
    return {"ok": True}