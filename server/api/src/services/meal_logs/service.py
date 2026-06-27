from typing import Unpack
from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.meal_logs import MealLog
from ..exceptions import ObjectNotFound
from .schemas import MealLogSchema
from .types import MealLogCreateParams, MealLogListFilters, MealLogUpdateParams


class MealLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _parse_integity_error(
        self,
        exc: IntegrityError,
        user_id: UUID | None = None,
        meal_id: int | None = None,
    ) -> ObjectNotFound:
        if "meal_logs_user_id_fkey" in str(exc.orig).lower():
            return ObjectNotFound(message="User not found", id=user_id)
        return ObjectNotFound(message="Meal not found", id=meal_id)

    async def get_list(
        self, limit: int, offset: int, **filters: Unpack[MealLogListFilters]
    ) -> list[MealLogSchema]:
        stmt = select(MealLog).order_by(MealLog.created_at.desc())

        if date_filter := filters.get("date_filter"):
            stmt = stmt.where(func.date(MealLog.created_at) == date_filter)
        if user_id := filters.get("user_id"):
            stmt = stmt.where(MealLog.user_id == user_id)

        stmt = stmt.offset(offset).limit(limit)

        res = await self.session.execute(stmt)
        return [
            MealLogSchema.model_validate(instance, from_attributes=True)
            for instance in res.scalars().all()
        ]

    async def create(self, **values: Unpack[MealLogCreateParams]) -> MealLogSchema:
        stmt = insert(MealLog).values(**values).returning(MealLog)
        try:
            res = await self.session.execute(stmt)
        except IntegrityError as exc:
            raise self._parse_integity_error(
                exc=exc,
                user_id=values.get("user_id"),
                meal_id=values.get("meal_id"),
            )
        return MealLogSchema.model_validate(res.scalar_one(), from_attributes=True)

    async def update(
        self, id: int, **values: Unpack[MealLogUpdateParams]
    ) -> MealLogSchema:
        stmt = (
            update(MealLog).where(MealLog.id == id).values(**values).returning(MealLog)
        )
        try:
            res = await self.session.execute(stmt)
        except IntegrityError as exc:
            raise self._parse_integity_error(
                exc=exc,
                user_id=values.get("user_id"),
                meal_id=values.get("meal_id"),
            )
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="MealLog not found", id=id)
        return MealLogSchema.model_validate(instance, from_attributes=True)

    async def delete(self, id: int) -> None:
        stmt = delete(MealLog).where(MealLog.id == id)
        await self.session.execute(stmt)
