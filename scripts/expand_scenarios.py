"""Expand scenario modules into full scenarios, validate them, and generate docs and media lists.

Reads:
    data/scenarios/modules/*.yaml       reusable step modules
    data/scenarios/conditions.yaml      conditions: modules, roles, valid locations, forbidden tags
    data/scenarios/locations.yaml       locations and the hazard/scene-safety modules they add first
    data/scenarios/extensions/*.yaml    optional extra modules and conditions for rare situations

Writes:
    data/scenarios/generated/scenarios.yaml   every valid scenario with its ordered modules
    docs/scenarios/catalog.md                 human-readable catalog
    media/manifest.yaml                       one entry per step with the expected video/image names
    media/replace.md                          checklist for you to fill (only if missing, or with --overwrite-replace)

Usage:
    python scripts/expand_scenarios.py
    python scripts/expand_scenarios.py --overwrite-replace

Validation fails (exit code 1) if a scenario references an unknown module, or a resolved step carries a
tag listed in the condition's ``forbid_tags``.
"""
import argparse
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "data", "scenarios")
ROLE_NAMES = {"B": "bystander", "S": "self", "R": "first responder"}


def load_yaml(path):
    """Load a YAML file and return its content."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_modules():
    """Load all step modules (core plus extensions) keyed by module id.

    Returns:
        dict: module id to module dict.
    """
    modules = {}
    for path in sorted(glob.glob(os.path.join(SC, "modules", "*.yaml"))) + sorted(
        glob.glob(os.path.join(SC, "extensions", "module_*.yaml"))
    ):
        m = load_yaml(path)
        modules[m["id"]] = m
    return modules


def load_conditions():
    """Load conditions (core plus extensions) keyed by condition id."""
    conditions = dict(load_yaml(os.path.join(SC, "conditions.yaml"))["conditions"])
    for path in sorted(glob.glob(os.path.join(SC, "extensions", "condition_*.yaml"))):
        conditions.update(load_yaml(path)["conditions"])
    return conditions


def ordered_modules(prefix, cond_modules):
    """Return the module order for a scenario: location prefix first, then the condition's modules.

    A module appears once; the first occurrence wins.
    """
    seen, out = set(), []
    for mid in list(prefix) + list(cond_modules):
        if mid not in seen:
            seen.add(mid)
            out.append(mid)
    return out


def resolve_steps(module_ids, modules, role, groups=()):
    """Return the steps a role sees for the given modules, in order.

    A step with ``only_groups`` is included only if the condition belongs to one of those groups
    (for example ``trauma`` or ``cardiac``). Modules with no step for the role are dropped.
    """
    steps = []
    for mid in module_ids:
        for s in modules[mid]["steps"]:
            if role in s["roles"] and (not s.get("only_groups") or set(s["only_groups"]) & set(groups)):
                steps.append({**s, "module": mid})
    return steps


def slug(text, words=5):
    """Make a short file-name slug from the first words of a step text."""
    w = re.sub(r"[^a-z0-9 ]", "", text.lower()).split()[:words]
    return "-".join(w) or "step"


def expand():
    """Expand and validate all scenarios.

    Returns:
        tuple: (scenarios list, modules dict, conditions dict, locations dict, errors list).
    """
    modules = load_modules()
    conditions = load_conditions()
    locations = load_yaml(os.path.join(SC, "locations.yaml"))["locations"]
    scenarios, errors = [], []
    for cid, c in conditions.items():
        for loc in c["valid_locations"]:
            if loc not in locations:
                errors.append(f"{cid}: unknown location {loc}")
                continue
            mods = ordered_modules(locations[loc]["prefix"], c["modules"])
            missing = [m for m in mods if m not in modules]
            if missing:
                errors.append(f"{cid}__{loc}: unknown modules {missing}")
                continue
            counts = {}
            for role in c["roles"]:
                steps = resolve_steps(mods, modules, role, c.get("groups", []))
                if not steps:
                    errors.append(f"{cid}__{loc}: no steps for role {role}")
                bad = [s["id"] for s in steps if set(s.get("tags", [])) & set(c.get("forbid_tags", []))]
                if bad:
                    errors.append(f"{cid}__{loc}: forbidden tags on steps {bad}")
                counts[role] = len(steps)
            scenarios.append({
                "id": f"{cid}__{loc}",
                "title": f"{c['title']} - {locations[loc]['label']}",
                "condition": cid,
                "location": loc,
                "roles": c["roles"],
                "modules": mods,
                "steps_per_role": counts,
                "facility_requirements": c["facility_requirements"],
            })
    return scenarios, modules, conditions, locations, errors


def write_generated(scenarios):
    """Write data/scenarios/generated/scenarios.yaml."""
    out = os.path.join(SC, "generated")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "scenarios.yaml"), "w", encoding="utf-8") as f:
        f.write("# Generated by scripts/expand_scenarios.py. Do not edit by hand.\n")
        yaml.safe_dump({"scenarios": scenarios}, f, sort_keys=False, allow_unicode=True, width=120)


def write_catalog(scenarios, modules, conditions):
    """Write docs/scenarios/catalog.md."""
    lines = ["# Scenario catalog", "",
             "Generated by `scripts/expand_scenarios.py`. Do not edit by hand.", "",
             f"- Scenarios: **{len(scenarios)}** (from {len(conditions)} conditions)",
             f"- Step modules: **{len(modules)}**, steps: **{sum(len(m['steps']) for m in modules.values())}**",
             "- Roles: B = bystander, S = self (the patient), R = first responder (trained).", ""]
    for cid, c in conditions.items():
        lines += [f"## {c['title']}", "", f"Roles: {', '.join(ROLE_NAMES[r] for r in c['roles'])}. "
                  f"Facility: {c['facility_requirements']}"]
        if c.get("note"):
            lines.append(f"Note: {c['note']}")
        lines += ["", "| Scenario | Location | Modules in order | Steps (B/S/R) |", "|---|---|---|---|"]
        for s in scenarios:
            if s["condition"] == cid:
                n = s["steps_per_role"]
                lines.append(f"| `{s['id']}` | {s['location']} | {' > '.join(s['modules'])} | "
                             f"{n.get('B', '-')}/{n.get('S', '-')}/{n.get('R', '-')} |")
        lines.append("")
    path = os.path.join(ROOT, "docs", "scenarios", "catalog.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_media(scenarios, modules, overwrite_replace):
    """Write media/manifest.yaml and (if allowed) media/replace.md."""
    usage = {m: 0 for m in modules}
    for s in scenarios:
        for m in s["modules"]:
            usage[m] += 1
    entries = []
    for mid, m in modules.items():
        for s in m["steps"]:
            base = f"emergencies/{mid}/{s['n']:02d}-{slug(s['text'])}"
            entries.append({"step_id": s["id"], "module": mid, "video": base + ".mp4", "image": base + ".webp",
                            "status": "missing"})
    with open(os.path.join(ROOT, "media", "manifest.yaml"), "w", encoding="utf-8") as f:
        f.write("# Generated by scripts/expand_scenarios.py. status: missing | video | image | both\n")
        yaml.safe_dump({"media": entries}, f, sort_keys=False, allow_unicode=True, width=120)

    rp = os.path.join(ROOT, "media", "replace.md")
    if os.path.exists(rp) and not overwrite_replace:
        # Protect your ticks: only replace the original empty skeleton.
        if "not confirmed yet" not in open(rp, encoding="utf-8").read():
            return
    lines = ["# Media placeholders (replace.md)", "",
             "You add the videos and images. Each step below has a video name and an image name. "
             "Provide either, both, or neither. If neither exists for a step, the app sends text only.", "",
             "Steps are grouped by **module**. A module is reused by many scenarios (for example `cpr_adult` appears in "
             "every cardiac arrest scenario), so one clip serves all of them. Work from the top: the list is sorted by how many "
             "scenarios use each module.", "",
             "## How to name and store files", "",
             "- Put originals in `media/emergencies/<module>/` using the names below, compressed outputs in `media/processed/`.",
             "- Video: MP4 (H.264), 480p to 720p, about 10 to 20 seconds, muted unless audio is needed. Image: WebP.",
             "- Tick the box when a file is added, and update `media/manifest.yaml` status (`video`, `image` or `both`).",
             "- Re-running `python scripts/expand_scenarios.py --overwrite-replace` rebuilds this file and erases your ticks.", "",
             "## Production priority", "", "| Module | Title | Used in scenarios | Steps |", "|---|---|---|---|"]
    for mid, n in sorted(usage.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| `{mid}` | {modules[mid]['title']} | {n} | {len(modules[mid]['steps'])} |")
    for mid, n in sorted(usage.items(), key=lambda kv: (-kv[1], kv[0])):
        m = modules[mid]
        lines += ["", f"## {m['title']} (`{mid}`)", f"Used in {n} scenarios.", "",
                  "| Done | Step | What it shows | Video file | Image file |", "|---|---|---|---|---|"]
        for s in m["steps"]:
            base = f"{mid}/{s['n']:02d}-{slug(s['text'])}"
            what = s["text"] if len(s["text"]) <= 70 else s["text"][:67].rstrip() + "..."
            lines.append(f"| [ ] | {s['id']} | {what.replace('|', '/')} | `{base}.mp4` | `{base}.webp` |")
    with open(rp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    """Run expansion, validation and file generation."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--overwrite-replace", action="store_true", help="rebuild media/replace.md (erases ticks)")
    args = ap.parse_args()
    scenarios, modules, conditions, _, errors = expand()
    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    write_generated(scenarios)
    write_catalog(scenarios, modules, conditions)
    write_media(scenarios, modules, args.overwrite_replace)
    print(f"OK: {len(scenarios)} scenarios, {len(modules)} modules, "
          f"{sum(len(m['steps']) for m in modules.values())} steps")


if __name__ == "__main__":
    main()
