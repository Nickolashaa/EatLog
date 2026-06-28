import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AppInfo
from ...types.errors import ObjectNotFoundError
from ...types.meal_logs import (
    CreateMealLogInput,
    CreateMealLogOrError,
    MealLog,
    UpdateMealLogInput,
    UpdateMealLogOrError,
)


@strawberry.type
class MealLogsMutation:
    @strawberry.mutation
    async def create_meal_log(
        self,
        info: AppInfo,
        input: CreateMealLogInput,
    ) -> CreateMealLogOrError:
        try:
            instance = await info.context.services.meal_log_service.create(
                **input.to_service_params(),
            )
            await info.context.session.commit()
            return MealLog.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_exception(e)

    @strawberry.mutation
    async def update_meal_log(
        self,
        info: AppInfo,
        id: int,
        input: UpdateMealLogInput,
    ) -> UpdateMealLogOrError:
        try:
            instance = await info.context.services.meal_log_service.update(
                id=id,
                **input.to_service_params(),
            )
            await info.context.session.commit()
            return MealLog.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_exception(e)

    @strawberry.mutation
    async def delete_meal_log(
        self,
        info: AppInfo,
        id: int,
    ) -> None:
        await info.context.services.meal_log_service.delete(id)
        await info.context.session.commit()
