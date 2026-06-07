from typing import TypedDict


class MealData(TypedDict):
    id: int
    title: str
    calories: float
    protein: float
    fat: float
    carbohydrate: float


class MealInput(TypedDict):
    title: str
    calories: float
    protein: float
    fat: float
    carbohydrate: float


class MealListParams(TypedDict, total=False):
    search: str
    limit: int


class MealUpdateParams(TypedDict):
    meal_id: int
    data: MealInput
