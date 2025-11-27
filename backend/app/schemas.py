"""Pydantic schemas for API responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, HttpUrl


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == "null":
        return None
    return text


class Ingredient(BaseModel):
    name: str
    measure: str | None = None


class MealSummary(BaseModel):
    id: str
    name: str
    category: str | None = None
    area: str | None = None
    thumbnail: HttpUrl | None = None


class MealDetail(MealSummary):
    instructions: str | None = None
    tags: list[str] = []
    youtube: HttpUrl | None = None
    source: HttpUrl | None = None
    ingredients: list[Ingredient] = []


class Category(BaseModel):
    id: str
    name: str
    description: str | None = None
    thumbnail: HttpUrl | None = None


def _collect_ingredients(meal: dict[str, Any]) -> list[Ingredient]:
    ingredients: list[Ingredient] = []
    for idx in range(1, 21):
        name_key = f"strIngredient{idx}"
        measure_key = f"strMeasure{idx}"
        name = _clean(meal.get(name_key)) or ""
        measure = _clean(meal.get(measure_key))
        if name:
            ingredients.append(Ingredient(name=name, measure=measure))
    return ingredients


def parse_meal_summary(meal: dict[str, Any]) -> MealSummary:
    return MealSummary(
        id=_clean(meal.get("idMeal")) or "",
        name=_clean(meal.get("strMeal")) or "",
        category=_clean(meal.get("strCategory")),
        area=_clean(meal.get("strArea")),
        thumbnail=_clean(meal.get("strMealThumb")),
    )


def parse_meal_detail(meal: dict[str, Any]) -> MealDetail:
    return MealDetail(
        **parse_meal_summary(meal).model_dump(),
        instructions=_clean(meal.get("strInstructions")),
        tags=[tag.strip() for tag in (meal.get("strTags") or "").split(",") if tag.strip()],
        youtube=_clean(meal.get("strYoutube")),
        source=_clean(meal.get("strSource")),
        ingredients=_collect_ingredients(meal),
    )


def parse_category(category: dict[str, Any]) -> Category:
    return Category(
        id=_clean(category.get("idCategory")) or "",
        name=_clean(category.get("strCategory")) or "",
        description=_clean(category.get("strCategoryDescription")),
        thumbnail=_clean(category.get("strCategoryThumb")),
    )

