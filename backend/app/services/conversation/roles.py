"""Age bands and the protocol (infant, child, adult) they map to."""
import re

from ..scenarios.loader import ScenarioStore


def band_protocol(store: ScenarioStore, band: str | None) -> str:
    """Return 'infant', 'child' or 'adult' for an age band id such as '0-1' or '18+'."""
    for b in store.age_bands["bands"]:
        if b["id"] == band:
            return b["protocol"]
    return store.age_bands.get("unknown_default", "adult")


def infer_age_band(text: str) -> str | None:
    """Guess an age band from free text such as 'my 2 year old' or 'a baby'. Returns None if unclear."""
    t = text.lower()
    if re.search(r"\b(baby|infant|newborn|months? old)\b", t):
        return "0-1"
    m = re.search(r"\b(\d{1,2})\s*(?:-| )?\s*(?:years?|yrs?|y)\s*(?:-| )?old\b", t) or re.search(r"\bage[d]? (\d{1,2})\b", t)
    if m:
        age = int(m.group(1))
        return "0-1" if age < 1 else "1-5" if age < 5 else "5-10" if age < 10 else "10-18" if age < 18 else "18+"
    if re.search(r"\b(toddler|kid|child|son|daughter)\b", t):
        return "5-10" if "toddler" not in t else "1-5"
    return None


def adjust_condition(condition_id: str, protocol: str) -> str:
    """Swap adult conditions for infant/child versions when the patient is a baby or child."""
    if condition_id == "cardiac_arrest_adult" and protocol in ("infant", "child"):
        return "cardiac_arrest_child_infant"
    if condition_id == "choking_adult_child" and protocol == "infant":
        return "choking_infant"
    return condition_id
