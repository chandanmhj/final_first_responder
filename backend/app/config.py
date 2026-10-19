"""Application settings, read from environment variables (see .env.example)."""
import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """All configuration in one place. Every value can be overridden with an environment variable."""

    model_config = SettingsConfigDict(env_file=(REPO_ROOT / ".env", "../.env"), extra="ignore")

    env: str = "development"
    allowed_origins: str = "http://localhost:5173"

    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    auth_disabled: bool = False  # development only: skip token verification

    # Groq (models are chosen by evaluation; see docs/architecture/groq-models.md)
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-120b"
    vision_model: str = "qwen/qwen3.8-27b"
    stt_model: str = "whisper-large-v3-turbo"

    # RAG
    embedding_provider: str = "fastembed"  # fastembed | hash (hash is for tests only)
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dim: int = 384
    retrieval_top_k: int = 6
    abstain_min_overlap: float = 0.12
    retriever: str = "auto"  # auto | memory | supabase

    # Content
    show_authored_steps: bool = True
    data_dir: str = Field(default_factory=lambda: str(REPO_ROOT / "data"))
    media_manifest: str = Field(default_factory=lambda: str(REPO_ROOT / "media" / "manifest.yaml"))
    media_base_url: str = ""

    # Limits
    rate_limit_per_minute: int = 40
    max_image_mb: int = 8
    max_audio_mb: int = 12

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def supabase_ready(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)

    @property
    def groq_ready(self) -> bool:
        return bool(self.groq_api_key)


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
