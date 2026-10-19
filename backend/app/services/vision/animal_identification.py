"""Identify a bite or sting animal from a photo and say how confident we are.

The vision model gives a guess and a raw confidence. We calibrate that number (see calibrate()) and always tell the
person to visit a hospital once for confirmation. The result never changes the first-aid steps.
"""
import json
import os
from dataclasses import asdict, dataclass, field

from ..rag.generation import GroqClient

PROMPT = """You are helping with first aid. Look at the photo. The person says: "{text}".
Return ONLY a JSON object with these keys:
is_animal (true/false), category ("snake"|"scorpion"|"spider"|"insect"|"other"|"none"),
species_guess (common name or "unknown"), venomous ("yes"|"no"|"unknown"),
confidence (integer 0-100, how sure you are that the venomous answer is right),
visible_features (list of up to 4 short strings). Do not add any other text."""

HOSPITAL_LINE = "Please still go to a hospital once to confirm, even if it does not look dangerous."


@dataclass
class AnimalResult:
    """What we tell the user about the animal in the photo."""

    is_animal: bool = False
    category: str = "none"
    species: str = "unknown"
    venomous: str = "unknown"
    confidence_pct: int = 0
    raw_confidence: int = 0
    headline: str = ""
    advice: list[str] = field(default_factory=list)
    condition: str | None = None  # scenario to start, if any
    features: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def calibrate(raw: int, data_dir: str | None = None) -> int:
    """Turn the model's raw confidence into a shown percentage.

    Placeholder until the evaluation notebook (05) fits a real curve: shrink toward 50 and cap at 90, because vision
    models are overconfident on animal identification. If data/vision/calibration.json exists it is used instead:
    {"points": [[raw, calibrated], ...]} with linear interpolation.
    """
    raw = max(0, min(100, int(raw)))
    path = os.path.join(data_dir, "vision", "calibration.json") if data_dir else None
    if path and os.path.exists(path):
        pts = sorted(json.load(open(path))["points"])
        if pts:
            if raw <= pts[0][0]:
                return int(pts[0][1])
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if raw <= x1:
                    return int(round(y0 + (y1 - y0) * (raw - x0) / max(x1 - x0, 1)))
            return int(pts[-1][1])
    shrunk = 50 + (raw - 50) * 0.7 if raw >= 50 else raw * 0.9
    return int(round(min(90, shrunk)))


def build_message(res: AnimalResult) -> AnimalResult:
    """Fill headline and advice from the result. Wording follows the product decision."""
    name = res.species if res.species != "unknown" else res.category
    p = res.confidence_pct
    if not res.is_animal or res.category == "none":
        res.headline = "I can't see a bite or sting animal in this photo."
        res.advice = ["Tell me what happened, or send another photo. If someone was bitten or stung, treat it as urgent and go to a hospital."]
        return res
    if res.venomous == "yes":
        res.headline = f"I can say with {p}% confidence that this looks like a venomous {name}."
        res.advice = ["Yes, it is likely venomous. Get to the nearest hospital now and call 108.", "Keep the person still and calm. Do not cut, suck or tie the wound."]
    elif res.venomous == "no":
        res.headline = f"I can say with {p}% confidence that it is not venomous ({name})."
        res.advice = [HOSPITAL_LINE]
    else:
        res.headline = f"I can't tell if this {name} is venomous (only {p}% confident)."
        res.advice = ["Treat it as if it could be venomous: go to a hospital now.", HOSPITAL_LINE]
    if res.category == "snake":
        res.condition = "snake_bite"
    elif res.category == "scorpion":
        res.condition = "scorpion_sting"
    elif res.category in ("insect", "spider"):
        res.condition = "insect_sting"
    return res


def identify(llm: GroqClient, image: bytes, mime: str, text: str, data_dir: str | None = None) -> AnimalResult:
    """Run the vision model and return a calibrated result. Falls back to 'cannot tell' on any failure."""
    if not llm.ready:
        return build_message(AnimalResult(is_animal=True, category="other", venomous="unknown", confidence_pct=0))
    try:
        d = llm.vision_json(image, mime, PROMPT.format(text=text or "someone was bitten or stung"))
    except Exception:
        return build_message(AnimalResult(is_animal=True, category="other", venomous="unknown", confidence_pct=0))
    raw = int(d.get("confidence", 0) or 0)
    venomous = d.get("venomous") if d.get("venomous") in ("yes", "no", "unknown") else "unknown"
    res = AnimalResult(
        is_animal=bool(d.get("is_animal")), category=d.get("category") or "none", species=d.get("species_guess") or "unknown",
        venomous=venomous, raw_confidence=raw, confidence_pct=calibrate(raw, data_dir),
        features=[str(x) for x in (d.get("visible_features") or [])][:4],
    )
    if res.confidence_pct < 50 and res.venomous != "yes":
        res.venomous = "unknown"
    return build_message(res)
