"""Command line: python -m rag_eval.cli run [--variants bm25,hybrid] [--embeddings hash|fastembed] [--make-seed]"""
import argparse

from . import datasets, runner
from .reporting import figures, report_builder


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run"])
    ap.add_argument("--variants", default=None)
    ap.add_argument("--embeddings", default="hash")
    ap.add_argument("--make-seed", action="store_true")
    a = ap.parse_args()
    if a.make_seed:
        datasets.generate_seed()
    rows = runner.run(a.variants.split(",") if a.variants else None, embedding_provider=a.embeddings)
    print("saved", runner.save(rows))
    fig = figures.bar_with_ci(rows)
    print("figure", fig, "report", report_builder.build(rows, ["retrieval_mrr.png"]))


if __name__ == "__main__":
    main()
