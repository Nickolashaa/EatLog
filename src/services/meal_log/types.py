from typing import NotRequired, Required, TypedDict


class MealLogCreateParams(TypedDict):
    meal_id: Required[int]
    grams: Required[float]


class MealLogUpdateParams(TypedDict):
    meal_id: NotRequired[int]
    grams: NotRequired[float]


class MealLogTotals(TypedDict):
    calories: float
    protein: float
    fat: float
    carbohydrate: float


class MealLogTableRow(TypedDict):
    log_id: int
    meal_title: str
    grams: float
    calories: float
    protein: float
    fat: float
    carbohydrate: float
