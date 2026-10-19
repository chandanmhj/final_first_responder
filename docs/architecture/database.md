# Database (Supabase Postgres)

Status: **Proposed.** Nothing is implemented. Migration files are empty placeholders.

| Migration | Intended content |
|---|---|
| 0001_profiles_and_auth | profile per auth user, including role preference |
| 0002_chat_history | conversations and messages, stored permanently (Decided) |
| 0003_knowledge_base | guideline chunks, with pgvector embeddings (Decided: pgvector) |
| 0004_media_assets | media per step id, from `media/manifest.yaml` |
| 0005_rls_policies | Row Level Security: users only access their own rows |
| 0006_storage_buckets | buckets for step media and user photos |
| 0007_hospitals | hospital locations and capabilities |
| 0008_incident_events_and_handover | incidents, timestamped events, generated handover reports |

Rules: RLS on every user table; the frontend uses only the anon key; evaluation data is kept apart from user data.

## Capacity warning
You decided to keep chat history and photos forever. On the Supabase free plan the database is 500 MB and file storage is
1 GB, and the vector index for the knowledge base also uses database space. Photos will reach the limit first.
Options: compress photos before upload, move photos to R2, or upgrade the plan. See media-delivery.md.
