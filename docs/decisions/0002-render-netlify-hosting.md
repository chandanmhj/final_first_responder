# 0002. Host backend on Render and frontend on Netlify

- Status: Decided
- Decided by: Chandan
- Date: 2026-10-05

## Context
Deployment target stated for the rebuild.

## Decision
FastAPI backend on Render, React frontend on Netlify.

## Consequences
Render free tier cold starts and limited RAM must be designed around. CORS locked to the Netlify domain.
