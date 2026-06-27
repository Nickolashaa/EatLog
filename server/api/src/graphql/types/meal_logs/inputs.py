from datetime import date
from uuid import UUID

import strawberry

from ....services.meal_logs.types import (
    MealLogCreateParams,
    MealLogListFilters,
    MealLogUpdateParams,
)


@strawberry.input
class CreateMealLogInput:
    user_id: UUID
    meal_id: int
    grams: float

    def to_service_params(self) -> MealLogCreateParams:
        return MealLogCreateParams(
            user_id=self.user_id,
            meal_id=self.meal_id,
            grams=self.grams,
        )


@strawberry.input
class UpdateMealLogInput:
    user_id: strawberry.Maybe[UUID]
    meal_id: strawberry.Maybe[int]
    grams: strawberry.Maybe[float]

    def to_service_params(self) -> MealLogUpdateParams:
        params: MealLogUpdateParams = {}
        if self.user_id is not None:
            params["user_id"] = self.user_id.value
        if self.meal_id is not None:
            params["meal_id"] = self.meal_id.value
        if self.grams is not None:
            params["grams"] = self.grams.value
        return params


@strawberry.type
class MealLogFilter:
    user_id: strawberry.Maybe[UUID]
    date_filter: strawberry.Maybe[date]

    def to_service_params(self) -> MealLogListFilters:
        params: MealLogListFilters = {}
        if self.user_id is not None:
            params["user_id"] = self.user_id.value
        if self.date_filter is not None:
            params["date_filter"] = self.date_filter.value
        return params
