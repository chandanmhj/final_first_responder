"""Question answering: retrieve, rerank, abstain or answer, cite."""
from dataclasses import dataclass, field

from . import citations
from .abstention import should_abstain
from .generation import GroqClient
from .prompting import build_messages
from .query_understanding import rewrite_query
from .reranking import rerank
from .retrieval import Chunk

NO_ANSWER = ("I'm not sure about that from my guidelines. If someone is in danger, call 108 now. "
             "Otherwise please ask a doctor or a pharmacist.")


@dataclass
class RagAnswer:
    text: str
    citations: list[dict] = field(default_factory=list)
    abstained: bool = False
    chunks: list[Chunk] = field(default_factory=list)


class RagPipeline:
    """Grounded answers over the IFRC and handbook knowledge base."""

    def __init__(self, retriever, llm: GroqClient, top_k: int = 6, min_overlap: float = 0.12):
        self.retriever, self.llm, self.top_k, self.min_overlap = retriever, llm, top_k, min_overlap

    def retrieve(self, query: str, condition: str | None = None) -> list[Chunk]:
        return rerank(self.retriever.search(query, k=self.top_k, condition=condition))

    def answer(self, question: str, *, condition: str | None = None, condition_title: str | None = None,
               step_text: str | None = None, style: str = "simple", history: list[dict] | None = None) -> RagAnswer:
        """Answer from the sources, or abstain when they do not cover the question."""
        query = rewrite_query(self.llm, question, step_text, condition_title)
        chunks = self.retrieve(query, condition)
        if should_abstain(chunks, self.min_overlap):
            return RagAnswer(NO_ANSWER, [], True, chunks)
        if not self.llm.ready:  # development without an API key: show the best passage
            top = chunks[0]
            return RagAnswer(top.text.split("\n", 1)[-1][:700], citations.from_chunks(chunks[:2]), False, chunks)
        msgs = build_messages(question, chunks, style, step_text, history)
        text = self.llm.chat(msgs, temperature=0.1, max_tokens=500).strip()
        return RagAnswer(text or NO_ANSWER, citations.from_chunks(chunks), not text, chunks)
