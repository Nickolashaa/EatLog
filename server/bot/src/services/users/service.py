from uuid import UUID

from aiohttp import ClientSession

from ...schemas.users import UserRegister, UserResponse
from ..exceptions import ObjectNotFound


class UserService:
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> UserResponse:
        async with self.session.get(f"/users/by-telegram/{telegram_id}") as res:
            if res.status == 404:
                raise ObjectNotFound(message="User not found", telegram_id=telegram_id)
            res.raise_for_status()
            return UserResponse.model_validate(await res.json())

    async def register(self, id: UUID, telegram_id: int) -> UserResponse:
        payload = UserRegister(id=id, telegram_id=telegram_id)
        async with self.session.post(
            "/users/register", json=payload.model_dump(mode="json")
        ) as res:
            if res.status == 404:
                raise ObjectNotFound(message="User not found", id=id)
            res.raise_for_status()
            return UserResponse.model_validate(await res.json())
