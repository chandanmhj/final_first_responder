"""Hybrid retrieval over the guideline corpus (BM25 + dense vectors, fused with reciprocal rank fusion)."""
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

    def search(self, query: str, k: int = 6, condition: str | None = None, mode: str = "hybrid") -> list[Chunk]:
        """Return the top-k chunks. mode: bm25 | dense | hybrid."""
        if not self.chunks:
            return []
        q_tokens = tokenize(query)
        n = len(self.chunks)
        ranks: dict[int, float] = {}
        if mode in ("bm25", "hybrid") and self.bm25:
            sc = self.bm25.get_scores(q_tokens)
            for r, i in enumerate(np.argsort(-sc)[:50]):
                ranks[int(i)] = ranks.get(int(i), 0.0) + 1.0 / (60 + r)
        if mode in ("dense", "hybrid") and self.matrix is not None:
            qv = self.embedder.embed([query])[0]
            sims = self.matrix @ qv
            for r, i in enumerate(np.argsort(-sims)[:50]):
                ranks[int(i)] = ranks.get(int(i), 0.0) + 1.0 / (60 + r)
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
        self.client, self.embedder = client, embedder

    def search(self, query: str, k: int = 6, condition: str | None = None, mode: str = "hybrid") -> list[Chunk]:
        qv = self.embedder.embed([query])[0].tolist()
        rows = self.client.rpc("match_chunks_hybrid", {"query_text": query, "query_embedding": qv, "match_count": k * 2,
                                                          "condition_filter": condition}).execute().data or []
        qset = set(tokenize(query))
        out = []
        for r in rows:
            c = Chunk(r["id"], r["source"], r["topic"], r["section"], str(r["page"]) if r.get("page") else None, r["text"],
                      r.get("doc", ""), r.get("conditions") or [], r.get("module_id"))
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
