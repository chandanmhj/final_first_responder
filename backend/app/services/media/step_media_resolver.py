"""Find the video and image for a step, if they exist. Text-only is the fallback."""
import os

import yaml


class StepMediaResolver:
    """Reads media/manifest.yaml (status: missing | video | image | both) and builds public URLs."""

    def __init__(self, manifest_path: str, base_url: str):
        self.base = base_url.rstrip("/")
        self.entries: dict[str, dict] = {}
        if os.path.exists(manifest_path):
            for e in (yaml.safe_load(open(manifest_path, encoding="utf-8")) or {}).get("media", []):
                self.entries[e["step_id"]] = e

    def resolve(self, step_id: str) -> dict:
        """Return {'video': url|None, 'image': url|None}. Nothing is returned for steps without files."""
        e = self.entries.get(step_id)
        if not e or e.get("status", "missing") == "missing" or not self.base:
            return {"video": None, "image": None}
        st = e["status"]
        return {
            "video": f"{self.base}/{e['video']}" if st in ("video", "both") else None,
            "image": f"{self.base}/{e['image']}" if st in ("image", "both") else None,
        }
