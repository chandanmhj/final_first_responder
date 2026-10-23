"""Decide which condition and location a message describes."""
import re
from dataclasses import dataclass

from ..rag.generation import GroqClient
from .composer import valid_location
from .loader import ScenarioStore

# (condition id, keywords). More specific entries come first and score higher.
KEYWORDS: list[tuple[str, list[str]]] = [
    ("road_not_breathing_bike", ["bike", "scooter", "motorcycle", "helmet"]),  # combined with 'not breathing' below
    ("cardiac_arrest_adult", ["not breathing", "stopped breathing", "no pulse", "cardiac arrest", "collapsed", "unresponsive", "unconscious", "not responding", "not responsive", "lost consciousness", "lost consiousness", "lost conciousness", "heart stopped"]),
    ("heart_attack", ["heart attack", "chest pain", "chest tightness", "chest pressure", "pain in chest", "left arm pain"]),
    ("stroke", ["stroke", "face drooping", "slurred speech", "face is drooping", "arm weakness", "can't lift arm", "one side weak"]),
    ("choking_adult_child", ["choking", "choked", "something stuck in throat", "food stuck", "can't breathe and can't talk"]),
    ("choking_infant", ["baby choking", "infant choking"]),
    ("choking_self", ["i am choking", "i'm choking", "choking alone"]),
    ("snake_bite", ["snake", "snakebite", "snake bite"]),
    ("scorpion_sting", ["scorpion"]),
    ("insect_sting", ["bee sting", "wasp", "bee stung", "insect bite", "tick bite", "stung by"]),
    ("animal_bite", ["dog bite", "dog bit", "bitten by a dog", "cat bite", "monkey bite", "bitten by", "animal bite", "rabies"]),
    ("anaphylaxis", ["allergic reaction", "anaphylaxis", "throat swelling", "face swelling", "swollen lips", "allergy"]),
    ("asthma_attack", ["asthma", "wheezing", "inhaler"]),
    ("breathing_difficulty", ["difficulty breathing", "can't breathe", "short of breath", "breathless", "hard to breathe"]),
    ("seizure", ["seizure", "convulsion", "fit", "fitting", "epilepsy", "shaking all over"]),
    ("low_blood_sugar", ["low sugar", "low blood sugar", "hypoglycemia", "hypoglycaemia", "diabetic and confused"]),
    ("high_blood_sugar", ["high sugar", "high blood sugar", "hyperglycemia"]),
    ("fainting", ["fainted", "feeling faint", "dizzy and about to pass out", "passed out"]),
    ("drowning", ["drowning", "drowned", "pulled out of water", "fell in water", "pool", "river", "lake"]),
    ("burns", ["burn", "burnt", "scald", "caught fire", "on fire"]),
    ("electric_shock", ["electric shock", "electrocuted", "live wire", "electrocution"]),
    ("bleeding_severe", ["bleeding heavily", "heavy bleeding", "bleeding a lot", "blood everywhere", "won't stop bleeding", "deep cut", "severe bleeding"]),
    ("minor_wound", ["small cut", "minor cut", "scrape", "graze", "minor wound"]),
    ("nosebleed", ["nosebleed", "nose bleed", "nose is bleeding"]),
    ("fracture_sprain", ["broken bone", "fracture", "sprain", "twisted ankle", "broke my arm", "broke his leg"]),
    ("head_injury", ["head injury", "hit his head", "hit her head", "hit my head", "concussion", "head trauma"]),
    ("chest_abdomen_injury", ["stabbed", "chest injury", "abdomen injury", "stomach injury"]),
    ("amputation", ["amputat", "finger cut off", "severed", "cut off"]),
    ("poisoning", ["poison", "swallowed", "overdose", "drank pesticide", "ingested", "bleach"]),
    ("heat_illness", ["heatstroke", "heat stroke", "heat exhaustion", "too hot", "overheated"]),
    ("hypothermia", ["hypothermia", "freezing", "too cold", "shivering badly"]),
    ("emergency_childbirth", ["giving birth", "in labour", "in labor", "baby is coming", "delivery now", "water broke"]),
    ("fever", ["fever", "high temperature"]),
    ("panic_attack", ["panic attack", "panic", "anxiety attack", "can't calm down"]),
    ("shock", ["pale and clammy", "signs of shock", "in shock"]),
    ("infection_red_flags", ["infection", "pus", "spreading redness"]),
    ("road_car_conscious", ["car accident", "car crash", "road accident", "road crash", "vehicle accident"]),
    ("road_pedestrian", ["hit by a car", "hit by a vehicle", "pedestrian"]),
    ("road_bike_helmet", ["bike accident", "scooter accident", "motorcycle accident", "fell off bike", "fell off his bike", "helmet"]),
    ("fall_or_machinery_trauma", ["fell from", "fall from height", "machine injury", "machinery", "crushed"]),
    ("railway_trauma", ["train accident", "railway accident", "hit by train"]),
]
LOCATION_CUES = [
    ("road_accident_scene", ["accident", "crash", "highway", "hit by", "fell off bike", "collision"]),
    ("road_journey_vehicle", ["while driving", "in the car", "in my car", "on the way", "during the journey", "on a journey", "road trip", "in the vehicle", "driving"]),
    ("railway", ["railway", "train track", "railway track", "hit by train"]),
    ("water_body", ["water", "pool", "river", "lake", "sea", "beach", "pond", "swimming"]),
    ("workplace_industrial", ["factory", "machine", "machinery", "construction", "industrial"]),
    ("fire_scene", ["fire", "smoke", "burning building", "explosion"]),
    ("public_transport", ["bus", "metro", "train", "flight", "tram"]),
    ("workplace", ["office", "at work", "workplace", "school", "college"]),
    ("outdoors", ["trek", "forest", "farm", "garden", "field", "trail", "hiking"]),
    ("public_place", ["mall", "street", "market", "public", "park", "temple", "station"]),
]

_STEMS = {"burn", "amputat"}  # may be followed by more letters (burns, burning)


def _has(t: str, w: str) -> bool:
    """Whole-word match, so 'pond' does not match 'responding' and 'sea' does not match 'search'."""
    w = w.strip()
    tail = "" if (w in _STEMS or " " in w or len(w) > 6) else r"(?![a-z])"
    return re.search(r"(?<![a-z])" + re.escape(w) + tail, t) is not None


@dataclass
class Route:
    """Result of routing a message."""

    kind: str  # emergency | smalltalk | question | unclear
    condition: str | None = None
    location: str | None = None
    score: float = 0.0
    clarify: str | None = None


def rule_based_match(text: str, store: ScenarioStore) -> Route:
    """Keyword routing. Fast, offline, and used as the fallback when no model is available."""
    t = " " + text.lower() + " "
    best, best_score = None, 0.0
    for cid, words in KEYWORDS:
        if cid not in store.conditions:
            continue
        hits = [w for w in words if _has(t, w)]
        if hits:
            score = max(len(w.split()) for w in hits) + 0.5 * len(hits)
            if score > best_score:
                best, best_score = cid, score
    # not breathing after a road accident
    breathing_stopped = any(_has(t, w) for w in ("not breathing", "stopped breathing", "unresponsive", "unconscious", "no pulse"))
    road = any(_has(t, w) for w in ("accident", "crash", "hit by", "fell off"))
    if breathing_stopped and road:
        bike = any(_has(t, w) for w in ("bike", "scooter", "motorcycle", "helmet"))
        best = "road_not_breathing_bike" if bike else "road_not_breathing_car"
        best_score = max(best_score, 4)
    elif best == "road_not_breathing_bike" and not breathing_stopped:
        best = "road_bike_helmet"
    if best == "cardiac_arrest_adult" and any(_has(t, w) for w in ("water", "pool", "river", "lake", "sea", "pond", "drown")):
        best, best_score = "drowning", max(best_score, 3)
    if not best:
        return Route("unclear")
    loc = None
    for lid, cues in LOCATION_CUES:
        if any(_has(t, c) for c in cues):
            loc = lid
            break
    if best.startswith(("road_", "fall_or", "railway")) and loc not in (None, "road_accident_scene", "railway", "workplace_industrial", "home", "public_place", "outdoors"):
        loc = "road_accident_scene"
    loc = valid_location(store, best, loc)
    return Route("emergency", best, loc, best_score)


SMALLTALK = re.compile(r"^\s*(hi|hello|hey|good (morning|afternoon|evening)|how are you|thanks|thank you|bye|who are you|what can you do|ok|okay|help)\b", re.I)


def classify(text: str, store: ScenarioStore, llm: GroqClient | None, has_active: bool) -> Route:
    """Route a free-text message: emergency (with condition), question, small talk or unclear."""
    rb = rule_based_match(text, store)
    if rb.kind == "emergency" and rb.score >= 1.5:
        return rb
    if SMALLTALK.match(text) and rb.kind != "emergency":
        return Route("smalltalk")
    if llm and llm.ready:
        listing = "\n".join(f"- {c.id}: {c.title}" for c in store.conditions.values())
        try:
            out = llm.chat_json([
                {"role": "system", "content": "Classify the user's message for a first-aid app. Return JSON with keys: kind (emergency|question|smalltalk|unclear), "
                                              "condition (one id from the list or null), location (home|public_place|workplace|workplace_industrial|road_journey_vehicle|"
                                              "road_accident_scene|railway|water_body|fire_scene|outdoors|public_transport or null), clarify (a short question or null).\n"
                                              f"Conditions:\n{listing}"},
                {"role": "user", "content": text},
            ])
            kind = out.get("kind")
            cond = out.get("condition")
            if kind == "emergency" and cond in store.conditions:
                return Route("emergency", cond, valid_location(store, cond, out.get("location")), 1.5, None)
            if kind in ("smalltalk", "question"):
                return Route(kind)
            if kind == "unclear":
                return Route("unclear", clarify=out.get("clarify"))
        except Exception:
            pass
    if rb.kind == "emergency":
        return rb
    if has_active:
        return Route("question")
    return Route("unclear")