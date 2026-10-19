# Open questions
Most earlier questions are answered (see docs/decisions/). Remaining:
1. **Written OK for the handbook.** You have your sister-in-law's OK. For the paper, a short email from the Trust confirming use and credit is worth keeping. The app credits sources accurately (IFRC, handbook, authored) on every step and on /about.
2. **Medical review.** Steps marked `authored` (for example scorpion sting) show "not yet medically reviewed". Have a professional review them, then set `SHOW_AUTHORED_STEPS` as you prefer.
3. **Vision accuracy.** Fit `data/vision/calibration.json` from a labelled animal photo set (notebook 05). Until then confidence is shrunk and capped at 85-90.
4. **Embedding model on Render free tier.** `BAAI/bge-small-en-v1.5` needs roughly 300 MB of RAM. If Render runs out, use a larger plan or host embeddings elsewhere.
5. **Media hosting.** Supabase Storage (1 GB free) or Cloudflare R2 (10 GB free). Set `MEDIA_BASE_URL`.
6. **Hospital data.** Run `python scripts/clean_hospitals.py` on your full file and add verified facts to `data/hospitals/capability_overrides.yaml`.
7. **Age bands.** Confirm infant/child/adult cut-offs in `data/scenarios/age_bands.yaml`.
