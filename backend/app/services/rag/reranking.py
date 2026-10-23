"""Rerank retrieved passages with a cross-encoder (query and passage read together), with a cheap fallback."""
import math

from .retrieval import Chunk, Filters

SECTION_BONUS = {"First aid steps": 0.15, "Key action": 0.10, "Steps": 0.15, "Guidelines": 0.05}


class CrossEncoderReranker:
    """Local ONNX cross-encoder (fastembed). Loaded on first use; if it cannot load, callers fall back to the heuristic."""

    def __init__(self, model_name: str = "Xenova/ms-marco-MiniLM-L-6-v2"):
        self.model_name, self._model, self.failed = model_name, None, False

    def scores(self, query: str, texts: list[str]) -> list[float] | None:
        if self.failed or not texts:
            return None
        try:
            if self._model is None:
                from fastembed.rerank.cross_encoder import TextCrossEncoder  # heavy import, so lazy

                self._model = TextCrossEncoder(model_name=self.model_name)
            return [float(s) for s in self._model.rerank(query, texts)]
        except Exception:
            self.failed = True
            return None


def rerank(chunks: list[Chunk], query: str | None = None, reranker: CrossEncoderReranker | None = None,
           filters: Filters | None = None) -> list[Chunk]:
    """Reorder chunks best first.

    With a reranker: final = 0.7 * relevance (cross-encoder, 0..1) + 0.3 * retrieval score + small section/metadata bonuses.
    Without one (tests, offline): retrieval score with the section and metadata bonuses.
    """
    if not chunks:
        return []
    top = max(c.score for c in chunks) or 1.0
    ce = reranker.scores(query, [f"{c.topic}. {c.section}: {c.text}" for c in chunks]) if (reranker and query) else None
    for i, c in enumerate(chunks):
        prior = c.score / top
        bonus = SECTION_BONUS.get(c.section, 0.0) * 0.5 + (0.06 if filters and not filters.empty() and filters.match(c) else 0.0)
        if ce is not None:
            c.relevance = 1.0 / (1.0 + math.exp(-max(min(ce[i], 30.0), -30.0)))
            c.score = 0.7 * c.relevance + 0.3 * prior + bonus
        else:
            c.score = prior * (1.0 + SECTION_BONUS.get(c.section, 0.0)) + (bonus - SECTION_BONUS.get(c.section, 0.0) * 0.5)
    return sorted(chunks, key=lambda c: -c.score)