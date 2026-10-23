"""Hybrid retrieval over the guideline corpus (BM25 + dense vectors, fused with reciprocal rank fusion), with metadata filters."""
import json
import os
import re
from dataclasses import dataclass, field

import numpy as np

from ...config import Settings
from .embeddings import EmbeddingProvider

SOURCE_BOOST = {"handbook": 1.15, "ifrc": 1.0, "authored": 0.9}
STOP = set("a an the and or of to in on for with is are was be it this that i my me we you your he she they them his her what how do does should can".split())


@dataclass
class Chunk:
    """One retrievable passage."""

    id: str
    source: str
    topic: str
    section: str
    page: str | None
    text: str
    doc: str = ""
    conditions: list[str] = field(default_factory=list)
    module_id: str | None = None
    score: float = 0.0
    overlap: float = 0.0
    relevance: float | None = None  # cross-encoder score 0..1, set by the reranker


@dataclass
class Filters:
    """Metadata filter: a passage matches if its topic is listed OR it is tagged with a listed condition; sources must match if given."""

    topics: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)

    def empty(self) -> bool:
        return not (self.topics or self.conditions or self.sources)

    def match(self, c: "Chunk") -> bool:
        if self.sources and c.source not in self.sources:
            return False
        if self.topics or self.conditions:
            return c.topic.lower() in {t.lower() for t in self.topics} or bool(set(self.conditions) & set(c.conditions))
        return True


def tokenize(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


def load_chunks(data_dir: str) -> list[Chunk]:
    """Load processed JSONL chunk files. Restricted topics (for example suicide) are not retrievable."""
    out = []
    proc = os.path.join(data_dir, "guidelines", "processed")
    for fn in ("module_chunks.jsonl", "ifrc_chunks.jsonl"):
        path = os.path.join(proc, fn)
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            if r.get("restricted"):
                continue
            out.append(Chunk(r["id"], r["source"], r["topic"], r["section"], str(r["page"]) if r.get("page") else None,
                             r["text"], r.get("doc", ""), r.get("conditions", []), r.get("module_id")))
    return out


class InMemoryRetriever:
    """BM25 + dense retrieval in memory. Used for development, tests and the evaluation harness."""

    def __init__(self, chunks: list[Chunk], embedder: EmbeddingProvider, use_dense: bool = True):
        from rank_bm25 import BM25Okapi  # lazy import

        self.chunks, self.embedder, self.use_dense = chunks, embedder, use_dense
        self.bm25 = BM25Okapi([tokenize(c.text) for c in chunks]) if chunks else None
        self.matrix = embedder.embed([c.text for c in chunks]) if (chunks and use_dense) else None

    def known_topics(self) -> list[str]:
        return sorted({c.topic for c in self.chunks})

    @staticmethod
    def _top(scores, allowed: set[int] | None, n: int) -> list[int]:
        out: list[int] = []
        for i in np.argsort(-scores):
            if allowed is None or int(i) in allowed:
                out.append(int(i))
                if len(out) >= n:
                    break
        return out

    def search(self, query: str, k: int = 6, condition: str | None = None, mode: str = "hybrid",
               filters: Filters | None = None) -> list[Chunk]:
        """Return the top-k chunks. mode: bm25 | dense | hybrid. filters limits the search to matching metadata."""
        if not self.chunks:
            return []
        allowed = None
        if filters and not filters.empty():
            allowed = {i for i, c in enumerate(self.chunks) if filters.match(c)}
            if not allowed:
                return []
        depth = max(50, k * 3)
        q_tokens = tokenize(query)
        ranks: dict[int, float] = {}
        if mode in ("bm25", "hybrid") and self.bm25:
            sc = self.bm25.get_scores(q_tokens)
            for r, i in enumerate(self._top(sc, allowed, depth)):
                ranks[i] = ranks.get(i, 0.0) + 1.0 / (60 + r)
        if mode in ("dense", "hybrid") and self.matrix is not None:
            qv = self.embedder.embed([query])[0]
            sims = self.matrix @ qv
            for r, i in enumerate(self._top(sims, allowed, depth)):
                ranks[i] = ranks.get(i, 0.0) + 1.0 / (60 + r)
        scored = []
        qset = set(q_tokens)
        for i, base in ranks.items():
            c = self.chunks[i]
            score = base * SOURCE_BOOST.get(c.source, 1.0)
            if condition and condition in c.conditions:
                score *= 1.25
            ov = len(qset & set(tokenize(c.text))) / max(len(qset), 1)
            scored.append(Chunk(**{**c.__dict__, "score": score, "overlap": ov}))
        scored.sort(key=lambda c: -c.score)
        return scored[:k]


class SupabaseRetriever:
    """Hybrid search inside Postgres (pgvector + full text) through the match_chunks_hybrid function."""

    def __init__(self, client, embedder: EmbeddingProvider):
        self.client, self.embedder, self._topics = client, embedder, None

    def known_topics(self) -> list[str]:
        if self._topics is None:
            try:
                rows = self.client.table("knowledge_chunks").select("topic").eq("restricted", False).execute().data or []
                self._topics = sorted({r["topic"] for r in rows if r.get("topic")})
            except Exception:
                self._topics = []
        return self._topics

    def search(self, query: str, k: int = 6, condition: str | None = None, mode: str = "hybrid",
               filters: Filters | None = None) -> list[Chunk]:
        use_f = bool(filters and not filters.empty())
        qv = self.embedder.embed([query])[0].tolist()
        rows = self.client.rpc("match_chunks_hybrid", {"query_text": query, "query_embedding": qv, "match_count": max(k * 2, 60) if use_f else k * 2,
                                                          "condition_filter": condition}).execute().data or []
        qset = set(tokenize(query))
        out = []
        for r in rows:
            c = Chunk(r["id"], r["source"], r["topic"], r["section"], str(r["page"]) if r.get("page") else None, r["text"],
                      r.get("doc", ""), r.get("conditions") or [], r.get("module_id"))
            if use_f and not filters.match(c):  # the SQL function has no topic filter, so filter here
                continue
            c.score = float(r.get("score", 0)) * SOURCE_BOOST.get(c.source, 1.0)
            c.overlap = len(qset & set(tokenize(c.text))) / max(len(qset), 1)
            out.append(c)
        out.sort(key=lambda c: -c.score)
        return out[:k]


def build_retriever(settings: Settings, embedder: EmbeddingProvider, supabase_client=None):
    """Choose the retriever: Supabase when configured and requested, otherwise in memory."""
    use_sb = settings.retriever == "supabase" or (settings.retriever == "auto" and settings.supabase_ready and supabase_client is not None
                                                  and settings.env == "production")
    if use_sb and supabase_client is not None:
        return SupabaseRetriever(supabase_client, embedder)
    return InMemoryRetriever(load_chunks(settings.data_dir), embedder)