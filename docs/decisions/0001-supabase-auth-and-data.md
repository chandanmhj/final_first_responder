# 0001. Use Supabase for authentication and user data

- Status: Decided
- Decided by: Chandan
- Date: 2026-10-05

## Context
Supabase provides auth (email and Google), Postgres and storage.

## Decision
Supabase for authentication and for storing all user data.

## Consequences
Backend verifies Supabase tokens. Row Level Security is required on user tables.
