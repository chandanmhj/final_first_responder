"""Spot messages that describe a life-threatening situation so the app can show the call-108 banner."""
import re

URGENT = re.compile(
    r"(not breathing|stopped breathing|no pulse|unresponsive|unconscious|collapsed|choking|heavy bleeding|bleeding heavily|"
    r"snake|seizure|heart attack|chest pain|stroke|drowning|electrocut|severe allergic|anaphylaxis|not waking)", re.I)


def is_urgent(text: str) -> bool:
    """True when the text mentions a potentially life-threatening problem."""
    return bool(URGENT.search(text or ""))
