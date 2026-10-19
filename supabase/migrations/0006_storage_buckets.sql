-- step-media: public, read by everyone (fast CDN delivery). user-uploads: private photos sent in chat.
insert into storage.buckets (id, name, public) values ('step-media', 'step-media', true) on conflict (id) do nothing;
insert into storage.buckets (id, name, public) values ('user-uploads', 'user-uploads', false) on conflict (id) do nothing;

drop policy if exists "users read own uploads" on storage.objects;
create policy "users read own uploads" on storage.objects for select
  using (bucket_id = 'user-uploads' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "users add own uploads" on storage.objects;
create policy "users add own uploads" on storage.objects for insert
  with check (bucket_id = 'user-uploads' and (storage.foldername(name))[1] = auth.uid()::text);
