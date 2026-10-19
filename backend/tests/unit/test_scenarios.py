from app.services.conversation.roles import adjust_condition, band_protocol, infer_age_band
from app.services.scenarios.composer import compose, role_code, to_clinical, valid_location


def test_loads_conditions_and_modules(store):
    assert len(store.conditions) >= 40
    assert "cpr_adult" in store.modules and "scorpion_sting" in store.modules


def test_heart_attack_on_road_has_safety_first(store):
    steps = compose(store, "heart_attack", "road_journey_vehicle", "common", False)
    assert steps[0].module == "hazard_vehicle_journey"
    assert any(s.module == "heart_attack" for s in steps)
    assert all(s.total == len(steps) for s in steps)


def test_role_filtering(store):
    common = compose(store, "cardiac_arrest_adult", "home", "common", False)
    resp = compose(store, "cardiac_arrest_adult", "home", "responder", False)
    assert len(resp) > len(common)
    assert not any("carotid" in s.text.lower() for s in common)
    assert any("carotid" in s.text.lower() for s in resp)


def test_self_text_and_fallback(store):
    steps = compose(store, "heart_attack", "home", "common", True)
    assert any(s.text.startswith("Stop what you are doing") for s in steps)
    # cardiac arrest cannot be self-treated: falls back to the helper version
    assert compose(store, "cardiac_arrest_adult", "home", "common", True)


def test_trauma_only_steps_not_in_heart_attack(store):
    steps = compose(store, "heart_attack", "home", "common", False)
    assert not any("log roll" in s.text.lower() for s in steps)
    trauma = compose(store, "road_bike_helmet", "road_accident_scene", "common", False)
    assert any("log roll" in s.text.lower() for s in trauma)


def test_forbidden_tags_respected(store):
    for cid, c in store.conditions.items():
        for loc in c.valid_locations:
            for role in ("common", "responder"):
                for s in compose(store, cid, loc, role, False):
                    assert not set(s.tags) & set(c.forbid_tags), (cid, loc, s.id)


def test_clinical_glossary(store):
    assert "sternum" in to_clinical("Press the breastbone", store.glossary)


def test_authored_can_be_hidden(store):
    shown = compose(store, "scorpion_sting", "home", "common", False, show_authored=True)
    hidden = compose(store, "scorpion_sting", "home", "common", False, show_authored=False)
    assert shown and any(s.authored for s in shown)
    assert not any(s.authored for s in hidden)


def test_age_helpers(store):
    assert infer_age_band("my baby is not breathing") == "0-1"
    assert infer_age_band("a 7 year old fell") == "5-10"
    assert infer_age_band("he is 40 years old") == "18+"
    assert band_protocol(store, "0-1") == "infant"
    assert adjust_condition("cardiac_arrest_adult", "child") == "cardiac_arrest_child_infant"
    assert adjust_condition("choking_adult_child", "infant") == "choking_infant"


def test_valid_location_and_role_code(store):
    assert valid_location(store, "drowning", "road_journey_vehicle") in store.conditions["drowning"].valid_locations
    assert role_code("responder", True) == "R"
    assert role_code("common", True) == "S"
