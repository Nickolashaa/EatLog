import strawberry

from ....services.exceptions import ObjectAlreadyExists
from ...context import AppInfo
from ...types.errors import ObjectAlreadyExistsError
from ...types.meals import CreateMealInput, CreateMealOrError, Meal


@strawberry.type
class MealsMutation:
    @strawberry.mutation
    async def create_meal(
        self,
        info: AppInfo,
        input: CreateMealInput,
    ) -> CreateMealOrError:
        try:
            instance = await info.context.services.meal_service.create(
                **input.to_service_params(),
            )
            await info.context.session.commit()
            return Meal.from_schema(instance)
        except ObjectAlreadyExists as e:
            await info.context.session.rollback()
            return ObjectAlreadyExistsError.from_exception(e)
