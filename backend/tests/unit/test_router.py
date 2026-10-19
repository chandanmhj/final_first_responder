import pytest

from app.services.scenarios.scenario_router import classify, rule_based_match


@pytest.mark.parametrize("text,cond,loc", [
    ("my father has chest pain while driving", "heart_attack", "road_journey_vehicle"),
    ("a snake bit my friend in the garden", "snake_bite", None),
    ("scorpion sting on my son's foot", "scorpion_sting", None),
    ("the biker is not breathing after the accident, helmet on", "road_not_breathing_bike", "road_accident_scene"),
    ("car accident, driver unconscious and not breathing", "road_not_breathing_car", "road_accident_scene"),
    ("someone is choking on food", "choking_adult_child", None),
    ("heavy bleeding from a deep cut at the factory", "bleeding_severe", "workplace_industrial"),
    ("kid fell in the pool and is not breathing", "drowning", "water_body"),
])
def test_rule_based_routes(store, text, cond, loc):
    r = rule_based_match(text, store)
    assert r.kind == "emergency"
    assert r.condition == cond
    if loc:
        assert r.location == loc
    assert r.location in store.conditions[r.condition].valid_locations


def test_smalltalk_and_unclear(store):
    assert classify("hi how are you", store, None, False).kind == "smalltalk"
    assert classify("the weather is nice", store, None, False).kind == "unclear"
    assert classify("what if it doesn't stop", store, None, True).kind == "question"
