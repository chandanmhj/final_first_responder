alter table public.profiles
  add column if not exists age int,
  add column if not exists sex text,
  add column if not exists blood_group text,
  add column if not exists allergies text,
  add column if not exists conditions text,
  add column if not exists medications text,
  add column if not exists emergency_contact text;
alter table public.chat_sessions add column if not exists pinned boolean not null default false;