# 0007. RAG evaluation in notebooks that write to docs

- Status: Decided
- Decided by: Chandan
- Date: 2026-10-05

## Context
How to evaluate and document the RAG system.

## Decision
A notebook folder that tests each model/variant, draws diagrams and visualizations, and stores them in the documentation folder.

## Consequences
Core logic sits in the rag_eval package so the same code can run headless.
