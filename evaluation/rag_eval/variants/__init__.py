"""Retrieval variants compared in the experiments. Each takes (retriever, question) and returns ranked chunk ids."""
from app.services.rag.reranking import rerank

from ..runner_utils import route_condition


def bm25(r, q):
    return [c.id for c in r.search(q, 10, mode="bm25")]


def dense(r, q):
    return [c.id for c in r.search(q, 10, mode="dense")]


def hybrid(r, q):
    return [c.id for c in r.search(q, 10, mode="hybrid")]


def hybrid_rerank(r, q):
    return [c.id for c in rerank(r.search(q, 10, mode="hybrid"))]


def scenario_aware(r, q):
    cond = route_condition(q)
    return [c.id for c in rerank(r.search(q, 10, condition=cond, mode="hybrid"))]


VARIANTS = {"bm25": bm25, "dense": dense, "hybrid": hybrid, "hybrid_rerank": hybrid_rerank, "scenario_aware": scenario_aware}
