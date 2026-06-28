import strawberry

from .meal_logs.mutations import MealLogsMutation
from .meal_logs.queries import MealLogsQuery
from .meals.mutations import MealsMutation
from .meals.queries import MealsQuery
from .users.mutations import UsersMutation
from .users.queries import UsersQuery


@strawberry.type
class Query(
    UsersQuery,
    MealsQuery,
    MealLogsQuery,
):
    pass


@strawberry.type
class Mutation(
    UsersMutation,
    MealsMutation,
    MealLogsMutation,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
