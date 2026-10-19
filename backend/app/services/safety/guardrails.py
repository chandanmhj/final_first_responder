"""Crisis detection. These messages get a fixed, careful reply instead of a model-generated one."""
import re

CRISIS = re.compile(r"\b(kill myself|want to die|end my life|suicid|self[- ]harm|hurt myself|don't want to live|no reason to live)\b", re.I)

CRISIS_REPLY = (
    "I'm really sorry you're feeling this way, and I'm glad you told me. You are not alone, and help is available right now.\n\n"
    "If you are in immediate danger, call 112 (emergency) or 108 (ambulance). "
    "You can also talk to someone free, any time: Tele-MANAS, 14416 (India, 24 hours).\n\n"
    "If you can, please stay with another person or let someone near you know how you feel. I can stay and talk with you too."
)


def is_crisis(text: str) -> bool:
    """True if the message suggests self-harm or suicidal thoughts."""
    return bool(CRISIS.search(text or ""))
