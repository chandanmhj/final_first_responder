# Deployment checklist

Status: **Proposed**. Fill in as setup happens.

## Supabase
- Create the project (choose a region near users).
- Apply migrations from `supabase/migrations/`.
- Enable email auth and Google; enable hCaptcha; configure custom SMTP.
- Set site URL and redirect URLs for localhost and Netlify.
- Create storage buckets for step media.

## Render (backend)
- Service from `backend/`; `render.yaml` is a placeholder.
- Set environment variables from `.env.example`.
- Health-check path: `/health`.
- Expect cold starts on the free tier; the frontend shows a "server waking up" state.

## Netlify (frontend)
- Build from `frontend/`; `public/_redirects` handles SPA routes.
- Set `VITE_API_BASE_URL`, Supabase anon key and hCaptcha site key.

## Security
- CORS limited to the Netlify domain.
- Service-role key only on Render.
- Run secret scanning before the first push.
