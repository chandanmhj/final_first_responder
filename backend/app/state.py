"""Builds and holds the long-lived services."""
from dataclasses import dataclass

from .config import Settings
from .core.rate_limit import RateLimiter
from .core.security import TokenVerifier
from .db.repositories import MemoryRepository, SupabaseRepository, make_supabase_client
from .services.conversation.chat_service import ChatService
from .services.hospitals.finder import HospitalIndex
from .services.media.step_media_resolver import StepMediaResolver
from .services.rag.embeddings import get_embedder
from .services.rag.generation import GroqClient
from .services.rag.pipeline import RagPipeline
from .services.rag.retrieval import build_retriever
from .services.scenarios.loader import ScenarioStore


@dataclass
class Services:
    """Everything the routes need."""

    settings: Settings
    store: ScenarioStore
    repo: object
    llm: GroqClient
    rag: RagPipeline
    hospitals: HospitalIndex
    media: StepMediaResolver
    chat: ChatService
    verifier: TokenVerifier
    limiter: RateLimiter


def build_services(settings: Settings, repo=None, llm: GroqClient | None = None) -> Services:
    """Create all services from settings. Pass repo/llm to override them (tests)."""
    store = ScenarioStore(settings.data_dir)
    client = None
    if repo is None:
        if settings.supabase_ready:
            client = make_supabase_client(settings.supabase_url, settings.supabase_service_role_key)
            repo = SupabaseRepository(client)
        else:
            repo = MemoryRepository()
    elif settings.supabase_ready:
        client = None
    llm = llm or GroqClient(settings)
    embedder = get_embedder(settings)
    retriever = build_retriever(settings, embedder, client)
    rag = RagPipeline(retriever, llm, settings.retrieval_top_k, settings.abstain_min_overlap)
    hospitals = HospitalIndex(settings.data_dir)
    media = StepMediaResolver(settings.media_manifest, settings.media_base_url)
    chat = ChatService(settings, store, repo, llm, rag, hospitals, media)
    return Services(settings, store, repo, llm, rag, hospitals, media, chat, TokenVerifier(settings), RateLimiter(settings.rate_limit_per_minute))
