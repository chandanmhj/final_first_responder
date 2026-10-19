# 0004. hCaptcha as the captcha provider

- Status: Decided
- Decided by: Chandan
- Date: 2026-10-05

## Context
Supabase Auth supports hCaptcha and Cloudflare Turnstile natively; reCAPTCHA would need custom verification.

## Decision
hCaptcha.

## Consequences
Site key in the frontend; secret entered in Supabase Auth settings.
