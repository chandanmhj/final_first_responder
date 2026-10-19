"""Prompts for grounded answers."""
from .retrieval import Chunk

SYSTEM = """You are First Responder, an emergency first-aid guide. Answer ONLY from the numbered sources provided.
Rules:
- If the sources do not answer the question, say you are not sure and tell the person to call 108 or see a doctor. Never guess.
- If sources disagree, follow the BCLS handbook sources first, then IFRC, then authored guidance.
- Never give medicine doses unless a source gives them and the reader is a certified first responder.
- Keep answers short and in steps. For anything life-threatening, start with: call 108.
- Do not diagnose. You support the person; you do not replace emergency services.
{style}"""

STYLE = {
    "simple": "Use plain everyday words and short sentences (reading level of a 12-year-old). Avoid medical jargon.",
    "clinical": "The reader is a certified first responder. Use precise clinical terminology.",
}


def build_messages(question: str, chunks: list[Chunk], style: str, step_context: str | None = None,
                   history: list[dict] | None = None) -> list[dict]:
    """Chat messages for a grounded answer."""
    srcs = "\n\n".join(f"[{i + 1}] ({c.source.upper()}: {c.topic}) {c.text}" for i, c in enumerate(chunks))
    ctx = f"\nThe person is currently on this step: {step_context}" if step_context else ""
    msgs = [{"role": "system", "content": SYSTEM.format(style=STYLE.get(style, STYLE['simple']))}]
    for h in (history or [])[-6:]:
        msgs.append({"role": h["role"], "content": h["content"]})
    msgs.append({"role": "user", "content": f"Sources:\n{srcs}\n{ctx}\n\nQuestion: {question}"})
    return msgs
