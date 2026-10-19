"""Load scenario modules, conditions, locations and settings from data/scenarios."""
import glob
import os
from dataclasses import dataclass, field

import yaml


@dataclass
class Step:
    """One instruction inside a module."""

    id: str
    module: str
    n: int
    text: str
    roles: list[str]
    source: str
    self_text: str | None = None
    page: str | None = None
    tags: list[str] = field(default_factory=list)
    only_groups: list[str] = field(default_factory=list)
    not_worked: dict | None = None


@dataclass
class Module:
    id: str
    title: str
    steps: list[Step]
    note: str | None = None


@dataclass
class Condition:
    id: str
    title: str
    roles: list[str]
    groups: list[str]
    modules: list[str]
    valid_locations: list[str]
    facility_requirements: str
    forbid_tags: list[str]
    note: str | None = None


class ScenarioStore:
    """In-memory view of all scenario data."""

    def __init__(self, data_dir: str):
        base = os.path.join(data_dir, "scenarios")
        self.modules: dict[str, Module] = {}
        for path in sorted(glob.glob(os.path.join(base, "modules", "*.yaml"))) + sorted(
            glob.glob(os.path.join(base, "extensions", "module_*.yaml"))
        ):
            raw = yaml.safe_load(open(path, encoding="utf-8"))
            steps = [
                Step(
                    id=s["id"], module=raw["id"], n=s["n"], text=s["text"], roles=s["roles"], source=s["source"],
                    self_text=s.get("self_text"), page=str(s["page"]) if s.get("page") else None, tags=s.get("tags", []),
                    only_groups=s.get("only_groups", []), not_worked=s.get("not_worked"),
                )
                for s in raw["steps"]
            ]
            self.modules[raw["id"]] = Module(raw["id"], raw["title"], steps, raw.get("note"))
        conds = dict(yaml.safe_load(open(os.path.join(base, "conditions.yaml"), encoding="utf-8"))["conditions"])
        for path in sorted(glob.glob(os.path.join(base, "extensions", "condition_*.yaml"))):
            conds.update(yaml.safe_load(open(path, encoding="utf-8"))["conditions"])
        self.conditions = {
            cid: Condition(
                id=cid, title=c["title"], roles=c["roles"], groups=c.get("groups", []), modules=c["modules"],
                valid_locations=c["valid_locations"], facility_requirements=c["facility_requirements"],
                forbid_tags=c.get("forbid_tags", []), note=c.get("note"),
            )
            for cid, c in conds.items()
        }
        self.locations = yaml.safe_load(open(os.path.join(base, "locations.yaml"), encoding="utf-8"))["locations"]
        self.age_bands = yaml.safe_load(open(os.path.join(base, "age_bands.yaml"), encoding="utf-8"))
        self.glossary = yaml.safe_load(open(os.path.join(base, "term_glossary.yaml"), encoding="utf-8"))["terms"]
