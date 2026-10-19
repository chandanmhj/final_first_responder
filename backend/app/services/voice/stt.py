"""Server-side speech to text (Whisper on Groq)."""
from ...core.errors import AppError
from ..rag.generation import GroqClient

ALLOWED = ("audio/wav", "audio/x-wav", "audio/webm", "audio/ogg", "audio/mpeg", "audio/mp4", "audio/m4a", "audio/flac", "video/webm")


def transcribe(llm: GroqClient, audio: bytes, filename: str, content_type: str, max_mb: int) -> str:
    """Validate the upload and return the transcript."""
    if not audio:
        raise AppError("No audio received.")
    if len(audio) > max_mb * 1024 * 1024:
        raise AppError(f"Audio is larger than {max_mb} MB.")
    if content_type and content_type.split(";")[0] not in ALLOWED:
        raise AppError("Unsupported audio type.")
    return llm.transcribe(audio, filename or "speech.wav", content_type.split(";")[0] or "audio/wav")
