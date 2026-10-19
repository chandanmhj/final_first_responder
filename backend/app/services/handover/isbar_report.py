"""Build the handover report in ISBAR format (Identify, Situation, Background, Assessment, Recommendation)."""
from .timeline import describe, now_iso


def build_report(incident: dict, events: list[dict], condition_title: str | None, facility_text: str | None,
                 profile: dict | None = None) -> dict:
    """Return the report as a dict. The timeline is in time order."""
    events = sorted(events, key=lambda e: e["occurred_at"])
    notes = [e["payload"].get("text", "") for e in events if e["event_type"] == "note"]
    key = [e for e in events if e["event_type"] not in ("step_shown",)]
    timeline = [{"time": e["occurred_at"], "text": describe(e), "type": e["event_type"]} for e in key]
    return {
        "generated_at": now_iso(),
        "identify": {
            "reported_by_role": incident.get("role"), "patient": "the reporter" if incident.get("for_self") else "another person",
            "age_band": incident.get("age_band"), "started_at": incident.get("started_at"),
            "location": incident.get("location_text") or incident.get("location"),
        },
        "situation": {"what_happened": condition_title or "Unknown emergency", "scenario": incident.get("condition")},
        "background": {"notes": notes},
        "assessment_and_actions": timeline,
        "recommendation": {"facility_needs": facility_text, "call": "108"},
    }


def to_markdown(report: dict) -> str:
    """Plain-text version for copying or printing."""
    i, s = report["identify"], report["situation"]
    lines = [
        "# Handover report (ISBAR)", "",
        f"Generated: {report['generated_at']}", "",
        "## I: Identify", f"- Reported by: {i['reported_by_role']}", f"- Patient: {i['patient']}, age group {i['age_band'] or 'unknown'}",
        f"- Started: {i['started_at']}", f"- Location: {i['location'] or 'not recorded'}", "",
        "## S: Situation", f"- {s['what_happened']}", "",
        "## B: Background"] + ([f"- {n}" for n in report["background"]["notes"]] or ["- None recorded"]) + ["", "## A: Assessment and actions (timeline)"]
    lines += [f"- {t['time']}  {t['text']}" for t in report["assessment_and_actions"]] or ["- No events recorded"]
    lines += ["", "## R: Recommendation", f"- Hospital needs: {report['recommendation']['facility_needs'] or 'nearest emergency department'}", "- Ambulance: 108"]
    return "\n".join(lines) + "\n"
