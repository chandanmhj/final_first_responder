"""Optional lightweight reranking: favour chunks of the active condition and first-aid steps."""
from .retrieval import Chunk

SECTION_BONUS = {"First aid steps": 1.15, "Key action": 1.1, "Steps": 1.15, "Guidelines": 1.05}


def rerank(chunks: list[Chunk]) -> list[Chunk]:
    """Reorder chunks using section type. Cheap, deterministic, measured in the evaluation notebooks."""
    for c in chunks:
        c.score *= SECTION_BONUS.get(c.section, 1.0)
    return sorted(chunks, key=lambda c: -c.score)
