"""Health check used by Render and by the frontend's 'server waking up' state."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """Return ok when the server is up."""
    return {"status": "ok"}
