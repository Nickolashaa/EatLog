from datetime import datetime
from typing import Self

import strawberry

from ....services.meals.schemas import MealSchema


@strawberry.type
class Meal:
    id: int
    title: str
    calories: float
    protein: float
    fat: float
    carbohydrate: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_schema(cls, instance: MealSchema) -> Self:
        return cls(
            id=instance.id,
            title=instance.title,
            calories=instance.calories,
            protein=instance.protein,
            fat=instance.fat,
            carbohydrate=instance.carbohydrate,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
