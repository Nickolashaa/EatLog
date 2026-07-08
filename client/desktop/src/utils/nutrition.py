from collections.abc import Iterable
from typing import TypedDict

from gql.client import MealLogFields


class Macros(TypedDict):
    calories: float
    protein: float
    fat: float
    carbohydrate: float


def macros_for_log(log: MealLogFields) -> Macros:
    factor = log.grams / 100
    meal = log.meal
    return {
        "calories": meal.calories * factor,
        "protein": meal.protein * factor,
        "fat": meal.fat * factor,
        "carbohydrate": meal.carbohydrate * factor,
    }


def sum_macros(logs: Iterable[MealLogFields]) -> Macros:
    totals: Macros = {"calories": 0.0, "protein": 0.0, "fat": 0.0, "carbohydrate": 0.0}
    for log in logs:
        m = macros_for_log(log)
        totals["calories"] += m["calories"]
        totals["protein"] += m["protein"]
        totals["fat"] += m["fat"]
        totals["carbohydrate"] += m["carbohydrate"]
    return totals
