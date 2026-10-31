"""Telegram alerts sent by the backend: emergency contacts, and the (demo) hospital."""
import logging
import os
import re

import httpx

log = logging.getLogger(__name__)
AVG_SPEED_KMH = 30.0  # rough city driving speed, used for the arrival estimate


def send_telegram(chat_id, text: str, token: str | None = None, reply_markup: dict | None = None) -> bool:
    """Send one Telegram message (from the main bot, or from the bot whose token is given). Returns False, never raises, on failure."""
    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or not chat_id:
        return False
    payload = {"chat_id": chat_id, "text": text[:3900], "disable_web_page_preview": True}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        r = httpx.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload, timeout=6)
        ok = bool(r.json().get("ok"))
        if not ok:
            log.warning("telegram alert failed: %s", r.text[:200])
        return ok
    except Exception as exc:
        log.warning("telegram alert error: %s", exc)
        return False

def parse_ids(raw) -> list[str]:
    """Telegram chat IDs typed as '123456789, 987654321'."""
    return re.findall(r"-?\d{5,}", raw or "")


def eta_minutes(distance_km: float) -> int:
    return max(1, round(float(distance_km) / AVG_SPEED_KMH * 60))