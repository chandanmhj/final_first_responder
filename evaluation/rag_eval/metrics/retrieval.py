"""Retrieval metrics for one question: recall@k, reciprocal rank and nDCG@k (binary relevance)."""
import math


def recall_at_k(ranked, gold, k):
    return len(set(ranked[:k]) & set(gold)) / max(len(gold), 1)


def reciprocal_rank(ranked, gold):
    for i, c in enumerate(ranked, 1):
        if c in gold:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked, gold, k):
    dcg = sum(1.0 / math.log2(i + 1) for i, c in enumerate(ranked[:k], 1) if c in gold)
    ideal = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(gold), k) + 1))
    return dcg / ideal if ideal else 0.0
