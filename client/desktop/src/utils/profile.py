from typing import TypedDict

from PyQt6.QtCore import QSettings

from ..graphql.client import Gender, Goal


def _settings() -> QSettings:
    return QSettings("EatLog", "EatLog")


def profile_exists() -> bool:
    return bool(_settings().value("profile/uuid"))


def get_uuid() -> str:
    return str(_settings().value("profile/uuid"))


def set_uuid(uuid: str) -> None:
    _settings().setValue("profile/uuid", uuid)


class Kbzhu(TypedDict):
    calories: int
    protein: int
    fat: int
    carbohydrate: int


def calculate_kbzhu(
    *, gender: Gender, weight: float, height: float, age: int, goal: Goal
) -> Kbzhu:
    if gender == Gender.MALE:
        bmr = 10.0 * weight + 6.25 * height - 5.0 * age + 5
    else:
        bmr = 10.0 * weight + 6.25 * height - 5.0 * age - 161

    tdee = bmr * 1.55

    if goal == Goal.LOSE:
        calories = tdee - 500
        protein_ratio = 2.2
    elif goal == Goal.GAIN:
        calories = tdee + 300
        protein_ratio = 2.2
    else:
        calories = tdee
        protein_ratio = 2.0

    protein = weight * protein_ratio
    fat = calories * 0.25 / 9
    carbohydrate = (calories - protein * 4 - fat * 9) / 4

    return {
        "calories": round(calories),
        "protein": round(protein),
        "fat": round(fat),
        "carbohydrate": max(0, round(carbohydrate)),
    }
