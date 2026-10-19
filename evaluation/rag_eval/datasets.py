"""Evaluation questions: load, and generate a seed set from the scenario modules.

The generated seed set is only a smoke test (templated questions, gold = the module's chunk). Real results need a reviewed
set: expand it with an LLM or by hand, have a medical reviewer check gold answers, and freeze data/eval/test.
"""
import glob
import json
import os
import random

import yaml

from .config import DATA

TEMPLATES = ["Someone near me has {t}. What should I do?", "How do I help with {t}?", "{t} first aid steps", "What should I not do for {t}?"]


def generate_seed(path=None, seed=7):
    """Write data/eval/dev/seed_questions.jsonl from the module titles."""
    rng = random.Random(seed)
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA, "scenarios", "modules", "*.yaml"))):
        m = yaml.safe_load(open(f, encoding="utf-8"))
        if m["id"] in ("call_for_help", "scene_safety", "safe_transfer", "primary_assessment") or m["id"].startswith("hazard_"):
            continue
        for t in rng.sample(TEMPLATES, 3):
            rows.append({"id": f"seed-{m['id']}-{len(rows)}", "question": t.format(t=m["title"].lower()), "gold_chunks": [f"module:{m['id']}"],
                         "scenario": m["id"], "status": "seed_unreviewed"})
    path = path or os.path.join(DATA, "eval", "dev", "seed_questions.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return rows


def load(path=None):
    path = path or os.path.join(DATA, "eval", "dev", "seed_questions.jsonl")
    return [json.loads(l) for l in open(path, encoding="utf-8")]
