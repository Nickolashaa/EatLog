from typing import Unpack
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.users import User
from ..exceptions import ObjectNotFound
from .schemas import UserResponse
from .types import UserCreateParams, UserUpdateParams


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: UUID) -> UserResponse:
        stmt = select(User).where(User.id == id)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="User not found", id=id)
        return UserResponse.model_validate(instance, from_attributes=True)

    async def get_by_telegram_id(self, telegram_id: str) -> UserResponse:
        stmt = select(User).where(User.telegram_id == telegram_id)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="User not found", telegram_id=telegram_id)
        return UserResponse.model_validate(instance, from_attributes=True)

    async def create(self, **values: Unpack[UserCreateParams]) -> UserResponse:
        stmt = insert(User).values(**values).returning(User)
        res = await self.session.execute(stmt)
        return UserResponse.model_validate(res.scalar_one(), from_attributes=True)

    async def update(
        self, id: UUID, **values: Unpack[UserUpdateParams]
    ) -> UserResponse:
        stmt = update(User).where(User.id == id).values(**values).returning(User)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="User not found", id=id)
        return UserResponse.model_validate(instance, from_attributes=True)

    async def delete(self, id: UUID) -> None:
        stmt = delete(User).where(User.id == id)
        await self.session.execute(stmt)
