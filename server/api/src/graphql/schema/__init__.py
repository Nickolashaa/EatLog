import strawberry

from .users.mutations import UsersMutation
from .users.queries import UsersQuery


@strawberry.type
class Query(
    UsersQuery,
):
    pass


@strawberry.type
class Mutation(
    UsersMutation,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
