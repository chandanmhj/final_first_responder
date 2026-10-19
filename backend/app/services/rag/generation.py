"""Groq client (OpenAI-compatible HTTP API) for chat, vision and speech-to-text."""
import base64
import json
import re

import httpx

from ...config import Settings
from ...core.errors import UpstreamError


class GroqClient:
    """Thin wrapper over Groq's OpenAI-compatible endpoints."""

    def __init__(self, settings: Settings, transport: httpx.BaseTransport | None = None):
        self.s = settings
        self._client = httpx.Client(timeout=45.0, transport=transport)

    @property
    def ready(self) -> bool:
        return self.s.groq_ready

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.s.groq_api_key}"}

    def chat(self, messages: list[dict], model: str | None = None, temperature: float = 0.2, max_tokens: int = 700,
             json_mode: bool = False) -> str:
        """Return the assistant text for a chat completion."""
        if not self.ready:
            raise UpstreamError("The language model is not configured.")
        body = {"model": model or self.s.llm_model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        try:
            r = self._client.post(f"{self.s.groq_base_url}/chat/completions", json=body, headers=self._headers())
        except httpx.HTTPError as exc:
            raise UpstreamError("Could not reach the language model.") from exc
        if r.status_code != 200:
            raise UpstreamError(f"Language model error ({r.status_code}).")
        return r.json()["choices"][0]["message"].get("content") or ""

    def chat_json(self, messages: list[dict], model: str | None = None, max_tokens: int = 500) -> dict:
        """Chat completion that must return a JSON object. Tolerates code fences."""
        text = self.chat(messages, model=model, temperature=0.0, max_tokens=max_tokens, json_mode=True)
        return parse_json_object(text)

    def vision_json(self, image_bytes: bytes, mime: str, prompt: str, max_tokens: int = 500) -> dict:
        """Ask the vision model about an image and return a JSON object."""
        b64 = base64.b64encode(image_bytes).decode()
        messages = [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        ]}]
        text = self.chat(messages, model=self.s.vision_model, temperature=0.0, max_tokens=max_tokens)
        return parse_json_object(text)

    def transcribe(self, audio: bytes, filename: str, content_type: str) -> str:
        """Speech to text with Whisper on Groq."""
        if not self.ready:
            raise UpstreamError("Speech recognition is not configured.")
        try:
            r = self._client.post(
                f"{self.s.groq_base_url}/audio/transcriptions",
                headers=self._headers(),
                data={"model": self.s.stt_model, "language": "en", "response_format": "json", "temperature": "0"},
                files={"file": (filename, audio, content_type)},
            )
        except httpx.HTTPError as exc:
            raise UpstreamError("Could not reach speech recognition.") from exc
        if r.status_code != 200:
            raise UpstreamError(f"Speech recognition error ({r.status_code}).")
        return (r.json().get("text") or "").strip()


def parse_json_object(text: str) -> dict:
    """Extract the first JSON object from model output. Returns {} if none is found."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    try:
        out = json.loads(text)
        return out if isinstance(out, dict) else {}
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                out = json.loads(m.group(0))
                return out if isinstance(out, dict) else {}
            except json.JSONDecodeError:
                return {}
    return {}
