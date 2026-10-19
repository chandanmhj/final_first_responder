# Hands-free voice mode

## Requirements (Decided)
- Works like ChatGPT or Claude call mode. No manual record or speak button.
- It listens while it speaks and speaks while it listens.
- It decides by itself when to send the speech to the model.
- Speech-to-text is **server-side with voice activity detection**.
- Text-to-speech is the **browser voice**, but it must feel human, comfortable and fast.
- English only for now.

## What this implies (Proposed design notes)
- **Voice activity detection** in the browser decides when the user starts and stops speaking.
- **End-of-turn detection** must tolerate pauses so the user is not cut off. The pause length is a tuning parameter.
- **Barge-in:** if the user speaks while the assistant talks, playback stops and the new speech is captured.
- **Echo handling:** the microphone must not pick up the assistant's own voice. Needs testing on real phones.
- **Latency:** stream audio up and stream the answer back; speak sentences as they arrive.
- **Natural voice with the browser voice:** choose the best available voice, short sentences, a slightly faster rate, small pauses between steps.
  Browser voices vary by device and cannot be fully controlled. If it still sounds robotic, a hosted voice is the fallback
  (Groq offers a preview English voice model, see groq-models.md).
- **Server speech-to-text:** Groq's `whisper-large-v3-turbo` is a candidate.
- **Emergency fallback:** the screen shows the same step text and quick-reply buttons, so the user can still tap.
