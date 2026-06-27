from uuid import UUID

from strawberry.dataloader import DataLoader

from ...services.users import UserService
from ...services.users.schemas import UserSchema
from ..types.users import User

type USER_DATA_LOADER = DataLoader[UUID, User]


def build_user_data_loader(user_service: UserService) -> USER_DATA_LOADER:
    async def load_users(
        keys: list[UUID],
    ) -> list[User]:
        id_to_user: dict[UUID, UserSchema] = {
            user.id: user for user in await user_service.get_list(ids=keys)
        }

        return [
            User.from_schema(instance) for instance in [id_to_user[key] for key in keys]
        ]

    return DataLoader(load_fn=load_users)
