from strawberry.dataloader import DataLoader

from ...services.meals import MealService
from ...services.meals.schemas import MealSchema
from ..types.meals import Meal

type MEAL_DATA_LOADER = DataLoader[int, Meal]


def build_meal_data_loader(meal_service: MealService) -> MEAL_DATA_LOADER:
    async def load_users(
        keys: list[int],
    ) -> list[Meal]:
        id_to_meal: dict[int, MealSchema] = {
            meal.id: meal for meal in await meal_service.get_list(ids=keys)
        }

        return [
            Meal.from_schema(instance) for instance in [id_to_meal[key] for key in keys]
        ]

    return DataLoader(load_fn=load_users)
