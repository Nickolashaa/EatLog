from uuid import UUID

import strawberry

from ....services.exceptions import ObjectNotFound
from ...types.errors import ObjectNotFoundError
from ...types.users import GetUserOrError, User


@strawberry.type
class UsersQuery:
    @strawberry.field
    async def user(
        self,
        id: UUID,
        info: strawberry.Info,
    ) -> GetUserOrError:
        try:
            return User.from_schema(
                instance=await info.context.user_service.get(
                    id=id,
                )
            )
        except ObjectNotFound as e:
            return ObjectNotFoundError.from_exception(e)
