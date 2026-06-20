import strawberry

from .users.queries import UsersQuery


@strawberry.type
class Query(
    UsersQuery,
):
    pass


schema = strawberry.Schema(query=Query)
