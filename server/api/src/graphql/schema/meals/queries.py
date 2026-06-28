import strawberry

from ....config import DEFAULT_LIMIT, DEFAULT_OFFSET
from ...context import AppInfo
from ...types.meals import (
    Meal,
    MealFilters,
)


@strawberry.type
class MealsQuery:
    @strawberry.field
    async def meals(
        self,
        info: AppInfo,
        filter: MealFilters | None = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = DEFAULT_OFFSET,
    ) -> list[Meal]:
        return [
            Meal.from_schema(instance)
            for instance in await info.context.services.meal_service.get_list(
                limit=limit,
                offset=offset,
                **filter.to_service_params() if filter is not None else {},
            )
        ]
