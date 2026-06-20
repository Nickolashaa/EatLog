from typing import NotRequired, Required, TypedDict


class MealListFilters(TypedDict):
    search_query: NotRequired[str]


class MealCreateParams(TypedDict):
    title: Required[str]
    calories: Required[float]
    protein: Required[float]
    fat: Required[float]
    carbohydrate: Required[float]


class MealUpdateParams(TypedDict):
    title: NotRequired[str]
    calories: NotRequired[float]
    protein: NotRequired[float]
    fat: NotRequired[float]
    carbohydrate: NotRequired[float]
