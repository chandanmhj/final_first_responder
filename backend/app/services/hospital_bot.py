"""The demo hospital portal: a second Telegram bot that receives incoming-patient alerts and lets staff acknowledge them."""
import logging
import os

import httpx

log = logging.getLogger(__name__)
WELCOME = ("Hospital portal (demo)\n\nIncoming-patient alerts from First Responder appear in this chat, with the patient's age group, "
           "the emergency and the estimated arrival time. Tap Acknowledge on an alert to confirm the team is preparing.\n\n"
           "Send /myid to see this chat's ID.")


def _call(method: str, **payload) -> dict:
    token = (os.getenv("TELEGRAM_HOSPITAL_BOT_TOKEN") or "").strip()
    try:
        return httpx.post(f"https://api.telegram.org/bot{token}/{method}", json=payload, timeout=15).json()
    except Exception as exc:
        log.warning("hospital bot %s error: %s", method, exc)
        return {"ok": False}


def handle_hospital_update(update: dict) -> None:
    """Handle a message or button tap sent to the hospital bot."""
    cq = update.get("callback_query")
    if cq:
        _call("answerCallbackQuery", callback_query_id=cq["id"], text="Acknowledged")
        if cq.get("data") == "ack" and cq.get("message"):
            m = cq["message"]
            who = (cq.get("from") or {}).get("first_name", "Hospital staff")
            _call("editMessageText", chat_id=m["chat"]["id"], message_id=m["message_id"],
                  text=f"{m.get('text', '')}\n\nSTATUS: ACKNOWLEDGED by {who}. Emergency team is preparing.")
        return
    msg = update.get("message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    if chat_id is None:
        return
    text = (msg.get("text") or "").strip()
    if text.startswith("/myid"):
        reply = f"This chat's ID is {chat_id}"
    elif text.startswith("/start"):
        reply = WELCOME
    else:
        reply = "This is a demo hospital portal. Alerts appear here automatically when a patient is on the way."
    _call("sendMessage", chat_id=chat_id, text=reply)