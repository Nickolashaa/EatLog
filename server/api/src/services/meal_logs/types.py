from datetime import date
from typing import NotRequired, Required, TypedDict
from uuid import UUID


class MealLogListFilters(TypedDict):
    user_id: NotRequired[UUID]
    exclude_user_ids: NotRequired[list[UUID]]
    date_filter: NotRequired[date]


class MealLogCreateParams(TypedDict):
    user_id: Required[UUID]
    meal_id: Required[int]
    grams: Required[float]


class MealLogUpdateParams(TypedDict):
    user_id: NotRequired[UUID]
    meal_id: NotRequired[int]
    grams: NotRequired[float]
