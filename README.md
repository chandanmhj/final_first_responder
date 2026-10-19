# First Responder

Emergency first-aid guide: guideline-grounded RAG, 180+ scenarios, photo help, hands-free voice, hospital finder and ISBAR handover report.
Final-year project and research paper basis.

## Run locally
1. Supabase: create a project, run `supabase/migrations/*.sql` in order, enable Email and Google auth, set redirect URLs.
2. `cp .env.example .env` and fill it; create `frontend/.env` from `frontend/.env.example`.
3. Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload` (tests: `pip install -r requirements-dev.txt && pytest`).
4. Corpus: `python scripts/build_corpus.py --ifrc data/guidelines/raw/ifrc_2025.pdf` then `python scripts/build_knowledge_base.py`.
5. Hospitals: save your list as `data/hospitals/raw/ambulance_hospitals.json`, run `python scripts/clean_hospitals.py`.
6. Frontend: `cd frontend && npm install && npm run dev`.
7. Media: fill `media/replace.md`, run `scripts/compress_media.sh`, then `scripts/upload_media_to_supabase.py`.
8. Evaluation: `cd evaluation && PYTHONPATH=. python -m rag_eval.cli run --make-seed`.

Deploy: backend on Render (`render.yaml`), frontend on Netlify (`netlify.toml`). See `docs/`.
