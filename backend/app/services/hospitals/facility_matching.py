"""Rank hospitals for an emergency using tier, emergency status, capabilities and distance."""


def _req(requirements: dict, condition: str | None) -> dict:
    default = requirements.get("default", {"min_status": "probable", "tiers": ["tertiary", "secondary", "primary"], "prefer": []})
    return {**default, **(requirements.get("conditions", {}).get(condition or "", {}))}


def rank(candidates: list[tuple[dict, float]], requirements: dict, condition: str | None) -> list[dict]:
    """Return hospital dicts (with distance and reasons) sorted best first.

    candidates: list of (hospital, distance_km). Hospitals below the minimum emergency status are dropped; if that leaves
    nothing, the minimum is relaxed one level so the user still gets an answer.
    """
    rank_of = requirements.get("status_rank") or {"confirmed": 3, "probable": 2, "specialty_only": 1, "unlikely": 0}
    req = _req(requirements, condition)
    need = rank_of.get(req.get("min_status", "probable"), 2)
    prefer = set(req.get("prefer", []))
    tiers = req.get("tiers", ["tertiary", "secondary", "primary"])

    def build(min_rank: int) -> list[dict]:
        out = []
        for h, d in candidates:
            if rank_of.get(h["emergency_status"], 0) < min_rank:
                continue
            caps = set(h.get("capabilities", []))
            if h.get("scope") == "specialty" and not (caps & prefer):
                continue
            if h["tier"] not in tiers:
                continue
            tier_score = len(tiers) - tiers.index(h["tier"])
            matched = sorted(caps & prefer)
            cap_bonus = sum(2.0 * (1.5 if h.get("verified") else 1.0) for _ in matched)
            status_bonus = {"confirmed": 1.5, "probable": 0.5}.get(h["emergency_status"], 0.0)
            score = tier_score + cap_bonus + status_bonus - 0.35 * d
            reasons = [f"{h['tier']} hospital"]
            if h["emergency_status"] == "confirmed":
                reasons.append("emergency care listed")
            elif h["emergency_status"] == "probable":
                reasons.append("emergency care likely (not confirmed)")
            if matched:
                reasons.append("capability: " + ", ".join(matched) + ("" if h.get("verified") else " (inferred from name)"))
            out.append({**h, "distance_km": round(d, 1), "score": round(score, 2), "reasons": reasons})
        return sorted(out, key=lambda x: -x["score"])

    res = build(need)
    if not res and need > 0:
        res = build(need - 1)
    return res
