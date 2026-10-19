-- Guideline chunks with embeddings (384 dimensions: BAAI/bge-small-en-v1.5) and hybrid search.
create table if not exists public.knowledge_chunks (
  id text primary key,
  source text not null check (source in ('ifrc', 'handbook', 'authored')),
  doc text,
  topic text,
  section text,
  page text,
  module_id text,
  conditions text[] not null default '{}',
  text text not null,
  restricted boolean not null default false,
  embedding vector(384),
  fts tsvector generated always as (to_tsvector('english', coalesce(topic, '') || ' ' || coalesce(text, ''))) stored
);
create index if not exists knowledge_chunks_embedding_idx on public.knowledge_chunks using hnsw (embedding vector_cosine_ops);
create index if not exists knowledge_chunks_fts_idx on public.knowledge_chunks using gin (fts);

-- Reciprocal rank fusion of dense and full-text search. condition_filter boosts chunks of the active scenario.
create or replace function public.match_chunks_hybrid(
  query_text text, query_embedding vector(384), match_count int default 12, condition_filter text default null)
returns table (id text, source text, doc text, topic text, section text, page text, module_id text,
               conditions text[], text text, score double precision)
language sql stable as $$
  with dense as (
    select k.id, row_number() over (order by k.embedding <=> query_embedding) as r
    from public.knowledge_chunks k
    where not k.restricted and k.embedding is not null
    order by k.embedding <=> query_embedding
    limit match_count * 3
  ), lexical as (
    select k.id,
           row_number() over (order by ts_rank_cd(k.fts, websearch_to_tsquery('english', regexp_replace(trim(query_text), '\s+', ' or ', 'g'))) desc) as r
    from public.knowledge_chunks k
    where not k.restricted
      and k.fts @@ websearch_to_tsquery('english', regexp_replace(trim(query_text), '\s+', ' or ', 'g'))
    order by ts_rank_cd(k.fts, websearch_to_tsquery('english', regexp_replace(trim(query_text), '\s+', ' or ', 'g'))) desc
    limit match_count * 3
  ), fused as (
    select coalesce(d.id, l.id) as id,
           coalesce(1.0 / (60 + d.r), 0) + coalesce(1.0 / (60 + l.r), 0) as s
    from dense d full outer join lexical l on d.id = l.id
  )
  select k.id, k.source, k.doc, k.topic, k.section, k.page, k.module_id, k.conditions, k.text,
         f.s * case when condition_filter is not null and condition_filter = any (k.conditions) then 1.25 else 1.0 end as score
  from fused f join public.knowledge_chunks k on k.id = f.id
  order by score desc
  limit match_count;
$$;
