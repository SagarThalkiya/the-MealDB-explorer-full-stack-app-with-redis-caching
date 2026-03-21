"""Main entrypoint for the FastAPI application."""

from __future__ import annotations
import os  # Added to read env vars
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Using relative imports for Vercel package resolution
from .config import settings
from .routers import meals


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Startup and shutdown logic."""
    yield


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI instance."""
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    # --- CORS CONFIGURATION ---
    # Get the deployed frontend URL from Vercel Env, fallback to local dev
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    origins = [
        frontend_url,
        "http://localhost:5173",  # Vite local default
        "http://127.0.0.1:5173",
    ]
    application.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://the-meal-db-explorer-full-stack-app-ten.vercel.app" # Your Frontend URL
    ],
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


# The FastAPI instance named 'app' for Vercel
app = create_app()