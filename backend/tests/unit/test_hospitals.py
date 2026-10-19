import json

from app.services.hospitals.finder import HospitalIndex


def test_heart_attack_prefers_cardiac(settings):
    idx = HospitalIndex(settings.data_dir)
    # near Jayadeva (Bannerghatta Road), Bengaluru
    out = idx.nearby(12.92, 77.60, "heart_attack", limit=3)
    assert out["results"]
    assert "cardiac" in out["results"][0]["capabilities"]
    assert out["results"][0]["directions_url"].startswith("https://www.google.com/maps")


def test_far_away_returns_message(settings):
    idx = HospitalIndex(settings.data_dir)
    out = idx.nearby(28.61, 77.20, "heart_attack")
    assert out["results"] == [] and "108" in out["message"]


def test_specialty_hospitals_not_used_for_general_emergencies(settings):
    idx = HospitalIndex(settings.data_dir)
    out = idx.nearby(12.9753, 77.6978, "bleeding_severe", limit=5)
    assert all(r["scope"] != "specialty" for r in out["results"])


def test_minor_condition_allows_primary(settings):
    idx = HospitalIndex(settings.data_dir)
    out = idx.nearby(12.9503, 77.6162, "animal_bite", limit=5)
    assert out["results"]
