"""Turn a follow-up message into a standalone search query."""
from .generation import GroqClient


def rewrite_query(llm: GroqClient, message: str, step_text: str | None, condition_title: str | None) -> str:
    """Add context from the active step so 'what if it doesn't stop?' can be searched. Falls back to the raw message."""
    ctx = " ".join(x for x in [condition_title, step_text] if x)
    if not ctx:
        return message
    if not llm.ready:
        return f"{message} {ctx}"
    try:
        return llm.chat([
            {"role": "system", "content": "Rewrite the user's message as one short standalone first-aid search query. Output only the query."},
            {"role": "user", "content": f"Situation: {ctx}\nMessage: {message}"},
        ], temperature=0.0, max_tokens=60).strip() or message
    except Exception:
        return f"{message} {ctx}"
