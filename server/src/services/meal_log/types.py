from datetime import date
from typing import NotRequired, Required, TypedDict
from uuid import UUID


class MealLogListFilters(TypedDict):
    date_filter: NotRequired[date]
    offset: NotRequired[int]


class MealLogCreateParams(TypedDict):
    user_id: Required[UUID]
    meal_id: Required[int]
    grams: Required[float]


class MealLogUpdateParams(TypedDict):
    meal_id: NotRequired[int]
    grams: NotRequired[float]
