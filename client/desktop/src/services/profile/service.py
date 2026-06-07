from typing import Literal, cast

from PyQt6.QtCore import QSettings

from .types import Kbzhu, Profile, ProfileBase


class ProfileService:
    @staticmethod
    def exists() -> bool:
        return bool(QSettings("EatLog", "EatLog").value("profile/uuid"))

    @staticmethod
    def load() -> Profile:
        s = QSettings("EatLog", "EatLog")
        return {
            "uuid": str(s.value("profile/uuid")),
            "gender": cast(Literal["male", "female"], s.value("profile/gender")),
            "weight": float(s.value("profile/weight")),
            "height": float(s.value("profile/height")),
            "age": int(s.value("profile/age")),
            "goal": cast(Literal["maintain", "lose", "gain"], s.value("profile/goal")),
        }

    @staticmethod
    def save(profile: Profile) -> None:
        s = QSettings("EatLog", "EatLog")
        s.setValue("profile/uuid", profile["uuid"])
        s.setValue("profile/gender", profile["gender"])
        s.setValue("profile/weight", profile["weight"])
        s.setValue("profile/height", profile["height"])
        s.setValue("profile/age", profile["age"])
        s.setValue("profile/goal", profile["goal"])

    @staticmethod
    def calculate(profile: ProfileBase) -> Kbzhu:
        w, h, a = profile["weight"], profile["height"], profile["age"]

        if profile["gender"] == "male":
            bmr = 10.0 * w + 6.25 * h - 5.0 * a + 5
        else:
            bmr = 10.0 * w + 6.25 * h - 5.0 * a - 161

        tdee = bmr * 1.55

        goal = profile["goal"]
        if goal == "lose":
            calories = tdee - 500
            protein_ratio = 2.2
        elif goal == "gain":
            calories = tdee + 300
            protein_ratio = 2.2
        else:
            calories = tdee
            protein_ratio = 2.0

        protein = w * protein_ratio
        fat = calories * 0.25 / 9
        carbohydrate = (calories - protein * 4 - fat * 9) / 4

        return {
            "calories": round(calories),
            "protein": round(protein),
            "fat": round(fat),
            "carbohydrate": max(0, round(carbohydrate)),
        }
