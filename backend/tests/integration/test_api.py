import io


def post(client, **data):
    return client.post("/api/chat", data={k: v for k, v in data.items() if v is not None}, files=data.pop("files", None))


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/health").json() == {"status": "ok"}


def test_profile_role_rules(client):
    assert client.get("/api/me").json()["role"] is None
    r = client.put("/api/me", json={"role": "responder"})
    assert r.status_code == 400
    r = client.put("/api/me", json={"role": "responder", "attested": True, "full_name": "A"})
    assert r.status_code == 200 and r.json()["role"] == "responder" and r.json()["attested_at"]
    assert client.put("/api/me", json={"role": "wizard"}).status_code == 422


def test_full_scenario_flow_and_handover(client):
    r = client.post("/api/chat", data={"message": "my father has chest pain while driving"}).json()
    sid = r["session_id"]
    assert r["scenario"]["condition"] == "heart_attack" and r["scenario"]["location"] == "road_journey_vehicle"
    step_msg = [m for m in r["messages"] if m["type"] == "step"][0]
    assert step_msg["step"]["index"] == 0 and [q["action"] for q in step_msg["quick_replies"]] == ["next", "not_worked"]
    assert step_msg["step"]["source_label"]
    total = step_msg["step"]["total"]
    # not worked keeps the same step
    nw = client.post("/api/chat", data={"session_id": sid, "action": "not_worked"}).json()
    assert nw["scenario"]["index"] == 0 and nw["messages"][0]["type"] == "text"
    last = None
    for _ in range(total):
        last = client.post("/api/chat", data={"session_id": sid, "action": "next"}).json()
    assert last["scenario"]["status"] == "completed"
    assert "108" in last["messages"][0]["text"]
    # hospitals need location
    h = client.post("/api/chat", data={"session_id": sid, "action": "hospitals"}).json()
    assert h["messages"][0]["type"] == "needs_location"
    h = client.post("/api/chat", data={"session_id": sid, "action": "hospitals", "lat": "12.92", "lon": "77.60"}).json()
    assert h["messages"][0]["type"] == "hospitals" and h["messages"][0]["hospitals"]
    # manual event + handover
    inc = r["incident_id"]
    assert client.post(f"/api/incidents/{inc}/events", json={"event_type": "called_108", "text": "called at roadside"}).status_code == 200
    rep = client.get(f"/api/incidents/{inc}/handover").json()
    assert "ISBAR" in rep["markdown"] and any("Called 108" in t["text"] for t in rep["report"]["assessment_and_actions"])
    # sessions and messages persisted
    assert client.get("/api/sessions").json()[0]["id"] == sid
    assert len(client.get(f"/api/sessions/{sid}/messages").json()["messages"]) >= 4
    assert client.delete(f"/api/sessions/{sid}").status_code == 200
    assert client.get(f"/api/sessions/{sid}/messages").status_code == 404


def test_smalltalk_and_unclear(client):
    r = client.post("/api/chat", data={"message": "hi, how are you?"}).json()
    assert r["scenario"] is None and r["messages"][0]["type"] == "text"
    r = client.post("/api/chat", data={"message": "tell me a thing about nothing"}).json()
    assert "who needs help" in r["messages"][0]["text"]


def test_baby_cpr_uses_child_protocol(client):
    r = client.post("/api/chat", data={"message": "my baby is not breathing and unresponsive"}).json()
    assert r["scenario"]["condition"] == "cardiac_arrest_child_infant"
    assert r["urgent"] is True


def test_crisis_message(client):
    r = client.post("/api/chat", data={"message": "I want to end my life"}).json()
    assert r["messages"][0].get("crisis") and "14416" in r["messages"][0]["text"]


def test_responder_sees_clinical_steps(client):
    client.put("/api/me", json={"role": "responder", "attested": True})
    r = client.post("/api/chat", data={"message": "adult collapsed and not breathing"}).json()
    texts = " ".join(m["step"]["text"] for m in r["messages"] if m["type"] == "step")
    assert r["scenario"]["condition"] == "cardiac_arrest_adult" and texts


def test_image_validation(client):
    r = client.post("/api/chat", data={"message": "bitten"}, files={"image": ("x.txt", io.BytesIO(b"hello"), "text/plain")})
    assert r.status_code == 400
    r = client.post("/api/chat", data={"message": "a snake bit me"}, files={"image": ("s.jpg", io.BytesIO(b"\xff\xd8\xff"), "image/jpeg")})
    assert r.status_code == 200
    kinds = [m["type"] for m in r.json()["messages"]]
    assert "animal" in kinds


def test_voice_validation(client):
    r = client.post("/api/voice/transcribe", files={"audio": ("a.wav", io.BytesIO(b""), "audio/wav")})
    assert r.status_code == 400


def test_unauthorized_when_auth_enabled(settings):
    from fastapi.testclient import TestClient

    from app.main import create_app

    s = settings.model_copy(update={"auth_disabled": False})
    with TestClient(create_app(s)) as c:
        assert c.get("/api/me").status_code == 401


def test_media_resolver(client):
    r = client.get("/api/media/step/cpr_adult.04")
    assert r.status_code == 200 and r.json() == {"video": None, "image": None}
