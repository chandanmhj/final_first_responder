"""Helpers shared by variants."""
from .config import DATA
from app.services.scenarios.loader import ScenarioStore
from app.services.scenarios.scenario_router import rule_based_match

_store = None


def route_condition(question):
    """Condition id guessed from the question with the rule-based router (None if unclear)."""
    global _store
    _store = _store or ScenarioStore(DATA)
    r = rule_based_match(question, _store)
    return r.condition if r.kind == "emergency" else None
