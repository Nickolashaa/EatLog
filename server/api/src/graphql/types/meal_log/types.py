from datetime import datetime
from typing import Self
from uuid import UUID

import strawberry

from ....services.meal_log.schemas import MealLogSchema


@strawberry.type
class MealLog:
    id: int
    user_id: strawberry.Private[UUID]
    meal_id: strawberry.Private[int]
    grams: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_schema(cls, instance: MealLogSchema) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            meal_id=instance.meal_id,
            grams=instance.grams,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
