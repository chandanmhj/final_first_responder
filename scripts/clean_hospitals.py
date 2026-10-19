"""Clean a scraped hospital list and write the dataset the backend uses.

Input  : data/hospitals/raw/ambulance_hospitals.json   (a JSON list; save your scraped file here)
Output : data/hospitals/hospitals_clean.json           (used by the API)
         data/hospitals/excluded.json                  (rows dropped, with the reason)
         data/hospitals/CLEANING_REPORT.md             (counts and what changed)

Input record fields: name, lat, lon, type (primary/secondary/tertiary), specialties[], emergency (yes/no/unknown),
operator_type, phone.

What it does:
  1. Drops rows that are not places to get emergency or urgent care (pharmacies, labs, dental, skin/hair/aesthetic,
     opticians, schools, alternative-medicine centres, wellness and similar).
  2. Classifies each row as hospital, nursing_home, clinic or eye_hospital.
  3. Fixes the tier: a clinic is always 'primary'; 'tertiary' is kept only for hospitals.
  4. Computes emergency_status: confirmed / probable / unlikely / specialty_only.
  5. Merges duplicates (same or near-identical name within 150 m).
  6. Cleans phone numbers.
  7. Adds capabilities inferred from names and specialties, then applies data/hospitals/capability_overrides.yaml.

Usage:
    python scripts/clean_hospitals.py
    python scripts/clean_hospitals.py --input my.json --output out.json
"""
import argparse
import difflib
import json
import math
import os
import re
from collections import Counter

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSP = os.path.join(ROOT, "data", "hospitals")

NON_MEDICAL = [
    r"\bpharm", r"medical shop", r"medicals?\b", r"\boptic", r"kirana", r"\bschool\b", r"\bhigh school", r"kaya skin", r"skin\b.*\bclinic",
    r"\bhair\b", r"trichology", r"cosmet", r"laser", r"aesthetic", r"derma", r"dermalogica", r"skinsi", r"toothsi", r"happy tooth",
    r"\bdent", r"\btooth", r"smile", r"orthodont", r"amplifon", r"hearing", r"speech", r"hurbz", r"wellness", r"sugar\.?fit",
    r"ancient china", r"touchwood", r"garbha gudi", r"femlife", r"fertil", r"test tube", r"ivf", r"surrogacy", r"\bspa\b", r"yoga",
    r"hydrotherapy", r"physio", r"rehab", r"occupational therapy", r"ayur", r"aarogya\b", r"homeo", r"homoeo", r"unani", r"nature ?cure",
    r"naturopath", r"acupuncture", r"hijama", r"piles", r"fistula", r"kidney stone", r"\bnu trust\b", r"sparkle", r"just smiles",
    r"vitiligo", r"psoriasis", r"hair loss", r"men's health", r"obesity", r"diabet(e|i)[a-z]* (centre|center|clinic)", r"counsel",
    r"astha centre", r"autism", r"cadabam", r"oncquest", r"metropolis", r"medall", r"thyrocare", r"path ?labs?", r"lal path",
    r"\blabs?\b", r"laborator", r"diagnostic", r"\bscan", r"x-?ray", r"radiolog", r"clinrad", r"blood bank", r"pharmeasy",
    r"orange health", r"aster labs", r"telerad", r"hear2speak", r"tibetan healing", r"healing hands", r"\bgeronics\b",
    r"karunashraya", r"turning point", r"pristyn", r"kasper multi", r"holistic", r"my dentist", r"the local dentist",
]
EYE = [r"\beye\b", r"netra", r"nethra", r"netral", r"nethral", r"ophthalm", r"vision", r"retina", r"lasik", r"vasan eye", r"agarwal"]
ENT_ONLY = [r"\bent\b.*(clinic|centre|center)", r"hearing"]
HOSPITAL = [r"hospital", r"hospitals", r"medical college", r"institute", r"trauma", r"nursing home", r"multi ?speciality", r"super ?speciality",
            r"medical centre", r"medical center", r"health ?care global", r"\bhcg\b", r"referral", r"general hospital", r"maternity home", r"nimhans", r"emergency", r"medical sciences"]
CLINIC = [r"clinic", r"polyclinic", r"poly clinic", r"dispensary", r"health cent", r"\bphc\b", r"\buphc\b", r"centre", r"center", r"doctor", r"\bdr\.? "]
MATERNITY = [r"maternity", r"women", r"cradle", r"cloud ?nine", r"motherhood", r"birth", r"nursing and maternity"]

CAP_RULES = {
    "cardiac": [r"cardio", r"heart", r"jayadeva", r"cardiac"],
    "neuro": [r"neuro", r"nimhans", r"brain", r"stroke"],
    "trauma": [r"trauma", r"accident", r"emergency block"],
    "orthopaedic": [r"ortho", r"hosmat", r"bone", r"spine"],
    "paediatric": [r"child", r"paediatric", r"pediatric", r"kids", r"rainbow", r"cradle"],
    "maternity": MATERNITY,
    "oncology": [r"cancer", r"onco", r"kidwai", r"hcg"],
    "eye": EYE,
    "psychiatric": [r"nimhans", r"mental", r"psychiatr"],
    "burns": [r"burn"],
    "kidney": [r"nephro", r"kidney", r"dialysis", r"urolog"],
}
SPECIALTY_MAP = {"cardiology": "cardiac", "neurology": "neuro", "orthopedic": "orthopaedic", "pediatric": "paediatric", "maternity": "maternity",
                 "oncology": "oncology", "ophthalmology": "eye", "psychiatric": "psychiatric", "nephrology_urology": "kidney"}


def has(patterns, text):
    return any(re.search(p, text, re.I) for p in patterns)


def haversine_km(a_lat, a_lon, b_lat, b_lon):
    r = 6371.0088
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dphi, dl = p2 - p1, math.radians(b_lon - a_lon)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def norm_name(name):
    n = re.sub(r"\(.*?\)", " ", name.lower())
    n = re.sub(r",.*$", "", n)
    n = re.sub(r"\b(bengaluru|bangalore|urban|rural|pvt|ltd|private|limited|the|a unit of)\b", " ", n)
    return re.sub(r"[^a-z0-9]+", " ", n).strip()


def clean_phone(raw):
    if not raw:
        return []
    out = []
    for part in re.split(r"[;,/]", str(raw).replace('"', "")):
        digits = re.sub(r"[^\d+]", "", part)
        if len(re.sub(r"\D", "", digits)) >= 8:
            out.append(re.sub(r"\s+", " ", part.strip()))
    return list(dict.fromkeys(out))


def classify(rec):
    """Return (class, reason_if_excluded)."""
    name = rec["name"]
    spec = rec.get("specialties") or []
    if has(NON_MEDICAL, name) and not has([r"hospital", r"trauma", r"nursing home", r"medical college", r"institute"], name):
        return None, "not an emergency-care facility (pharmacy, lab, dental, aesthetic, wellness or similar)"
    if has(EYE, name) or spec == ["ophthalmology"]:
        return "eye_hospital", None
    if has([r"nursing home"], name):
        return "nursing_home", None
    if has(HOSPITAL, name):
        return "hospital", None
    if rec.get("type") in ("secondary", "tertiary") and (rec.get("emergency") or "").lower() == "yes" \
            and not has([r"clinic", r"polyclinic", r"dispensary", r"centre", r"center"], name):
        return "hospital", None  # named like a hospital brand (e.g. Cloud Nine) and flagged as an emergency-capable higher tier
    return "clinic", None


def infer_capabilities(rec, cls):
    caps = set()
    text = rec["name"]
    for cap, pats in CAP_RULES.items():
        if has(pats, text):
            caps.add(cap)
    for s in rec.get("specialties") or []:
        if s in SPECIALTY_MAP:
            caps.add(SPECIALTY_MAP[s])
    return sorted(caps)


SPECIALTY_ONLY = {"maternity", "oncology", "kidney", "psychiatric", "paediatric", "eye"}


def scope_of(caps, cls):
    """'specialty' when the facility only treats one specialty (eye, cancer, maternity...), otherwise 'general'."""
    if cls == "eye_hospital":
        return "specialty"
    if caps and set(caps) <= SPECIALTY_ONLY:
        return "specialty"
    return "general"


def emergency_status(rec, cls, caps):
    raw = (rec.get("emergency") or "unknown").lower()
    tier = rec.get("type", "primary")
    if cls == "eye_hospital":
        return "specialty_only"
    if cls == "clinic":
        return "unlikely"
    if raw == "yes" and cls in ("hospital", "nursing_home"):
        return "confirmed"
    if raw == "no":
        return "unlikely"
    if cls == "hospital" and tier in ("secondary", "tertiary"):
        return "probable"
    return "unlikely"


def merge_duplicates(rows):
    """Merge rows with the same or near-identical name within 150 m."""
    kept = []
    dropped = []
    for r in rows:
        match = None
        for k in kept:
            if haversine_km(r["lat"], r["lon"], k["lat"], k["lon"]) > 0.15:
                continue
            a, b = norm_name(r["name"]), norm_name(k["name"])
            if a == b or difflib.SequenceMatcher(None, a, b).ratio() >= 0.88:
                match = k
                break
        if not match:
            kept.append(r)
            continue
        rank = {"confirmed": 3, "probable": 2, "specialty_only": 1, "unlikely": 0}
        if rank[r["emergency_status"]] > rank[match["emergency_status"]]:
            match["emergency_status"] = r["emergency_status"]
        match["phones"] = list(dict.fromkeys(match["phones"] + r["phones"]))
        if match["tier"] == "primary" and r["tier"] != "primary":
            match["tier"] = r["tier"]
        match["capabilities"] = sorted(set(match["capabilities"]) | set(r["capabilities"]))
        match["scope"] = scope_of(match["capabilities"], match["class"])
        dropped.append({"name": r["name"], "reason": f"duplicate of '{match['name']}'"})
    return kept, dropped


def apply_overrides(rows, overrides):
    for r in rows:
        for o in overrides:
            if re.search(o["match"], r["name"], re.I):
                if "capabilities" in o:
                    r["capabilities"] = sorted(set(r["capabilities"]) | set(o["capabilities"]))
                if "emergency_status" in o:
                    r["emergency_status"] = o["emergency_status"]
                if "tier" in o:
                    r["tier"] = o["tier"]
                r["scope"] = scope_of(r["capabilities"], r["class"])
                r["verified"] = bool(o.get("verified", False))
                r["override_note"] = o.get("note", "")
    return rows


def clean(records, overrides):
    rows, excluded = [], []
    for rec in records:
        try:
            lat, lon = float(rec["lat"]), float(rec["lon"])
        except (KeyError, TypeError, ValueError):
            excluded.append({"name": rec.get("name"), "reason": "missing or invalid coordinates"})
            continue
        name = re.sub(r"\s+", " ", (rec.get("name") or "").strip())
        if not name or name.lower() in {"clinic", "hospital", "unknown clinic", "medical center", "health centre"} and not rec.get("phone"):
            excluded.append({"name": name or "(no name)", "reason": "generic or missing name"})
            continue
        rec = {**rec, "name": name}
        cls, why = classify(rec)
        if not cls:
            excluded.append({"name": name, "reason": why})
            continue
        caps = infer_capabilities(rec, cls)
        tier = rec.get("type", "primary")
        if cls in ("clinic",):
            tier = "primary"
        status = emergency_status(rec, cls, caps)
        rows.append({
            "name": name, "lat": round(lat, 6), "lon": round(lon, 6), "tier": tier, "class": cls,
            "specialties": rec.get("specialties") or [], "capabilities": caps,
            "emergency_raw": (rec.get("emergency") or "unknown").lower(), "emergency_status": status,
            "scope": scope_of(caps, cls),
            "operator_type": rec.get("operator_type") or "unknown", "phones": clean_phone(rec.get("phone")),
            "verified": False, "inferred_capabilities": True,
        })
    rows, dups = merge_duplicates(rows)
    excluded += dups
    rows = apply_overrides(rows, overrides)
    for i, r in enumerate(sorted(rows, key=lambda x: (x["lat"], x["lon"])), 1):
        r["id"] = f"h{i:05d}"
    return rows, excluded


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=os.path.join(HOSP, "raw", "ambulance_hospitals.json"))
    ap.add_argument("--output", default=os.path.join(HOSP, "hospitals_clean.json"))
    args = ap.parse_args()
    records = json.load(open(args.input, encoding="utf-8"))
    ov_path = os.path.join(HOSP, "capability_overrides.yaml")
    overrides = (yaml.safe_load(open(ov_path, encoding="utf-8")) or {}).get("overrides", []) if os.path.exists(ov_path) else []
    rows, excluded = clean(records, overrides)
    json.dump(rows, open(args.output, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(excluded, open(os.path.join(HOSP, "excluded.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    status = Counter(r["emergency_status"] for r in rows)
    reasons = Counter(re.sub(r"'.*'", "'...'", e["reason"]) for e in excluded)
    report = ["# Hospital cleaning report", "",
              f"- Input rows: {len(records)}", f"- Kept: {len(rows)}", f"- Excluded: {len(excluded)}", "",
              "## Emergency status of kept rows", ""] + [f"- {k}: {v}" for k, v in status.most_common()] + \
             ["", "## Why rows were excluded", ""] + [f"- {k}: {v}" for k, v in reasons.most_common()] + \
             ["", "Capabilities are inferred from names and specialties unless verified in capability_overrides.yaml."]
    open(os.path.join(HOSP, "CLEANING_REPORT.md"), "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(f"kept {len(rows)}, excluded {len(excluded)}")


if __name__ == "__main__":
    main()
