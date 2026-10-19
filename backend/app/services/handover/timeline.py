"""Events recorded during an emergency, with timestamps."""
from datetime import datetime, timezone

EVENT_TYPES = {
    "scenario_started": "Emergency started",
    "step_shown": "Step shown",
    "step_done": "Step done",
    "step_not_worked": "Step did not work",
    "called_108": "Called 108",
    "ambulance_arrived": "Ambulance arrived",
    "cpr_started": "CPR started",
    "aed_used": "AED used",
    "tourniquet_applied": "Tourniquet applied",
    "helmet_removed": "Helmet removed",
    "patient_moved": "Patient moved",
    "photo_analyzed": "Photo analysed",
    "hospital_viewed": "Hospitals viewed",
    "note": "Note",
    "scenario_completed": "All steps completed",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def describe(event: dict) -> str:
    """One-line description of an event for the report."""
    label = EVENT_TYPES.get(event["event_type"], event["event_type"])
    p = event.get("payload") or {}
    extra = p.get("text") or p.get("step_text") or p.get("headline") or p.get("title") or ""
    return f"{label}: {extra}" if extra else label
