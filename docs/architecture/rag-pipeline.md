# RAG pipeline

The RAG system is the most important part of the project and the basis of the paper.

## Requirements (Decided)
- Answers come from the guidelines and cite them.
- State of the art, and measured so the paper can prove it.
- Missing guideline data is added manually by you.
- Image questions (for example a bite photo) combine the image with the guideline knowledge.
- Small talk is handled outside the guideline pipeline.

## Candidate techniques (Proposed, to be evaluated, not assumed)
Hybrid retrieval, reranking, scenario-aware filtering, step-structured chunking, contextual chunk enrichment, query rewriting, abstention on low confidence, and citation-enforced generation. See docs/evaluation/methodology.md.

## Process
Nothing is chosen because it sounds good. Each technique earns its place through the evaluation notebooks.
