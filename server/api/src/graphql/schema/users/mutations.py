from uuid import UUID

import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AppInfo
from ...types.errors import ObjectNotFoundError
from ...types.users import CreateUserInput, UpdateUserInput, UpdateUserOrError, User


@strawberry.type
class UsersMutation:
    @strawberry.mutation
    async def create_user(
        self,
        info: AppInfo,
        input: CreateUserInput,
    ) -> User:
        instance = await info.context.user_service.create(**input.to_create_params())
        await info.context.session.commit()
        return User.from_schema(instance)

    @strawberry.mutation
    async def update_user(
        self,
        info: AppInfo,
        id: UUID,
        input: UpdateUserInput,
    ) -> UpdateUserOrError:
        try:
            instance = await info.context.user_service.update(
                id=id, **input.to_update_params()
            )
            await info.context.session.commit()
            return User.from_schema(instance)
        except ObjectNotFound as e:
            return ObjectNotFoundError.from_exception(e)

    @strawberry.mutation
    async def delete_user(
        self,
        info: AppInfo,
        id: UUID,
    ) -> None:
        await info.context.user_service.delete(id)
        await info.context.session.commit()
