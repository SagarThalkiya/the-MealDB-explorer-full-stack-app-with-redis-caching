"""Simple in-memory response cache with TTL support."""

from __future__ import annotations

from threading import RLock
from typing import Any, Hashable

from cachetools import TTLCache


class ResponseCache:
    """Thread-safe TTL cache wrapper."""

    def __init__(self, maxsize: int, ttl: int) -> None:
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = RLock()

    def _make_key(self, endpoint: str, params: tuple[tuple[str, Any], ...] | None) -> Hashable:
        return endpoint, params

    def get(self, endpoint: str, params: tuple[tuple[str, Any], ...] | None = None) -> Any | None:
        key = self._make_key(endpoint, params)
        with self._lock:
            return self._cache.get(key)

    def set(
        self,
        endpoint: str,
        params: tuple[tuple[str, Any], ...] | None,
        value: Any,
    ) -> None:
        key = self._make_key(endpoint, params)
        with self._lock:
            self._cache[key] = value

