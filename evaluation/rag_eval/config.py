"""Paths used by the evaluation harness."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "backend"))
DATA = os.path.join(ROOT, "data")
OUT_RESULTS = os.path.join(ROOT, "docs", "evaluation", "results")
OUT_FIGURES = os.path.join(ROOT, "docs", "evaluation", "figures")
