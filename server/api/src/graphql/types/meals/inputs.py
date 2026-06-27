import strawberry

from ....services.meals.types import MealCreateParams, MealListFilters


@strawberry.input
class CreateMealInput:
    title: str
    calories: float
    protein: float
    fat: float
    carbohydrate: float

    def to_service_params(self) -> MealCreateParams:
        return MealCreateParams(
            title=self.title,
            calories=self.calories,
            protein=self.protein,
            fat=self.fat,
            carbohydrate=self.carbohydrate,
        )


@strawberry.input
class MealFilters:
    search_query: strawberry.Maybe[str]

    def to_service_params(self) -> MealListFilters:
        params: MealListFilters = {}
        if self.search_query is not None:
            params["search_query"] = self.search_query.value
        return params
