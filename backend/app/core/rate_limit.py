"""A small in-memory sliding-window rate limiter (per process)."""
import time
from collections import defaultdict, deque

from .errors import TooManyRequests


class RateLimiter:
    """Allow at most `limit` calls per key per `window` seconds."""

    def __init__(self, limit: int, window: float = 60.0):
        self.limit, self.window = limit, window
        self._hits: dict[str, deque] = defaultdict(deque)

    def check(self, key: str) -> None:
        """Raise TooManyRequests when the key has exceeded its allowance."""
        now = time.monotonic()
        q = self._hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.limit:
            raise TooManyRequests("Too many requests. Please wait a moment.")
        q.append(now)
