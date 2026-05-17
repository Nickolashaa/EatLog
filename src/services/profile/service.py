import json
from pathlib import Path
from typing import cast

from .types import Kbzhu, Profile

PROFILE_PATH = Path("src/database/profile.json")


class ProfileService:
    @staticmethod
    def exists() -> bool:
        return PROFILE_PATH.exists()

    @staticmethod
    def load() -> Profile:
        with PROFILE_PATH.open(encoding="utf-8") as f:
            return cast(Profile, json.load(f))

    @staticmethod
    def save(profile: Profile) -> None:
        PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with PROFILE_PATH.open("w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

    @staticmethod
    def calculate(profile: Profile) -> Kbzhu:
        w, h, a = profile["weight"], profile["height"], profile["age"]

        if profile["gender"] == "male":
            bmr = 10.0 * w + 6.25 * h - 5.0 * a + 5
        else:
            bmr = 10.0 * w + 6.25 * h - 5.0 * a - 161

        # Moderate activity (3-5 days/week)
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
