"""Conversation list and history."""
from fastapi import APIRouter, Depends

from ...core.errors import NotFound
from ...core.security import AuthUser
from ...schemas.session import SessionRename
from ...state import Services
from ..deps import current_user, get_services

router = APIRouter(prefix="/api/sessions")


@router.get("")
def list_sessions(user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """The user's conversations, newest first."""
    out = []
    for s in services.repo.list_sessions(user.id):
        st = s.get("state") or {}
        cond = services.store.conditions.get(st.get("condition")) if st.get("condition") else None
        out.append({"id": s["id"], "title": s["title"], "updated_at": s["updated_at"], "status": st.get("status", "idle"),
                    "condition": cond.title if cond else None, "incident_id": st.get("incident_id")})
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
def rename(session_id: str, body: SessionRename, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Rename a conversation."""
    if not services.repo.update_session(user.id, session_id, {"title": body.title}):
        raise NotFound("Conversation not found.")
    return {"ok": True}


@router.delete("/{session_id}")
def delete(session_id: str, user: AuthUser = Depends(current_user), services: Services = Depends(get_services)):
    """Delete a conversation and its messages."""
    if not services.repo.delete_session(user.id, session_id):
        raise NotFound("Conversation not found.")
    return {"ok": True}
