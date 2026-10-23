"""Turn a message into search queries and metadata filters (fix spelling, resolve follow-ups, pick topics)."""
import re
from dataclasses import dataclass, field

from .generation import GroqClient

TYPOS = {"consiousness": "consciousness", "conciousness": "consciousness", "unconcious": "unconscious", "unconsious": "unconscious",
         "bleading": "bleeding", "breething": "breathing", "chocking": "choking", "siezure": "seizure", "seizer": "seizure", "drowing": "drowning"}
SYNONYMS = [("not responding", "unresponsive"), ("not responsive", "unresponsive"), ("passed out", "unconscious"), ("blacked out", "unconscious"),
            ("lost consciousness", "unconscious unresponsive"), ("not waking", "unresponsive"), ("can't breathe", "difficulty breathing")]
STOP = set("a an the and or of to in on for with is are was be it this that i my me we you your he she they them his her what how do does should can hazard adult child".split())


@dataclass
class Understood:
    """A cleaned search query, alternative phrasings, and knowledge-base topics to filter on."""

    query: str
    variants: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)


def normalize(text: str) -> str:
    """Lower-case, fix common misspellings, and add the medical term for common phrases."""
    t = text.lower()
    for bad, good in TYPOS.items():
        t = t.replace(bad, good)
    extra = [syn for phrase, syn in SYNONYMS if phrase in t]
    return " ".join([t.strip(), *extra]).strip()


def _stems(text: str) -> set[str]:
    return {w[:4] for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP and len(w) > 2}


def heuristic_topics(query: str, vocab: list[str]) -> list[str]:
    """Offline topic guess: topics whose title words appear in the query."""
    q = _stems(query)
    scored = []
    for t in vocab:
        ts = _stems(t)
        hit = len(q & ts)
        if ts and hit and hit / len(ts) >= 0.5:
            scored.append((hit / len(ts), t))
    scored.sort(key=lambda x: -x[0])
    return [t for _, t in scored[:2]]


def understand_query(llm: GroqClient, message: str, step_text: str | None = None, condition_title: str | None = None,
                     history: list[dict] | None = None, topics: list[str] | None = None, case: str | None = None) -> Understood:
    """Standalone query + up to 2 variants + up to 2 topics. Falls back to rules when no model is available."""
    topics = topics or []
    ctx = " ".join(x for x in [condition_title, step_text] if x)
    base = normalize(message)
    fallback_q = f"{base} {ctx}".strip() if ctx else base
    fb = Understood(fallback_q, [], heuristic_topics(fallback_q, topics))
    if not llm.ready:
        return fb
    recent = "\n".join(f"{h['role']}: {str(h['content'])[:200]}" for h in (history or [])[-8:])
    try:
        out = llm.chat_json([
            {"role": "system", "content": "You prepare searches over a first-aid knowledge base. Fix spelling, replace everyday words with the medical term "
                                          "(for example 'not responding' means unresponsive), and use the situation and recent chat to make follow-ups standalone. "
                                          "Return JSON: {\"query\": one short standalone search query, \"variants\": up to 2 alternative phrasings using different "
                                          "words, \"topics\": up to 2 topic names copied exactly from the list that the question is about, or []}.\n"
                                          f"Topics: {'; '.join(topics)}"},
            {"role": "user", "content": f"Case notes: {case or 'none'}\nSituation: {ctx or 'none'}\nRecent chat:\n{recent or 'none'}\nMessage: {message}"},
        ])
    except Exception:
        return fb
    q = str(out.get("query") or "").strip() or fallback_q
    variants = [str(v).strip() for v in (out.get("variants") or []) if str(v).strip()][:2]
    lower = {t.lower(): t for t in topics}
    picked = [lower[t.lower()] for t in (out.get("topics") or []) if isinstance(t, str) and t.lower() in lower][:2]
    return Understood(q, variants, picked or fb.topics)


def rewrite_query(llm: GroqClient, message: str, step_text: str | None, condition_title: str | None) -> str:
    """Older entry point: just the standalone query."""
    return understand_query(llm, message, step_text, condition_title).query