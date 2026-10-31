"""Telegram bot: the same chat as the web app, with buttons, photos, videos and a shared location.

Every Telegram chat keeps its own conversation. All of them run under one Supabase user (TELEGRAM_USER_ID).
"""
import logging
import os

import httpx

from .conversation.chat_service import ChatRequest

log = logging.getLogger(__name__)
API = "https://api.telegram.org"
_MEM: dict[int, dict] = {}  # used only when there is no Supabase (local development)
WELCOME = ("Hi, I'm First Responder. Tell me what is happening, or send a photo or a short video, and I'll guide you one step at a time.\n\n"
           "Send /myid to see your Telegram ID (needed to be someone's emergency contact).\n\n"
           "Tap the button below to share your location so I can find the right hospital. Send /new to start a fresh chat.\n"
           "In a life-threatening emergency, call 108 now.")


def tg(method: str, **payload) -> dict:
    """Call the Telegram Bot API. Failures are logged, never raised."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    try:
        r = httpx.post(f"{API}/bot{token}/{method}", json=payload, timeout=25)
        data = r.json()
        if not data.get("ok"):
            log.warning("telegram %s failed: %s", method, data.get("description"))
        return data
    except Exception as exc:
        log.warning("telegram %s error: %s", method, exc)
        return {"ok": False}


class _Links:
    """Which conversation belongs to which Telegram chat (stored in Supabase, or in memory for development)."""

    def __init__(self, repo):
        self.c = getattr(repo, "c", None)
        self.mem = _MEM

    def get(self, chat_id: int) -> dict:
        blank = {"chat_id": chat_id, "session_id": None, "lat": None, "lon": None, "replies": [], "rev": 0, "last_update_id": 0}
        if self.c is None:
            return self.mem.setdefault(chat_id, blank)
        rows = self.c.table("telegram_chats").select("*").eq("chat_id", chat_id).limit(1).execute().data or []
        return rows[0] if rows else blank

    def save(self, row: dict) -> None:
        keep = {k: row.get(k) for k in ("chat_id", "session_id", "lat", "lon", "replies", "rev", "last_update_id")}
        if self.c is None:
            self.mem[row["chat_id"]] = keep
        else:
            self.c.table("telegram_chats").upsert(keep, on_conflict="chat_id").execute()


def _chunks(text: str, n: int = 3800) -> list[str]:
    return [text[i:i + n] for i in range(0, len(text), n)] or [""]


def convert(messages: list[dict], rev: int) -> tuple[list[dict], list[dict]]:
    """Turn the app's messages into Telegram messages. Returns (items to send, button replies to remember)."""
    items: list[dict] = []
    replies: list[dict] = []
    for m in messages:
        t = m.get("type")
        text, photo, url_buttons = m.get("text", ""), None, []
        if t == "step":
            s = m["step"]
            text = f"Step {s['index'] + 1} of {s['total']}\n\n{s['text']}\n\nSource: {s['source_label']}"
            if s.get("unreviewed_note"):
                text += f"\n{s['unreviewed_note']}"
            media = s.get("media") or {}
            photo = media.get("image")
            if media.get("video"):
                text += f"\n\nWatch: {media['video']}"
        elif t == "animal":
            r = m["result"]
            text = "\n".join([r["headline"], *[f"• {a}" for a in r.get("advice", [])], "", "A photo cannot confirm what an animal is. This is a best guess, not a diagnosis."])
        elif t == "hospitals":
            lines = [m.get("text", "Nearest suitable hospitals:")]
            for h in m.get("hospitals", [])[:3]:
                lines.append(f"• {h['name']} ({h['distance_km']} km)\n  {h['directions_url']}")
            text = "\n".join(lines)
        elif t == "hospital_prompt":
            text = f"{m['text']}\n\nCall 108 now."
            if m.get("hospital"):
                h = m["hospital"]
                text += f"\nBest match: {h['name']} ({h.get('tier') or 'hospital'}, {h['distance_km']} km)"
            url_buttons = [[{"text": "Open in Google Maps", "url": m["maps_url"]}], [{"text": "I'm going there", "callback_data": f"h:{rev}"}]]
        elif t == "report":
            text = f"{m['text']}\n\n{m.get('markdown', '')}\n\nSend any message to start a new chat."
        rows = list(url_buttons)
        for r in m.get("quick_replies") or []:
            replies.append({"action": r["action"], "text": r.get("text") or r["label"]})
            rows.append([{"text": r["label"][:60], "callback_data": f"r:{rev}:{len(replies) - 1}"}])
        if text.strip():
            items.append({"text": text, "photo": photo, "markup": {"inline_keyboard": rows} if rows else None})
    return items, replies


def _send(chat_id: int, items: list[dict]) -> None:
    for it in items:
        parts, markup = _chunks(it["text"]), it["markup"]
        if it["photo"] and len(it["text"]) <= 1000:
            extra = {"reply_markup": markup} if markup else {}
            if tg("sendPhoto", chat_id=chat_id, photo=it["photo"], caption=it["text"], **extra).get("ok"):
                continue
        for i, part in enumerate(parts):
            extra = {"reply_markup": markup} if (markup and i == len(parts) - 1) else {}
            tg("sendMessage", chat_id=chat_id, text=part, disable_web_page_preview=True, **extra)


def _download(file_id: str, mime: str) -> tuple[bytes, str] | None:
    info = tg("getFile", file_id=file_id)
    path = (info.get("result") or {}).get("file_path")
    if not path:
        return None
    try:
        r = httpx.get(f"{API}/file/bot{os.getenv('TELEGRAM_BOT_TOKEN', '')}/{path}", timeout=25)
        return (r.content, mime) if r.status_code == 200 else None
    except Exception:
        return None


def handle_update(services, update: dict) -> None:
    """Process one Telegram update (a message, a photo, a video, a location or a button tap)."""
    user_id = os.getenv("TELEGRAM_USER_ID")
    if not user_id:
        log.error("TELEGRAM_USER_ID is not set")
        return
    links = _Links(services.repo)
    cq = update.get("callback_query")
    msg = update.get("message") or {}
    chat_id = (cq or {}).get("message", {}).get("chat", {}).get("id") if cq else (msg.get("chat") or {}).get("id")
    if chat_id is None:
        return
    row = links.get(chat_id)
    if update.get("update_id", 0) <= (row.get("last_update_id") or 0):
        return  # Telegram retry of something already handled
    row["last_update_id"] = update.get("update_id", 0)
    links.save(row)

    action, text, image = "message", "", None
    if cq:
        tg("answerCallbackQuery", callback_query_id=cq["id"])
        if (cq.get("data") or "").startswith("h:"):  # "I'm going there": alert the hospital
            if (cq["data"].split(":") + [""])[1] != str(row.get("rev")):
                tg("sendMessage", chat_id=chat_id, text="That button has expired. Please use the buttons on the newest message.")
                return
            out = services.chat.notify_hospital_for_session(user_id, row.get("session_id"))
            tg("sendMessage", chat_id=chat_id, text=f"The hospital has been alerted. Expected arrival: about {out['eta_min']} min." if out.get("sent")
               else "The hospital was already alerted." if out.get("already") else "I could not alert the hospital right now. Please call 108.")
            return
        try:
            _, rev, idx = (cq.get("data") or "").split(":")
            if int(rev) != row.get("rev"):
                tg("sendMessage", chat_id=chat_id, text="That button has expired. Please use the buttons on the newest message.")
                return
            reply = row["replies"][int(idx)]
        except (ValueError, IndexError):
            return
        action, text = ("message", reply.get("text", "")) if reply["action"] == "ask" else (reply["action"], "")
    elif msg.get("location"):
        row["lat"], row["lon"] = msg["location"]["latitude"], msg["location"]["longitude"]
        links.save(row)
        tg("sendMessage", chat_id=chat_id, text="Location saved. I will use it to pick the right hospital.")
        return
    elif msg.get("photo"):
        image = _download(msg["photo"][-1]["file_id"], "image/jpeg")
        text = msg.get("caption", "")
        if image is None:
            tg("sendMessage", chat_id=chat_id, text="I could not download that photo. Please try again.")
            return
    elif msg.get("video") or msg.get("video_note") or msg.get("animation"):
        v = msg.get("video") or msg.get("video_note") or msg.get("animation")
        image = _download(v["file_id"], "video/mp4")
        text = msg.get("caption", "")
        if image is None:
            tg("sendMessage", chat_id=chat_id, text="I could not download that video. Telegram only lets bots read videos up to 20 MB, so please send a shorter clip.")
            return
    elif msg.get("text"):
        text = msg["text"].strip()
        if text.startswith("/start"):
            tg("sendMessage", chat_id=chat_id, text=WELCOME, reply_markup={"keyboard": [[{"text": "Share my location", "request_location": True}]], "resize_keyboard": True})
            return
        if text.startswith("/myid"):
            tg("sendMessage", chat_id=chat_id, text=f"Your Telegram ID is {chat_id}\nGive it to the person who wants to add you as an emergency contact.")
            return
        if text.startswith("/new"):
            row["session_id"], row["replies"] = None, []
            links.save(row)
            tg("sendMessage", chat_id=chat_id, text="New chat started. Tell me what is happening.")
            return
    else:
        tg("sendMessage", chat_id=chat_id, text="I can read text, photos and short videos here. Please type or send one of those.")
        return

    tg("sendChatAction", chat_id=chat_id, action="typing")
    req = ChatRequest(message=text, session_id=row.get("session_id"), action=action, lat=row.get("lat"), lon=row.get("lon"))
    try:
        res = services.chat.handle(user_id, req, image)
    except Exception:
        log.exception("telegram chat turn failed")
        tg("sendMessage", chat_id=chat_id, text="Something went wrong. Please try again. If someone is in danger, call 108 now.")
        return
    row["rev"] = (row.get("rev") or 0) + 1
    items, replies = convert(res["messages"], row["rev"])
    row["replies"] = replies
    row["session_id"] = None if res.get("ended") else res["session_id"]
    _send(chat_id, items)
    links.save(row)