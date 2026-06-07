from datetime import date
from typing import Unpack
from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.meal_log import MealLog
from ...database.models.meals import Meal
from ...schemas.meal_log import (
    MealLogResponse,
    MealLogTableRowResponse,
    MealLogTotalsResponse,
)
from ..exceptions import ObjectNotFound
from .types import MealLogCreateParams, MealLogListFilters, MealLogUpdateParams


class MealLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> MealLogResponse:
        stmt = select(MealLog).where(MealLog.id == id)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="MealLog not found", id=id)
        return MealLogResponse.model_validate(instance)

    async def get_list(
        self, user_id: UUID, **filters: Unpack[MealLogListFilters]
    ) -> list[MealLogResponse]:
        stmt = (
            select(MealLog)
            .where(MealLog.user_id == user_id)
            .order_by(MealLog.created_at.desc())
        )
        if date_filter := filters.get("date_filter"):
            stmt = stmt.where(func.date(MealLog.created_at) == date_filter)
        if offset := filters.get("offset"):
            stmt = stmt.offset(offset)
        res = await self.session.execute(stmt)
        return [MealLogResponse.model_validate(log) for log in res.scalars().all()]

    async def create(self, **values: Unpack[MealLogCreateParams]) -> MealLogResponse:
        stmt = insert(MealLog).values(values).returning(MealLog)
        res = await self.session.execute(stmt)
        return MealLogResponse.model_validate(res.scalar_one())

    async def update(
        self, id: int, **values: Unpack[MealLogUpdateParams]
    ) -> MealLogResponse:
        stmt = update(MealLog).where(MealLog.id == id).values(values).returning(MealLog)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="MealLog not found", id=id)
        return MealLogResponse.model_validate(instance)

    async def delete(self, id: int) -> None:
        stmt = delete(MealLog).where(MealLog.id == id)
        await self.session.execute(stmt)

    async def get_table_list(
        self, user_id: UUID, **filters: Unpack[MealLogListFilters]
    ) -> list[MealLogTableRowResponse]:
        stmt = (
            select(
                MealLog.id,
                MealLog.meal_id,
                Meal.title,
                MealLog.grams,
                (Meal.calories * MealLog.grams / 100).label("calories"),
                (Meal.protein * MealLog.grams / 100).label("protein"),
                (Meal.fat * MealLog.grams / 100).label("fat"),
                (Meal.carbohydrate * MealLog.grams / 100).label("carbohydrate"),
            )
            .join(Meal, MealLog.meal_id == Meal.id)
            .where(MealLog.user_id == user_id)
            .order_by(MealLog.created_at.desc())
        )
        if date_filter := filters.get("date_filter"):
            stmt = stmt.where(func.date(MealLog.created_at) == date_filter)
        if offset := filters.get("offset"):
            stmt = stmt.offset(offset)
        res = await self.session.execute(stmt)
        return [
            MealLogTableRowResponse(
                log_id=int(r[0]),
                meal_id=int(r[1]),
                meal_title=str(r[2]),
                grams=float(r[3]),
                calories=round(float(r[4]), 1),
                protein=round(float(r[5]), 1),
                fat=round(float(r[6]), 1),
                carbohydrate=round(float(r[7]), 1),
            )
            for r in res.all()
        ]

    async def get_daily_totals(
        self, user_id: UUID, target_date: date
    ) -> MealLogTotalsResponse:
        stmt = (
            select(
                func.coalesce(func.sum(Meal.calories * MealLog.grams / 100), 0.0),
                func.coalesce(func.sum(Meal.protein * MealLog.grams / 100), 0.0),
                func.coalesce(func.sum(Meal.fat * MealLog.grams / 100), 0.0),
                func.coalesce(func.sum(Meal.carbohydrate * MealLog.grams / 100), 0.0),
            )
            .select_from(MealLog)
            .join(Meal, MealLog.meal_id == Meal.id)
            .where(
                MealLog.user_id == user_id, func.date(MealLog.created_at) == target_date
            )
        )
        res = await self.session.execute(stmt)
        row = res.one()
        return MealLogTotalsResponse(
            calories=float(row[0]),
            protein=float(row[1]),
            fat=float(row[2]),
            carbohydrate=float(row[3]),
        )
