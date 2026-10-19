# Architecture overview

```mermaid
flowchart LR
    U[User browser<br/>React + TypeScript + Tailwind<br/>Netlify] -->|REST / streaming| API[FastAPI backend<br/>Render]
    U -->|Auth, Google sign-in, hCaptcha| SB[(Supabase<br/>Auth + Postgres + pgvector)]
    U -->|media URLs| MEDIA[(Object storage<br/>R2 or Supabase, open)]
    API -->|verify token, read/write| SB
    API --> SC[Scenario engine<br/>modules + roles + rules]
    API --> RAG[RAG pipeline]
    RAG --> SB
    RAG --> GROQ[Groq language model]
    API --> VIS[Groq vision model]
    API --> STT[Groq Whisper speech-to-text]
    API --> HOS[Hospital finder]
    API --> REP[Handover report<br/>ISBAR timeline]
```

## Principles
- The browser fetches media directly from storage/CDN. Media bytes never pass through the backend.
- The step-to-media mapping is returned with the step text so the browser can start loading immediately.
- The service-role key lives only on the backend.
- The scenario engine decides the safe order of steps; the RAG system explains and answers questions around them.
- Everything about the RAG pipeline is evaluated before it is chosen.
