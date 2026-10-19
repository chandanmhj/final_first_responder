-- Row Level Security: users only see their own rows. The backend uses the service-role key and filters by user_id itself.
alter table public.profiles enable row level security;
alter table public.chat_sessions enable row level security;
alter table public.chat_messages enable row level security;
alter table public.media_assets enable row level security;
alter table public.knowledge_chunks enable row level security;   -- no policies: only the backend can read it

drop policy if exists "own profile" on public.profiles;
create policy "own profile" on public.profiles for all using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "own sessions" on public.chat_sessions;
create policy "own sessions" on public.chat_sessions for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own messages" on public.chat_messages;
create policy "own messages" on public.chat_messages for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "media is readable" on public.media_assets;
create policy "media is readable" on public.media_assets for select using (true);
