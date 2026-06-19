from PyQt6.QtCore import QSettings

from .types import Kbzhu, Profile, ProfileBase


class ProfileService:
    _cache: Profile | None = None

    @staticmethod
    def exists() -> bool:
        return bool(QSettings("EatLog", "EatLog").value("profile/uuid"))

    @staticmethod
    def uuid() -> str:
        return str(QSettings("EatLog", "EatLog").value("profile/uuid"))

    @classmethod
    def set_uuid(cls, uuid: str) -> None:
        QSettings("EatLog", "EatLog").setValue("profile/uuid", uuid)

    @classmethod
    def load(cls) -> Profile:
        if cls._cache is None:
            from ..users import UserApiService

            cls._cache = UserApiService.get(cls.uuid())
        return cls._cache

    @classmethod
    def set_cache(cls, profile: Profile) -> None:
        cls._cache = profile

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
