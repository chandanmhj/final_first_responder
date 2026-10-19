"""Embed the corpus chunks and upload them to Supabase (table knowledge_chunks).

Prerequisites: run scripts/build_corpus.py first, apply supabase/migrations, and set SUPABASE_URL and
SUPABASE_SERVICE_ROLE_KEY (and optionally EMBEDDING_PROVIDER / EMBEDDING_MODEL) in .env.

Usage:
    python scripts/build_knowledge_base.py --dry-run     # count chunks and test embeddings only
    python scripts/build_knowledge_base.py               # upload
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "backend"))

from app.config import Settings  # noqa: E402
from app.services.rag.embeddings import get_embedder  # noqa: E402

PROC = os.path.join(ROOT, "data", "guidelines", "processed")


def read_rows():
    rows = []
    for fn in ("module_chunks.jsonl", "ifrc_chunks.jsonl"):
        path = os.path.join(PROC, fn)
        if os.path.exists(path):
            rows += [json.loads(l) for l in open(path, encoding="utf-8")]
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch", type=int, default=32)
    args = ap.parse_args()
    s = Settings()
    rows = read_rows()
    print(f"{len(rows)} chunks")
    embedder = get_embedder(s)
    if args.dry_run:
        v = embedder.embed([rows[0]["text"]])
        print("embedding shape", v.shape)
        return
    from app.db.repositories import make_supabase_client

    client = make_supabase_client(s.supabase_url, s.supabase_service_role_key)
    for i in range(0, len(rows), args.batch):
        part = rows[i:i + args.batch]
        vecs = embedder.embed([r["text"] for r in part])
        payload = [{
            "id": r["id"], "source": r["source"], "doc": r.get("doc"), "topic": r.get("topic"), "section": r.get("section"),
            "page": str(r["page"]) if r.get("page") else None, "module_id": r.get("module_id"), "conditions": r.get("conditions", []),
            "text": r["text"], "restricted": bool(r.get("restricted")), "embedding": vecs[j].tolist(),
        } for j, r in enumerate(part)]
        client.table("knowledge_chunks").upsert(payload).execute()
        print(f"uploaded {min(i + args.batch, len(rows))}/{len(rows)}")


if __name__ == "__main__":
    main()
