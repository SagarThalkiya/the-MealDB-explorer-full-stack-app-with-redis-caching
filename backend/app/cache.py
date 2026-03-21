"""Hybrid cache supporting Redis (Production) and TTLCache (Local)."""

from __future__ import annotations
import os
import json
import redis
from threading import RLock
from typing import Any, Hashable
from cachetools import TTLCache
from .config import settings

class ResponseCache:
    """Thread-safe cache wrapper with Redis support."""

    def __init__(self, maxsize: int, ttl: int) -> None:
        self.ttl = ttl
        self._local_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = RLock()
        
        # Initialize Redis
        self.redis_client = None
        if settings.REDIS_URL:
            try:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL, 
                    decode_responses=True,
                    socket_timeout=2
                )
                self.redis_client.ping()
                print("Successfully connected to Redis")
            except Exception as e:
                print(f"Redis connection failed, falling back to local cache: {e}")
                self.redis_client = None

    def _make_key(self, endpoint: str, params: Any) -> str:
        # Redis keys must be strings
        return f"cache:{endpoint}:{hash(params)}"

    def get(self, endpoint: str, params: Any = None) -> Any | None:
        key = self._make_key(endpoint, params)
        
        # 1. Try Redis
        if self.redis_client:
            try:
                data = self.redis_client.get(key)
                return json.loads(data) if data else None
            except Exception:
                pass # Fallback to local if Redis fails mid-request
        
        # 2. Try Local Memory
        with self._lock:
            return self._local_cache.get(key)

    def set(self, endpoint: str, params: Any, value: Any) -> None:
        key = self._make_key(endpoint, params)
        
        # 1. Set in Redis
        if self.redis_client:
            try:
                self.redis_client.setex(key, self.ttl, json.dumps(value))
            except Exception:
                pass
        
        # 2. Set in Local Memory
        with self._lock:
            self._local_cache[key] = value