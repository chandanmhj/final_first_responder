-- Which step has which media file. Filled from media/manifest.yaml by scripts/upload_media_to_supabase.py.
create table if not exists public.media_assets (
  step_id text primary key,            -- for example cpr_adult.04
  video_path text,
  image_path text,
  status text not null default 'missing' check (status in ('missing', 'video', 'image', 'both')),
  updated_at timestamptz not null default now()
);
