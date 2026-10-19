from app.services.safety.emergency_triage import is_urgent
from app.services.safety.guardrails import CRISIS_REPLY, is_crisis
from app.services.vision.animal_identification import AnimalResult, build_message, calibrate


def test_calibration_shrinks_and_caps():
    assert calibrate(100) == 85 and calibrate(100) <= 90
    assert calibrate(60) < 60 and calibrate(60) >= 50
    assert calibrate(20) < 20


def test_venomous_message_format():
    r = build_message(AnimalResult(is_animal=True, category="snake", species="cobra", venomous="yes", confidence_pct=80))
    assert "80% confidence" in r.headline and "hospital" in r.advice[0].lower()
    assert r.condition == "snake_bite"


def test_not_venomous_still_hospital():
    r = build_message(AnimalResult(is_animal=True, category="snake", species="rat snake", venomous="no", confidence_pct=59))
    assert r.headline.startswith("I can say with 59% confidence that it is not venomous")
    assert any("hospital" in a.lower() for a in r.advice)


def test_unknown_treated_as_dangerous():
    r = build_message(AnimalResult(is_animal=True, category="scorpion", venomous="unknown", confidence_pct=30))
    assert any("go to a hospital now" in a.lower() for a in r.advice)
    assert r.condition == "scorpion_sting"


def test_crisis_and_urgent_detection():
    assert is_crisis("I want to kill myself")
    assert "14416" in CRISIS_REPLY
    assert is_urgent("he is not breathing")
    assert not is_urgent("hello there")
