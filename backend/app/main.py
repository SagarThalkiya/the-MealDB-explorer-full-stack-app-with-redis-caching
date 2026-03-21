"""Main entrypoint for the FastAPI application."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Using absolute imports to ensure compatibility with Vercel/Serverless environments
from .config import settings
from .routers import meals


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Useful for initializing connection pools, caches, etc.
    """
    # Startup logic here
    yield
    # Shutdown logic here


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI instance."""
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    application.include_router(meals.router)

    @application.get("/")
    async def root():
        return {
            "message": "Welcome to the MealDB Explorer API",
            "docs": "/api/docs",
            "version": settings.APP_VERSION,
        }

    return application


# The FastAPI instance named 'app' for Vercel and other WSGI/ASGI servers
app = create_app()
