# Groq models

Source: Groq documentation (console.groq.com/docs/models), read on 2026-10-06. This list changes often.
The live list is available from `https://api.groq.com/openai/v1/models`.

Status: Groq is **Decided** as the provider. **No model has been chosen.** Models are chosen by evaluation in Phase 3.

## Text and reasoning
| Model id | Status | Notes |
|---|---|---|
| `openai/gpt-oss-120b` | Production | 131k context, 65k max output, reasoning, tool use. Featured model. |
| `openai/gpt-oss-20b` | Production | Faster and cheaper, same context. |
| `llama-3.3-70b-versatile` | Production (Enterprise: contact sales) | 131k context. |
| `llama-3.1-8b-instant` | Production (Enterprise: contact sales) | Fastest, 131k context. |
| `minimaxai/minimax-m2.7` | Preview (Enterprise) | 196k context. |
| `groq/compound`, `groq/compound-mini` | Systems with built-in web search and code execution | Not suited to a closed guideline knowledge base. |

## Vision (images)
| Model id | Status | Notes |
|---|---|---|
| `qwen/qwen3.8-27b` | **Preview** | Image input, 20 MB max file, 131k context. Preview models are for evaluation and may be discontinued at short notice. |
| `qwen/qwen3.6-27b` | Listed on the vision page | Check whether it is still available. |

## Speech
| Model id | Status | Notes |
|---|---|---|
| `whisper-large-v3-turbo` | Production | Speech-to-text, 100 MB max file. Candidate for hands-free mode. |
| `whisper-large-v3` | Production | More accurate, slower. |
| `canopylabs/orpheus-v1-english` | Preview | Text-to-speech, English. A more natural alternative to browser voice if you later want it. |

## Safety
| Model id | Status | Notes |
|---|---|---|
| `openai/gpt-oss-safeguard-20b` | Preview | Safety classification. |
| `meta-llama/llama-prompt-guard-2-22m`, `-86m` | Preview | Prompt-injection detection. |

## Important findings
- **Groq lists no embedding model and no reranker.** The RAG system needs a separate embedding model (open question 5).
- The only vision models are **preview**, which is a risk for the animal photo feature in a deployed app.
- Whisper is available for the server-side speech-to-text you chose.
