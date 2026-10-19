# Evaluation methodology

Status: **Proposed**. Finalized in Phase 2 together with you.

## Principles
- Change one variable at a time.
- Freeze the test set early; use the dev set for tuning.
- Multiple seeds, bootstrap confidence intervals, paired significance tests.
- If an LLM is used as a judge, validate it against human labels on a subset.
- Every figure records timestamp, git commit and configuration.

## Variants to compare (candidates)
LLM only, BM25, dense, hybrid, hybrid + reranker, scenario-aware, step-structured chunking, query rewriting, abstention, citation-enforced generation. Code placeholders are in `evaluation/rag_eval/variants/`.

## Metrics
- Retrieval: recall@k, MRR, nDCG
- Generation: faithfulness, step-order accuracy, completeness, citation correctness
- Safety: hallucinated steps, unsafe advice, correct refusals, critical-error rate
- Images: identification accuracy and calibration on bite/sting photos
- Efficiency: p50/p95 latency, tokens per query, cost, memory, cold start

## Notebooks
`evaluation/notebooks/00` to `09`. Outputs go to `docs/evaluation/figures/` and `docs/evaluation/results/`; `REPORT.md` is generated from them.

## Planned figures
Retrieval metrics per variant with error bars, recall heatmap by scenario, ablation chart, quality-versus-latency scatter with Pareto frontier, latency distributions, safety chart, scenario classifier confusion matrix, top-k and chunk-size sweeps, confidence histogram for the abstention threshold, pipeline diagram.
