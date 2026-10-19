-- Incidents, the timestamped events inside them, and generated handover reports.
create table if not exists public.incidents (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  session_id uuid references public.chat_sessions (id) on delete set null,
  condition text not null,
  location text,
  location_text text,
  scenario_id text,
  role text,
  for_self boolean not null default false,
  age_band text,
  status text not null default 'active',
  started_at timestamptz not null default now(),
  ended_at timestamptz
);
create index if not exists incidents_user_idx on public.incidents (user_id, started_at desc);

create table if not exists public.incident_events (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid not null references public.incidents (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  event_type text not null,
  payload jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);
create index if not exists incident_events_idx on public.incident_events (incident_id, occurred_at);

create table if not exists public.handover_reports (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid not null references public.incidents (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  report jsonb not null,
  created_at timestamptz not null default now()
);

alter table public.incidents enable row level security;
alter table public.incident_events enable row level security;
alter table public.handover_reports enable row level security;
drop policy if exists "own incidents" on public.incidents;
create policy "own incidents" on public.incidents for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
drop policy if exists "own events" on public.incident_events;
create policy "own events" on public.incident_events for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
drop policy if exists "own reports" on public.handover_reports;
create policy "own reports" on public.handover_reports for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
