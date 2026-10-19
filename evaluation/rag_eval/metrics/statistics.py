"""Bootstrap confidence interval and a paired bootstrap difference test."""
import numpy as np


def bootstrap_ci(values, n=2000, alpha=0.05, seed=0):
    v = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = [rng.choice(v, len(v)).mean() for _ in range(n)]
    return float(v.mean()), float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))


def paired_bootstrap_p(a, b, n=2000, seed=0):
    """Share of resamples where system A is not better than B (small = A better)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(a), (n, len(a)))
    return float(((a[idx] - b[idx]).mean(axis=1) <= 0).mean())
