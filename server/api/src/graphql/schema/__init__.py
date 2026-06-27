import strawberry

from .meals.mutations import MealsMutation
from .meals.queries import MealsQuery
from .users.mutations import UsersMutation
from .users.queries import UsersQuery


@strawberry.type
class Query(
    UsersQuery,
    MealsQuery,
):
    pass


@strawberry.type
class Mutation(
    UsersMutation,
    MealsMutation,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
