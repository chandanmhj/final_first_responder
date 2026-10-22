"""Quick-reply buttons shown under each step."""


def for_step(step: dict, is_last: bool) -> list[dict]:
    """Buttons for one step: Next (or Done) and a step-specific 'did not work' button."""
    nw = step.get("not_worked") or {}
    return [
        {"id": "next", "action": "next", "label": "Done" if is_last else "Done, next step"},
        {"id": "not_worked", "action": "not_worked", "label": nw.get("label") or "That didn't work"},
    ]


def after_completion() -> list[dict]:
    """No buttons now. The handover report comes from typing 'paramedics arrived'."""
    return []