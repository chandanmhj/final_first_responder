"""Logging setup."""
import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Log to stdout in a simple one-line format."""
    logging.basicConfig(level=level, stream=sys.stdout, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
