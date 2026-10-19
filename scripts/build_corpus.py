"""Build the RAG corpus (JSONL) from the IFRC guidelines PDF and the scenario modules.

Outputs (in data/guidelines/processed/):
    ifrc_chunks.jsonl     chunks of the IFRC International First Aid, Resuscitation and Education Guidelines 2025
    module_chunks.jsonl   one chunk per scenario module (handbook-based, IFRC-based or authored steps)

Usage:
    python scripts/build_corpus.py --ifrc data/guidelines/raw/ifrc_2025.pdf
    python scripts/build_corpus.py --text /path/to/ifrc.txt     # pre-extracted text (pages split by form feed)

PDF text extraction uses PyMuPDF if installed, otherwise the `pdftotext` command (poppler).
"""
import argparse
import glob
import json
import os
import re
import subprocess

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "guidelines", "processed")
SC = os.path.join(ROOT, "data", "scenarios")

FIRST_TOPIC_PAGE, LAST_TOPIC_PAGE = 113, 522
NAME_FIXES = {
    196: "Unresponsive and abnormal breathing with defibrillator available",
    208: "Unresponsive and abnormal breathing with opioid overdose",
}
RESTRICTED = {"Suicidal ideation", "Acute grief", "Traumatic event"}
HEADINGS = {"Key action", "Introduction", "Guidelines", "Good practice points", "Chain of survival behaviours",
            "First aid steps", "Local adaptation", "Access help", "Special cases", "CAUTION", "Prevent and prepare",
            "Early recognition", "Recovery"}
STOP = {"Education considerations", "Scientific foundation", "Education review", "Context considerations",
        "Learner considerations", "Learning connections", "Facilitation tips", "Facilitation tools"}
MAX_CHARS = 900


def extract_pages(pdf_path=None, text_path=None):
    """Return a list of page texts (index 0 is page 1)."""
    if text_path:
        return open(text_path, encoding="utf-8").read().split("\f")
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        return [p.get_text() for p in doc]
    except ImportError:
        out = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True, check=True).stdout
        return out.split("\f")


def clean(s):
    """Remove page furniture and odd characters."""
    s = s.replace("\u200b", "").replace("⚙️", "")
    s = re.sub(r"International first aid, resuscitation and education guidelines 2025", "", s)
    s = re.sub(r"FIRST AID\s*\|\s*\d+", "", s)
    s = re.sub(r"^\s*\d+\s*\|\s*", "", s, flags=re.M)
    s = re.sub(r"[ \t]+", " ", s)
    return s


def detect_topics(pages):
    """Find topic start pages: pages whose opening text contains 'Key action'."""
    topics = []
    for i, p in enumerate(pages, 1):
        if i < FIRST_TOPIC_PAGE or i > LAST_TOPIC_PAGE:
            continue
        head = p[:900]
        if "Key action" not in head:
            continue
        before = head.split("Key action")[0]
        lines = [l.strip() for l in before.split("\n") if l.strip()]
        lines = [l for l in lines if not re.search(r"international first aid|^\d+\s*\|?$|^FIRST AID|\|", l, re.I) and len(l) > 2]
        name = NAME_FIXES.get(i) or (lines[-1] if lines else f"Topic {i}")
        topics.append((i, name))
    return topics


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def _hard_split(text, limit=1400):
    """Split an over-long chunk on sentence boundaries."""
    if len(text) <= limit:
        return [text]
    out, cur = [], ""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if len(cur) + len(sent) > limit and cur:
            out.append(cur.strip())
            cur = ""
        cur += sent + " "
    if cur.strip():
        out.append(cur.strip())
    return out


def topic_chunks(pages, start, end, name):
    """Split one topic into section-aware chunks of at most MAX_CHARS characters."""
    section, buf, buf_page, chunks = "Overview", [], start, []
    stop = False

    def flush():
        nonlocal buf
        text = "\n".join(buf).strip()
        buf = []
        if len(text) < 40:
            return
        parts, cur = [], ""
        for para in re.split(r"\n(?= ?[●•○]|\s*\d+\.\s)", text):
            if len(cur) + len(para) > MAX_CHARS and cur:
                parts.append(cur.strip())
                cur = ""
            cur += para + "\n"
        if cur.strip():
            parts.append(cur.strip())
        for part in parts:
            for piece in _hard_split(part):
                chunks.append({"section": section, "page": buf_page, "text": piece})

    for pn in range(start, end):
        for line in clean(pages[pn - 1]).split("\n"):
            l = line.strip()
            if not l:
                continue
            if l in STOP:
                flush()
                stop = True
                break
            if l in HEADINGS:
                flush()
                section, buf_page = l, pn
                continue
            if not buf:
                buf_page = pn
            buf.append(l)
        if stop:
            break
    flush()
    return chunks


def build_ifrc(pages):
    topics = detect_topics(pages)
    rows = []
    for idx, (start, name) in enumerate(topics):
        end = topics[idx + 1][0] if idx + 1 < len(topics) else LAST_TOPIC_PAGE + 1
        for n, c in enumerate(topic_chunks(pages, start, end, name)):
            rows.append({
                "id": f"ifrc:{slug(name)}:{n:03d}",
                "source": "ifrc",
                "doc": "IFRC International First Aid, Resuscitation and Education Guidelines 2025",
                "topic": name,
                "section": c["section"],
                "page": c["page"],
                "text": f"{name} - {c['section']}\n{c['text']}",
                "restricted": name in RESTRICTED,
                "conditions": [],
                "module_id": None,
            })
    return rows


def build_modules():
    conds = yaml.safe_load(open(os.path.join(SC, "conditions.yaml")))["conditions"]
    used_by = {}
    for cid, c in conds.items():
        for m in c["modules"]:
            used_by.setdefault(m, []).append(cid)
    rows = []
    for path in sorted(glob.glob(os.path.join(SC, "modules", "*.yaml"))):
        m = yaml.safe_load(open(path, encoding="utf-8"))
        lines, sources, pages_ = [m["title"] + ":"], set(), []
        for s in m["steps"]:
            if "B" not in s["roles"] and "R" not in s["roles"]:
                continue
            tag = " (responders)" if s["roles"] == ["R"] else ""
            lines.append(f"{s['n']}. {s['text']}{tag}")
            sources.add(s["source"])
            if s.get("page"):
                pages_.append(str(s["page"]))
        src = "handbook" if "handbook" in sources else ("ifrc" if "ifrc" in sources else "authored")
        rows.append({
            "id": f"module:{m['id']}",
            "source": src,
            "doc": "Scenario module",
            "topic": m["title"],
            "section": "Steps",
            "page": ", ".join(sorted(set(pages_)))[:60] or None,
            "text": "\n".join(lines),
            "restricted": False,
            "conditions": sorted(used_by.get(m["id"], [])),
            "module_id": m["id"],
            "step_sources": sorted(sources),
        })
    return rows


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ifrc", default=os.path.join(ROOT, "data", "guidelines", "raw", "ifrc_2025.pdf"))
    ap.add_argument("--text", default=None)
    args = ap.parse_args()
    if args.text or os.path.exists(args.ifrc):
        pages = extract_pages(args.ifrc, args.text)
        ifrc = build_ifrc(pages)
        write_jsonl(os.path.join(PROC, "ifrc_chunks.jsonl"), ifrc)
        print(f"IFRC chunks: {len(ifrc)} from {len(detect_topics(pages))} topics")
    else:
        print("IFRC PDF not found; skipped. Put it at data/guidelines/raw/ifrc_2025.pdf or pass --ifrc")
    mods = build_modules()
    write_jsonl(os.path.join(PROC, "module_chunks.jsonl"), mods)
    print(f"Module chunks: {len(mods)}")


if __name__ == "__main__":
    main()
