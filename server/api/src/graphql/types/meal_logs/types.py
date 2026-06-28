from datetime import datetime
from typing import Self
from uuid import UUID

import strawberry

from ....services.meal_logs.schemas import MealLogSchema
from ...context import AppInfo
from ..meals import Meal
from ..users import User


@strawberry.type
class MealLog:
    id: int
    user_id: strawberry.Private[UUID]
    meal_id: strawberry.Private[int]
    grams: float
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    async def user(self, info: AppInfo) -> User:
        return await info.context.data_loaders.user_data_loader.load(self.user_id)

    @strawberry.field
    async def meal(self, info: AppInfo) -> Meal:
        return await info.context.data_loaders.meal_data_loader.load(self.meal_id)

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
