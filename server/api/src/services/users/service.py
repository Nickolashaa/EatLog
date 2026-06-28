from typing import Unpack
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.users import User
from ..exceptions import ObjectNotFound
from .schemas import UserSchema
from .types import UserCreateParams, UserListFilters, UserUpdateParams


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: UUID) -> UserSchema:
        stmt = select(User).where(User.id == id)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="User not found", id=id)
        return UserSchema.model_validate(instance, from_attributes=True)

    async def get_list(
        self,
        **filters: Unpack[UserListFilters],
    ) -> list[UserSchema]:
        stmt = select(User)

        if ids := filters.get("ids"):
            stmt = stmt.where(User.id.in_(ids))

        res = await self.session.execute(stmt)

        return [
            UserSchema.model_validate(instance, from_attributes=True)
            for instance in res.scalars().all()
        ]

    async def get_by_telegram_id(self, telegram_id: str) -> UserSchema:
        stmt = select(User).where(User.telegram_id == telegram_id)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="User not found", telegram_id=telegram_id)
        return UserSchema.model_validate(instance, from_attributes=True)

    async def create(self, **values: Unpack[UserCreateParams]) -> UserSchema:
        stmt = insert(User).values(**values).returning(User)
        res = await self.session.execute(stmt)
        return UserSchema.model_validate(res.scalar_one(), from_attributes=True)

    async def update(self, id: UUID, **values: Unpack[UserUpdateParams]) -> UserSchema:
        stmt = update(User).where(User.id == id).values(**values).returning(User)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="User not found", id=id)
        return UserSchema.model_validate(instance, from_attributes=True)
