from typing import NotRequired, Required, TypedDict


class MealListFilters(TypedDict):
    search_query: NotRequired[str]


class MealCreateParams(TypedDict):
    title: Required[str]
    calories: Required[float]
    protein: Required[float]
    fat: Required[float]
    carbohydrate: Required[float]
