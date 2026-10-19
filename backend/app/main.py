"""FastAPI application entry point.  Run: uvicorn app.main:app --reload"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import chat, health, hospitals, incidents, me, media, scenarios, sessions, voice
from .config import Settings, get_settings
from .core.errors import install_error_handlers
from .core.logging import setup_logging
from .state import Services, build_services


def create_app(settings: Settings | None = None, services: Services | None = None) -> FastAPI:
    """Build the app. Tests pass their own settings or services."""
    settings = settings or get_settings()
    setup_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.services = services or build_services(settings)
        yield

    app = FastAPI(title="First Responder API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    install_error_handlers(app)
    app.include_router(health.router)
    app.include_router(health.router, prefix="/api")
    for r in (me, sessions, chat, voice, media, hospitals, incidents, scenarios):
        app.include_router(r.router)
    return app


app = create_app()
