"""Source labels. Every step and every citation names the source its content really comes from."""
from .retrieval import Chunk

LABELS = {
    "ifrc": "IFRC International First Aid, Resuscitation and Education Guidelines 2025",
    "handbook": "BCLS Provider Handbook (RGUHS-JeevaRaksha Trust)",
    "authored": "General first-aid guidance (authored, not yet medically reviewed)",
}


def label(source: str, page: str | None = None) -> str:
    """Human-readable source label, with page when known."""
    base = LABELS.get(source, source)
    return f"{base}, p. {page}" if page else base


def from_chunks(chunks: list[Chunk], limit: int = 4) -> list[dict]:
    """Deduplicated citations for the chunks used in an answer."""
    seen, out = set(), []
    for c in chunks:
        key = (c.source, c.topic, c.page)
        if key in seen:
            continue
        seen.add(key)
        out.append({"source": c.source, "topic": c.topic, "page": c.page, "label": label(c.source, c.page)})
        if len(out) >= limit:
            break
    return out
