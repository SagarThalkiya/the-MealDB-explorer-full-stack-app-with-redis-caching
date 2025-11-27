"""HTTP client for interacting with TheMealDB API."""

from __future__ import annotations

from typing import Any

import httpx

from .cache import ResponseCache
from .config import settings


class MealDBClientError(RuntimeError):
    """Raised when TheMealDB upstream call fails."""


class MealDBClient:
    """Handles outbound requests to TheMealDB with caching."""

    def __init__(self) -> None:
        self._base_url = settings.base_api_url
        self._cache = ResponseCache(settings.CACHE_MAX_SIZE, settings.CACHE_TTL_SECONDS)

    async def _request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        *,
        skip_cache: bool = False,
    ) -> dict[str, Any]:
        normalized_params = tuple(sorted((params or {}).items()))
        if not skip_cache:
            cached = self._cache.get(endpoint, normalized_params)
            if cached is not None:
                return cached

        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=10.0) as client:
                response = await client.get(f"/{endpoint}", params=params)
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as exc:
            raise MealDBClientError(f"Upstream request failed for {endpoint}: {exc}") from exc

        if not skip_cache:
            self._cache.set(endpoint, normalized_params, data)
        return data

    async def search_meals(self, query: str) -> dict[str, Any]:
        return await self._request("search.php", {"s": query})

    async def get_categories(self) -> dict[str, Any]:
        return await self._request("categories.php")

    async def get_meals_by_category(self, category: str) -> dict[str, Any]:
        return await self._request("filter.php", {"c": category})

    async def get_meal(self, meal_id: str) -> dict[str, Any]:
        return await self._request("lookup.php", {"i": meal_id})

    async def get_random_meal(self) -> dict[str, Any]:
        return await self._request("random.php", skip_cache=True)


mealdb_client = MealDBClient()

