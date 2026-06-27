import strawberry

from ....services.meals.types import MealCreateParams, MealListFilters, MealUpdateParams


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
class UpdateMealInput:
    title: strawberry.Maybe[str]
    calories: strawberry.Maybe[float]
    protein: strawberry.Maybe[float]
    fat: strawberry.Maybe[float]
    carbohydrate: strawberry.Maybe[float]

    def to_service_params(self) -> MealUpdateParams:
        params: MealUpdateParams = {}
        if self.title is not None:
            params["title"] = self.title.value
        if self.calories is not None:
            params["calories"] = self.calories.value
        if self.protein is not None:
            params["protein"] = self.protein.value
        if self.fat is not None:
            params["fat"] = self.fat.value
        if self.carbohydrate is not None:
            params["carbohydrate"] = self.carbohydrate.value
        return params


@strawberry.input
class MealFilters:
    search_query: strawberry.Maybe[str]

    def to_service_params(self) -> MealListFilters:
        params: MealListFilters = {}
        if self.search_query is not None:
            params["search_query"] = self.search_query.value
        return params
