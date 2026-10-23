"""Vercel entry point: exposes the FastAPI app from backend/app."""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
for _base in (_here, os.path.dirname(_here)):  # works whether Vercel runs this as /index.py or /api/index.py
    _backend = os.path.join(_base, "backend")
    if os.path.isdir(_backend):
        sys.path.insert(0, _backend)
        break
else:
    raise RuntimeError(f"backend folder not found. Looked in {_here} (contents: {sorted(os.listdir(_here))[:30]})")

from app.main import app  # noqa: E402,F401