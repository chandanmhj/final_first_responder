"""Upload processed step media to the step-media bucket and update the media_assets table.

Put compressed files in media/processed/ using the names in media/replace.md, for example
media/processed/cpr_adult/04-lock-your-elbows-and-keep.mp4. Then run:  python scripts/upload_media_to_supabase.py
The bucket is public, so URLs are cached by the Supabase CDN. Use versioned file names when you replace a file.
"""
import mimetypes
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "backend"))

from app.config import Settings  # noqa: E402
from app.db.repositories import make_supabase_client  # noqa: E402


def main():
    s = Settings()
    manifest_path = os.path.join(ROOT, "media", "manifest.yaml")
    manifest = yaml.safe_load(open(manifest_path, encoding="utf-8"))
    client = make_supabase_client(s.supabase_url, s.supabase_service_role_key)
    changed = 0
    for e in manifest["media"]:
        has = {}
        for kind in ("video", "image"):
            rel = e[kind].replace("emergencies/", "", 1)
            local = os.path.join(ROOT, "media", "processed", rel)
            if os.path.exists(local):
                ctype = mimetypes.guess_type(local)[0] or "application/octet-stream"
                client.storage.from_("step-media").upload(e[kind], open(local, "rb").read(),
                                                          {"content-type": ctype, "upsert": "true", "cache-control": "31536000"})
                has[kind] = True
        status = "both" if len(has) == 2 else ("video" if has.get("video") else "image" if has.get("image") else "missing")
        if status != e["status"]:
            e["status"] = status
            changed += 1
        client.table("media_assets").upsert({"step_id": e["step_id"], "video_path": e["video"] if has.get("video") else None,
                                              "image_path": e["image"] if has.get("image") else None, "status": status}).execute()
    yaml.safe_dump(manifest, open(manifest_path, "w", encoding="utf-8"), sort_keys=False, allow_unicode=True, width=120)
    print(f"done, {changed} steps changed status")


if __name__ == "__main__":
    main()
