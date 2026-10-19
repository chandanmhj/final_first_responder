# Backend (FastAPI on Render)

Status: module layout **Proposed**; the folders exist in `backend/app/`.

| Module | Responsibility |
|---|---|
| api/routes | health, chat, voice, vision, media, sessions, me, hospitals, handover, incidents |
| core | security, logging, rate limiting, error handling |
| db | Supabase client and repositories |
| schemas | request and response models |
| services/rag | ingestion, chunking, embeddings, retrieval, reranking, query understanding, prompting, generation, citations, abstention, pipeline |
| services/scenarios | loads `data/scenarios`, composes scenarios, routes a user message to a scenario |
| services/vision | image understanding, animal identification with calibrated confidence |
| services/voice | speech-to-text, voice activity and end-of-turn, text-to-speech helpers |
| services/conversation | intent routing (emergency vs small talk), roles, step manager, quick replies |
| services/media | resolve step media, signed URLs |
| services/hospitals | finder and facility matching |
| services/handover | event timeline and ISBAR report |
| services/safety | emergency triage, disclaimers, guardrails |

Rules: a docstring on every public method; no secrets in code; Render's free tier has cold starts and limited RAM, so avoid heavy local models.
F