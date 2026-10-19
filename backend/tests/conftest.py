import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "scripts"))

from app.config import Settings  # noqa: E402
from app.main import create_app  # noqa: E402


@pytest.fixture(scope="session")
def settings():
    return Settings(env="test", auth_disabled=True, embedding_provider="hash", groq_api_key="", supabase_url="",
                    supabase_service_role_key="", media_base_url="https://media.example.com")


@pytest.fixture()
def client(settings):
    app = create_app(settings)
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def store(settings):
    from app.services.scenarios.loader import ScenarioStore

    return ScenarioStore(settings.data_dir)
