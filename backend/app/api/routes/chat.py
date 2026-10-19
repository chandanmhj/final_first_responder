"""The chat endpoint: text, quick-reply actions and an optional photo."""
from fastapi import APIRouter, Depends, File, Form, UploadFile

from ...core.errors import AppError
from ...core.security import AuthUser
from ...services.conversation.chat_service import ChatRequest
from ...state import Services
from ..deps import get_services, rate_limited

router = APIRouter(prefix="/api")

IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@router.post("/chat")
async def chat(
    message: str = Form(default="", max_length=4000),
    session_id: str | None = Form(default=None),
    action: str = Form(default="message"),
    role: str | None = Form(default=None),
    for_self: bool | None = Form(default=None),
    age_band: str | None = Form(default=None),
    lat: float | None = Form(default=None),
    lon: float | None = Form(default=None),
    image: UploadFile | None = File(default=None),
    user: AuthUser = Depends(rate_limited),
    services: Services = Depends(get_services),
):
    """Handle one turn. Returns the messages to show (text, step cards, photo result, hospitals, report)."""
    img = None
    if image is not None and image.filename:
        if (image.content_type or "") not in IMAGE_TYPES:
            raise AppError("Please send a JPEG, PNG or WebP image.")
        data = await image.read()
        if len(data) > services.settings.max_image_mb * 1024 * 1024:
            raise AppError(f"Image is larger than {services.settings.max_image_mb} MB.")
        img = (data, image.content_type)
    if action not in ("message", "next", "not_worked", "hospitals", "report", "restart"):
        raise AppError("Unknown action.")
    req = ChatRequest(message=message, session_id=session_id, action=action, role=role, for_self=for_self, age_band=age_band, lat=lat, lon=lon)
    return services.chat.handle(user.id, req, img)
