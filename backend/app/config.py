"""Application configuration settings."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from project root or current directory
# Since we might run this from the backend folder or project root
# search upwards from the current file's directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


class Settings:
    """Basic settings loaded from environment variables."""

    THEMEALDB_BASE_URL: str = "https://www.themealdb.com/api/json/v1"
    API_KEY: str = os.getenv("MEALDB_API_KEY", "1")
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "256"))
    APP_NAME: str = "TheMealDB Explorer API"
    APP_VERSION: str = "1.0.0"

    @property
    def base_api_url(self) -> str:
        return f"{self.THEMEALDB_BASE_URL}/{self.API_KEY}"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()

