"""Load the cleaned hospital list and find suitable hospitals near a point."""
import json
import math
import os
from urllib.parse import quote

import yaml

from .facility_matching import rank


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


class HospitalIndex:
    """Hospital list plus matching rules."""

    def __init__(self, data_dir: str):
        bases = [os.path.join(data_dir, "hospitals"), os.path.join(data_dir, "guidelines", "processed", "hospitals")]
        base = next((b for b in bases if os.path.exists(os.path.join(b, "hospitals_clean.json"))), bases[0])
        path = os.path.join(base, "hospitals_clean.json")
        self.hospitals = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else []
        req = os.path.join(base, "emergency_requirements.yaml")
        self.requirements = yaml.safe_load(open(req, encoding="utf-8")) if os.path.exists(req) else {"default": {}, "conditions": {}, "status_rank": {}}

    def nearby(self, lat: float, lon: float, condition: str | None = None, limit: int = 5, max_km: float = 40.0) -> dict:
        """Ranked hospitals near the point (tier chosen by the emergency type), widening the search if none are close."""
        scored = []
        for h in self.hospitals:
            d = haversine_km(lat, lon, h["lat"], h["lon"])
            if d <= max_km:
                scored.append((h, d))
        results = rank(scored, self.requirements, condition)[:limit]
        if not results and max_km < 600:
            return self.nearby(lat, lon, condition, limit, 600.0)
        for r in results:
            r["directions_url"] = f"https://www.google.com/maps/dir/?api=1&destination={r['lat']},{r['lon']}"
            r["call_url"] = f"tel:{quote(r['phones'][0])}" if r.get("phones") else None
        message = None if results else "No suitable hospital was found near this location in the loaded data. Call 108."
        return {"results": results, "message": message, "condition": condition}