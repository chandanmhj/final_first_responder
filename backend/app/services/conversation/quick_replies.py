"""Quick-reply buttons shown under each step."""


def for_step(step: dict, is_last: bool) -> list[dict]:
    """Buttons for one step: Next (or Finish) and a step-specific 'did not work' button."""
    nw = step.get("not_worked") or {}
    return [
        {"id": "next", "action": "next", "label": "Done, show hospitals" if is_last else "Done, next step"},
        {"id": "not_worked", "action": "not_worked", "label": nw.get("label") or "That didn't work"},
    ]


def after_completion() -> list[dict]:
    """Buttons shown when the last step is done."""
    return [
        {"id": "hospitals", "action": "hospitals", "label": "Nearest hospitals"},
        {"id": "report", "action": "report", "label": "Handover report"},
        {"id": "restart", "action": "restart", "label": "Start over"},
    ]
