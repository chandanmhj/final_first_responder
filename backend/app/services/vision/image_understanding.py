"""Describe an injury photo in plain words so the router can pick a scenario."""
from ..rag.generation import GroqClient

PROMPT = ("Describe in one or two short sentences what first-aid problem this photo shows (for example: deep bleeding cut, burn, "
          "swollen ankle, rash). Do not diagnose. The person says: \"{text}\". Return JSON: {{\"description\": \"...\"}}")


def describe(llm: GroqClient, image: bytes, mime: str, text: str) -> str:
    """Return a short description, or an empty string when the model is unavailable."""
    if not llm.ready:
        return ""
    try:
        return str(llm.vision_json(image, mime, PROMPT.format(text=text or "")).get("description", ""))[:300]
    except Exception:
        return ""
