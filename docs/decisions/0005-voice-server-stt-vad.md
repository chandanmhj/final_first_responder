# 0005. Hands-free mode uses server speech-to-text with voice activity detection

- Status: Decided
- Decided by: Chandan
- Date: 2026-10-05

## Context
Browser-native speech is simpler; server speech-to-text is more accurate but more work.

## Decision
Server-side speech-to-text plus voice activity detection.

## Consequences
More engineering: echo handling, barge-in and end-of-turn tuning. Text-to-speech and languages still open.
