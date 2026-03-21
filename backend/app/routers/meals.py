"""Meal-related API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from ..schemas import Category, MealDetail, MealSummary, parse_category, parse_meal_detail, parse_meal_summary
from  ..themealdb_client import MealDBClientError, mealdb_client

router = APIRouter(prefix="/api", tags=["meals"])


def _dict_items(items: list | None) -> list[dict]:
    return [item for item in (items or []) if isinstance(item, dict)]


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/meals/search", response_model=list[MealSummary])
async def search_meals(q: str = Query(..., min_length=1, description="Meal name to search")) -> list[MealSummary]:
    payload = await _handle_upstream(lambda: mealdb_client.search_meals(q))
    meals = _dict_items(payload.get("meals"))
    return [parse_meal_summary(meal) for meal in meals]


async def _handle_upstream(call):
    try:
        return await call()
    except MealDBClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/meals/random", response_model=MealDetail)
async def random_meal() -> MealDetail:
    payload = await _handle_upstream(mealdb_client.get_random_meal)
    meals = _dict_items(payload.get("meals"))
    if not meals:
        raise HTTPException(status_code=502, detail="Random meal unavailable")
    return parse_meal_detail(meals[0])


@router.get("/meals/{meal_id}", response_model=MealDetail)
async def get_meal(meal_id: str) -> MealDetail:
    payload = await _handle_upstream(lambda: mealdb_client.get_meal(meal_id))
    meals = _dict_items(payload.get("meals"))
    if not meals:
        raise HTTPException(status_code=404, detail="Meal not found")
    return parse_meal_detail(meals[0])


@router.get("/categories", response_model=list[Category])
async def list_categories() -> list[Category]:
    payload = await _handle_upstream(mealdb_client.get_categories)
    categories = _dict_items(payload.get("categories"))
    return [parse_category(cat) for cat in categories]


@router.get("/categories/{category}/meals", response_model=list[MealSummary])
async def meals_by_category(category: str) -> list[MealSummary]:
    payload = await _handle_upstream(lambda: mealdb_client.get_meals_by_category(category))
    meals = _dict_items(payload.get("meals"))
    return [parse_meal_summary(meal) for meal in meals]

