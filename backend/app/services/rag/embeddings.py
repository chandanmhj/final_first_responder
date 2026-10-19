"""Text embeddings. The default provider runs a small ONNX model locally (fastembed)."""
import hashlib
import re

import numpy as np

from ...config import Settings


class EmbeddingProvider:
    """Interface: turn texts into unit-length vectors."""

    dim = 384

    def embed(self, texts: list[str]) -> np.ndarray:
        raise NotImplementedError


class HashEmbeddingProvider(EmbeddingProvider):
    """Deterministic bag-of-words hashing. For tests and offline development only; not a real semantic model."""

    def __init__(self, dim: int = 384):
        self.dim = dim

    def embed(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            for w in re.findall(r"[a-z0-9]+", t.lower()):
                h = int(hashlib.md5(w.encode()).hexdigest(), 16)
                out[i, h % self.dim] += 1.0
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.maximum(norms, 1e-9)


class FastEmbedProvider(EmbeddingProvider):
    """Local ONNX embeddings (BAAI/bge-small-en-v1.5 by default, 384 dimensions)."""

    def __init__(self, model_name: str, dim: int = 384):
        self.dim, self.model_name, self._model = dim, model_name, None

    def _load(self):
        if self._model is None:
            from fastembed import TextEmbedding  # imported lazily: heavy

            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def embed(self, texts: list[str]) -> np.ndarray:
        vecs = np.array(list(self._load().embed(texts)), dtype=np.float32)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs / np.maximum(norms, 1e-9)


def get_embedder(settings: Settings) -> EmbeddingProvider:
    """Create the configured embedding provider."""
    if settings.embedding_provider == "hash":
        return HashEmbeddingProvider(settings.embedding_dim)
    return FastEmbedProvider(settings.embedding_model, settings.embedding_dim)
