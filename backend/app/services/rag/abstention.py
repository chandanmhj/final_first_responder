"""Decide when the system should say it does not know instead of guessing."""
from .retrieval import Chunk


def should_abstain(chunks: list[Chunk], min_overlap: float) -> bool:
    """True when nothing retrieved is related enough to the question."""
    if not chunks:
        return True
    return max(c.overlap for c in chunks) < min_overlap
