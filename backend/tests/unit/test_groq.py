import json

import httpx

from app.config import Settings
from app.services.rag.generation import GroqClient
from app.services.vision.animal_identification import identify


def client_with(handler):
    s = Settings(env="test", groq_api_key="k", auth_disabled=True)
    return GroqClient(s, transport=httpx.MockTransport(handler))


def test_chat_and_json():
    def handler(req):
        body = json.loads(req.content)
        assert req.headers["authorization"] == "Bearer k"
        content = '{"kind": "emergency"}' if body.get("response_format") else "hello"
        return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})

    c = client_with(handler)
    assert c.chat([{"role": "user", "content": "x"}]) == "hello"
    assert c.chat_json([{"role": "user", "content": "x"}]) == {"kind": "emergency"}


def test_vision_identify_calibrates():
    def handler(req):
        body = json.loads(req.content)
        assert body["messages"][0]["content"][1]["type"] == "image_url"
        d = {"is_animal": True, "category": "snake", "species_guess": "common krait", "venomous": "yes", "confidence": 95, "visible_features": ["banded"]}
        return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(d)}}]})

    res = identify(client_with(handler), b"\xff\xd8", "image/jpeg", "it just bit me")
    assert res.venomous == "yes" and res.confidence_pct < 95 and res.condition == "snake_bite"
    assert "venomous" in res.headline


def test_upstream_error_falls_back():
    res = identify(client_with(lambda r: httpx.Response(500)), b"x", "image/jpeg", "")
    assert res.venomous == "unknown" and any("hospital" in a.lower() for a in res.advice)


def test_transcribe():
    def handler(req):
        assert b"whisper" in req.content
        return httpx.Response(200, json={"text": " next step please "})

    assert client_with(handler).transcribe(b"RIFF", "a.wav", "audio/wav") == "next step please"
