"""Figures saved to docs/evaluation/figures/."""
import os
from collections import defaultdict

from ..config import OUT_FIGURES
from ..metrics.statistics import bootstrap_ci


def bar_with_ci(rows, metric="mrr", name="retrieval_mrr.png"):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    by = defaultdict(list)
    for r in rows:
        by[r["variant"]].append(r[metric])
    names = list(by)
    stats = [bootstrap_ci(by[n]) for n in names]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar(names, [s[0] for s in stats], yerr=[[s[0] - s[1] for s in stats], [s[2] - s[0] for s in stats]], capsize=4, color="#2458e0")
    ax.set_ylabel(metric)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    os.makedirs(OUT_FIGURES, exist_ok=True)
    path = os.path.join(OUT_FIGURES, name)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
