"""Telegram webhook. Telegram calls this for every message sent to the bot."""
import os

from fastapi import APIRouter, Body, Depends, Header, HTTPException

from ...services.telegram_bot import handle_update
from ...state import Services
from ..deps import get_services

router = APIRouter(prefix="/api/telegram")


@router.post("/webhook")
def webhook(update: dict = Body(...), x_telegram_bot_api_secret_token: str | None = Header(default=None),
            services: Services = Depends(get_services)):
    """Only requests carrying our secret (set when registering the webhook) are accepted."""
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    if not secret or x_telegram_bot_api_secret_token != secret:
        raise HTTPException(status_code=403, detail="Forbidden")
    handle_update(services, update)
    return {"ok": True}