# scripts/
- `expand_scenarios.py`: validate and expand scenarios; writes catalog, media manifest and replace.md.
- `build_corpus.py`: IFRC PDF and modules to JSONL chunks.
- `build_knowledge_base.py`: embed chunks and upload to Supabase.
- `clean_hospitals.py`: clean the scraped hospital list.
- `compress_media.sh`, `upload_media_to_supabase.py`: prepare and upload step media.
