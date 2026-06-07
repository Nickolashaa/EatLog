import datetime
from typing import NotRequired, TypedDict


class MealLogTableRow(TypedDict):
    log_id: int
    meal_id: int
    meal_title: str
    grams: float
    calories: float
    protein: float
    fat: float
    carbohydrate: float


class MealLogTotals(TypedDict):
    calories: float
    protein: float
    fat: float
    carbohydrate: float


class MealLogTableParams(TypedDict):
    user_id: str
    date_filter: NotRequired[datetime.date]


class MealLogTotalsParams(TypedDict):
    user_id: str
    target_date: datetime.date


class MealLogCreateParams(TypedDict):
    user_id: str
    meal_id: int
    grams: float


class MealLogUpdateParams(TypedDict):
    log_id: int
    meal_id: int
    grams: float
    user_id: str
