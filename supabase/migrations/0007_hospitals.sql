-- Optional table for the cleaned hospital list. The API currently reads data/hospitals/hospitals_clean.json.
create table if not exists public.hospitals (
  id text primary key,
  name text not null,
  lat double precision not null,
  lon double precision not null,
  tier text,
  class text,
  scope text,
  emergency_status text,
  specialties text[] default '{}',
  capabilities text[] default '{}',
  phones text[] default '{}',
  verified boolean default false
);
alter table public.hospitals enable row level security;
drop policy if exists "hospitals readable" on public.hospitals;
create policy "hospitals readable" on public.hospitals for select using (auth.role() = 'authenticated');
