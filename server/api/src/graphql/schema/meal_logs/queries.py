import strawberry

from ....config import DEFAULT_LIMIT, DEFAULT_OFFSET
from ...context import AppInfo
from ...types.meal_logs import (
    MealLog,
    MealLogFilter,
)


@strawberry.type
class MealLogsQuery:
    @strawberry.field
    async def meal_logs(
        self,
        info: AppInfo,
        filter: MealLogFilter | None = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = DEFAULT_OFFSET,
    ) -> list[MealLog]:
        return [
            MealLog.from_schema(instance)
            for instance in await info.context.services.meal_log_service.get_list(
                limit=limit,
                offset=offset,
                **filter.to_service_params() if filter is not None else {},
            )
        ]
