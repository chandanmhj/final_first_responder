"""Turn a condition + location + role into an ordered list of steps."""
import re
from dataclasses import dataclass, field

from .loader import ScenarioStore, Step

ROLE_CODE = {"common": "B", "responder": "R"}


@dataclass
class ResolvedStep:
    """A step ready to show to one user."""

    id: str
    index: int
    total: int
    module: str
    text: str
    source: str
    page: str | None
    authored: bool
    tags: list[str] = field(default_factory=list)
    not_worked: dict | None = None

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def role_code(role: str, for_self: bool) -> str:
    """Map the profile role and the 'for me or someone else' choice to B, S or R."""
    if role == "responder":
        return "R"
    return "S" if for_self else "B"


def to_clinical(text: str, glossary: dict[str, str]) -> str:
    """Replace everyday words with clinical terms for certified first responders (longest terms first)."""
    out = text
    for plain in sorted(glossary, key=len, reverse=True):
        clinical = glossary[plain]
        if plain == clinical:
            continue
        out = re.sub(rf"\b{re.escape(plain)}\b", clinical, out, flags=re.I)
    return out


def ordered_modules(store: ScenarioStore, condition_id: str, location_id: str) -> list[str]:
    """Location hazard modules first, then the condition's modules, without repeats."""
    cond = store.conditions[condition_id]
    prefix = store.locations.get(location_id, {}).get("prefix", [])
    seen, out = set(), []
    for m in list(prefix) + list(cond.modules):
        if m in store.modules and m not in seen:
            seen.add(m)
            out.append(m)
    return out


def valid_location(store: ScenarioStore, condition_id: str, location_id: str | None) -> str:
    """Return the location if it is valid for the condition, otherwise the condition's first valid location."""
    cond = store.conditions[condition_id]
    if location_id in cond.valid_locations:
        return location_id
    return "home" if "home" in cond.valid_locations else cond.valid_locations[0]


def compose(store: ScenarioStore, condition_id: str, location_id: str, role: str, for_self: bool,
            show_authored: bool = True) -> list[ResolvedStep]:
    """Build the step list for this user. Steps are filtered by role and by the condition's groups."""
    cond = store.conditions[condition_id]
    code = role_code(role, for_self)
    if code == "S" and "S" not in cond.roles:
        code = "B"  # the patient cannot do this alone: show the helper version
    raw: list[Step] = []
    for mid in ordered_modules(store, condition_id, location_id):
        for s in store.modules[mid].steps:
            if code not in s.roles:
                continue
            if s.only_groups and not set(s.only_groups) & set(cond.groups):
                continue
            if s.source == "authored" and not show_authored:
                continue
            raw.append(s)
    total = len(raw)
    out = []
    for i, s in enumerate(raw):
        text = s.self_text if (code == "S" and s.self_text) else s.text
        if code == "R":
            text = to_clinical(text, store.glossary)
        out.append(ResolvedStep(
            id=s.id, index=i, total=total, module=s.module, text=text, source=s.source, page=s.page,
            authored=s.source == "authored", tags=s.tags, not_worked=s.not_worked,
        ))
    return out
