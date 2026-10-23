"""Question answering: understand, retrieve (with metadata filters), rerank, abstain or answer, cite."""
import re
from dataclasses import dataclass, field

from . import citations
from .abstention import should_abstain
from .generation import GroqClient
from .prompting import build_messages
from .query_understanding import understand_query
from .reranking import CrossEncoderReranker, rerank
from .retrieval import Chunk, Filters

NO_ANSWER = ("I'm not sure about that from my guidelines. If someone is in danger, call 108 now. "
             "Otherwise please ask a doctor or a pharmacist.")
STRONG_RELEVANCE = 0.5  # a cross-encoder score this high means the passage really answers the question


def clean_answer(text: str) -> str:
    """The chat shows plain text, so remove markdown (bold, headings, stray or empty bullets) the model may still produce."""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    t = re.sub(r"(?m)^\s*[*\-•]\s*$", "", t)
    t = re.sub(r"(?m)^\s*[*\-]\s+", "• ", t)
    t = re.sub(r"(?m)^#{1,6}\s*", "", t)
    t = t.replace("*", "")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def clip(text: str, max_lines: int = 6, max_chars: int = 650) -> str:
    """Hard limit so a reply can never turn into a full walkthrough."""
    t = "\n".join([ln for ln in text.split("\n") if ln.strip()][:max_lines])
    if len(t) > max_chars:
        cut = t[:max_chars]
        k = max(cut.rfind(". "), cut.rfind("\n"))
        t = cut[: k + 1] if k > 200 else cut
    return t.rstrip()


@dataclass
class RagAnswer:
    text: str
    citations: list[dict] = field(default_factory=list)
    abstained: bool = False
    chunks: list[Chunk] = field(default_factory=list)


def _merge(lists: list[list[Chunk]]) -> dict[str, Chunk]:
    """Union of result lists; a passage found more than once gets a small boost."""
    merged: dict[str, Chunk] = {}
    for res in lists:
        for c in res:
            if c.id not in merged:
                merged[c.id] = c
            else:
                keep = merged[c.id]
                keep.score = max(keep.score, c.score) * 1.1
    return merged


class RagPipeline:
    """Grounded answers over the IFRC and handbook knowledge base."""

    def __init__(self, retriever, llm: GroqClient, top_k: int = 6, min_overlap: float = 0.12,
                 reranker: CrossEncoderReranker | None = None, pool: int = 20):
        self.retriever, self.llm, self.top_k, self.min_overlap = retriever, llm, top_k, min_overlap
        self.reranker, self.pool = reranker, max(pool, top_k)

    def retrieve(self, query: str, condition: str | None = None, variants: list[str] | tuple = (), topics: list[str] | tuple = ()) -> list[Chunk]:
        """Wide candidate pool (filtered by topic/condition, plus unfiltered for coverage), then rerank and keep top_k."""
        flt = Filters(topics=list(topics), conditions=[condition] if condition else [])
        lists = []
        if not flt.empty():
            lists.append(self.retriever.search(query, k=self.pool, condition=condition, filters=flt))
        for q in [query, *list(variants)[:2]]:
            lists.append(self.retriever.search(q, k=self.pool, condition=condition))
        cands = sorted(_merge(lists).values(), key=lambda c: -c.score)[: self.pool * 2]
        return rerank(cands, query, self.reranker, flt)[: self.top_k]

    def answer(self, question: str, *, condition: str | None = None, condition_title: str | None = None,
               step_text: str | None = None, style: str = "simple", history: list[dict] | None = None,
               case_context: str | None = None) -> RagAnswer:
        """Answer from the sources, or abstain when they do not cover the question."""
        known = self.retriever.known_topics() if hasattr(self.retriever, "known_topics") else []
        u = understand_query(self.llm, question, step_text, condition_title, history, known, case_context)
        chunks = self.retrieve(u.query, condition, u.variants, u.topics)
        strong = any((c.relevance or 0.0) >= STRONG_RELEVANCE for c in chunks)
        if not strong and should_abstain(chunks, self.min_overlap):
            return RagAnswer(NO_ANSWER, [], True, chunks)
        if not self.llm.ready:  # development without an API key: show the best passage
            top = chunks[0]
            return RagAnswer(top.text.split("\n", 1)[-1][:700], citations.from_chunks(chunks[:2]), False, chunks)
        msgs = build_messages(question, chunks, style, step_text, history, case_context)
        text = clip(clean_answer(self.llm.chat(msgs, temperature=0.1, max_tokens=500)))
        return RagAnswer(text or NO_ANSWER, citations.from_chunks(chunks), not text, chunks)