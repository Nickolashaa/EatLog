from uuid import UUID

import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AppInfo
from ...types.errors import ObjectNotFoundError
from ...types.users import GetUserOrError, User, UsersFilterInput


@strawberry.type
class UsersQuery:
    @strawberry.field
    async def user(
        self,
        id: UUID,
        info: AppInfo,
    ) -> GetUserOrError:
        try:
            return User.from_schema(
                instance=await info.context.services.user_service.get(
                    id=id,
                )
            )
        except ObjectNotFound as e:
            return ObjectNotFoundError.from_exception(e)

    @strawberry.field
    async def user_by_telegram_id(
        self,
        telegram_id: str,
        info: AppInfo,
    ) -> GetUserOrError:
        try:
            return User.from_schema(
                instance=await info.context.services.user_service.get_by_telegram_id(
                    telegram_id=telegram_id,
                )
            )
        except ObjectNotFound as e:
            return ObjectNotFoundError.from_exception(e)

    @strawberry.field
    async def users(
        self,
        info: AppInfo,
        filter: UsersFilterInput | None = None,
    ) -> list[User]:
        return [
            User.from_schema(instance)
            for instance in await info.context.services.user_service.get_list(
                **filter.to_service_params() if filter is not None else {},
            )
        ]
