"""Run variants over a question set and save per-question results."""
import csv
import os
import time

from app.config import Settings
from app.services.rag.embeddings import get_embedder
from app.services.rag.retrieval import InMemoryRetriever, load_chunks

from . import datasets
from .config import DATA, OUT_RESULTS
from .metrics.retrieval import ndcg_at_k, recall_at_k, reciprocal_rank
from .variants import VARIANTS


def run(variant_names=None, questions=None, embedding_provider="hash", k=5):
    """Return a list of per-question result dicts. Use embedding_provider='fastembed' for real dense retrieval."""
    s = Settings(embedding_provider=embedding_provider, data_dir=DATA)
    retriever = InMemoryRetriever(load_chunks(DATA), get_embedder(s))
    qs = questions or datasets.load()
    rows = []
    for name in variant_names or list(VARIANTS):
        fn = VARIANTS[name]
        for q in qs:
            t0 = time.perf_counter()
            ranked = fn(retriever, q["question"])
            ms = (time.perf_counter() - t0) * 1000
            g = q["gold_chunks"]
            rows.append({"variant": name, "id": q["id"], "scenario": q.get("scenario", ""), f"recall@{k}": recall_at_k(ranked, g, k),
                         "mrr": reciprocal_rank(ranked, g), f"ndcg@{k}": ndcg_at_k(ranked, g, k), "latency_ms": ms})
    return rows


def save(rows, name="retrieval_results.csv"):
    os.makedirs(OUT_RESULTS, exist_ok=True)
    path = os.path.join(OUT_RESULTS, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path
