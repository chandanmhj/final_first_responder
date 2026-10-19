"""Voice activity detection runs in the browser (frontend/src/hooks/useVoiceActivity.ts).

The server only receives finished utterances. This module documents the contract and holds shared limits.
"""
MAX_UTTERANCE_SECONDS = 20
SAMPLE_RATE = 16000
