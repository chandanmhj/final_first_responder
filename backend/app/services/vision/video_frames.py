"""Short videos: pull a few evenly spaced frames and let the Groq vision model describe what is happening."""
import io

from ..rag.generation import GroqClient

PROMPT = ("These {n} frames come from one short video, in time order. Describe in two or three short sentences what is happening and what "
          "first-aid problem it shows (for example: person collapsed and not moving, deep bleeding cut, choking, burn, snake bite). "
          "Mention hazards such as traffic, fire or water. Do not diagnose. The person says: \"{text}\". "
          "Return JSON: {{\"description\": \"...\"}}")


def extract_frames(data: bytes, n: int = 4, max_side: int = 768) -> list[bytes]:
    """Return up to n JPEG frames spread across the video. Empty list if the video cannot be read."""
    try:
        import av  # PyAV bundles its own decoder, so no ffmpeg install is needed
    except ImportError:
        return []
    thumbs = []
    try:
        with av.open(io.BytesIO(data)) as c:
            stream = c.streams.video[0]
            step = max(1, (stream.frames or 240) // 24)
            for i, frame in enumerate(c.decode(stream)):
                if i > 900:
                    break
                if i % step == 0:
                    img = frame.to_image()
                    img.thumbnail((max_side, max_side))
                    thumbs.append(img)
    except Exception:
        return []
    if not thumbs:
        return []
    picks = [thumbs[min(len(thumbs) - 1, int((k + 0.5) * len(thumbs) / n))] for k in range(min(n, len(thumbs)))]
    out = []
    for img in picks:
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=80)
        out.append(buf.getvalue())
    return out


def describe(llm: GroqClient, frames: list[bytes], text: str) -> str:
    """Short description of the video, or an empty string when the model is unavailable."""
    if not llm.ready or not frames:
        return ""
    try:
        out = llm.vision_json_multi([(f, "image/jpeg") for f in frames], PROMPT.format(n=len(frames), text=text or ""))
        return str(out.get("description", ""))[:400]
    except Exception:
        return ""