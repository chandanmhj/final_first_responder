"""Friendly small talk that steers back to emergencies."""
from ..rag.generation import GroqClient

SYSTEM = ("You are First Responder, a calm and friendly emergency first-aid guide. Chat naturally and briefly (1 to 3 sentences). "
          "You can say hello and talk, but you do not give medical advice outside the guidelines. "
          "If the person describes an emergency, tell them to describe what happened so you can guide them, and to call 108 if it is serious.")

CANNED = [
    (r"\b(thanks|thank you)\b", "You're welcome. I'm here if you need anything."),
    (r"\b(bye|goodbye)\b", "Take care. If there's ever an emergency, I'm here, and 108 is always the number to call."),
    (r"\bhow are you\b", "I'm doing well, thank you for asking. How are you? If something has happened, tell me and I'll guide you."),
    (r"\b(who are you|what can you do)\b", "I'm First Responder. I guide you step by step through emergencies like chest pain, bleeding, choking, bites and accidents, and I can look at a photo too. What's happening?"),
]


def reply(llm: GroqClient, message: str, history: list[dict] | None = None) -> str:
    """Answer small talk with the model when available, otherwise a short canned reply."""
    import re

    if llm.ready:
        try:
            msgs = [{"role": "system", "content": SYSTEM}] + [{"role": h["role"], "content": h["content"]} for h in (history or [])[-6:]]
            msgs.append({"role": "user", "content": message})
            return llm.chat(msgs, temperature=0.6, max_tokens=120).strip()
        except Exception:
            pass
    for pat, text in CANNED:
        if re.search(pat, message, re.I):
            return text
    return "Hello! I'm First Responder. Tell me what's happening, or send a photo, and I'll guide you step by step. In an emergency, call 108."
