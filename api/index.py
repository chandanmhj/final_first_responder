"""Vercel entry point (v2): exposes the FastAPI app from backend/app."""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_found = None
for _root in (_here, os.path.dirname(_here), "/var/task"):
    _cand = os.path.join(_root, "backend")
    if os.path.isfile(os.path.join(_cand, "app", "main.py")):
        _found = _cand
        break
if _found is None:
    raise RuntimeError(f"ENTRY V2: backend/app/main.py not found. Looked in {_here}; files there: {sorted(os.listdir(_here))[:30]}")
sys.path.insert(0, _found)

from app.main import app  # noqa: E402,F401