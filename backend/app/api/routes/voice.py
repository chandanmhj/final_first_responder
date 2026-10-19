"""Speech to text for hands-free mode."""
from fastapi import APIRouter, Depends, File, UploadFile

from ...core.security import AuthUser
from ...services.voice.stt import transcribe
from ...state import Services
from ..deps import get_services, rate_limited

router = APIRouter(prefix="/api/voice")


@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), user: AuthUser = Depends(rate_limited), services: Services = Depends(get_services)):
    """Turn one finished utterance into text."""
    data = await audio.read()
    text = transcribe(services.llm, data, audio.filename or "speech.wav", audio.content_type or "audio/wav", services.settings.max_audio_mb)
    return {"text": text}
