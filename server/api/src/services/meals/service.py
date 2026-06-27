from typing import Unpack

from sqlalchemy import delete, insert, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.meals import Meal
from ..exceptions import ObjectAlreadyExists, ObjectNotFound
from .schemas import MealSchema
from .types import MealCreateParams, MealListFilters, MealUpdateParams


class MealService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> MealSchema:
        stmt = select(Meal).where(Meal.id == id)
        res = await self.session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            raise ObjectNotFound(message="Meal not found", id=id)
        return MealSchema.model_validate(instance, from_attributes=True)

    async def get_list(
        self, limit: int = 10, offset: int = 0, **filters: Unpack[MealListFilters]
    ) -> list[MealSchema]:
        stmt = select(Meal).order_by(Meal.title)
        if search_query := filters.get("search_query"):
            stmt = stmt.where(
                or_(
                    Meal.title.icontains(search_query),
                    Meal.title.icontains(search_query.lower()),
                    Meal.title.icontains(search_query.upper()),
                    Meal.title.icontains(search_query.capitalize()),
                )
            )

        stmt = stmt.offset(offset).limit(limit)

        res = await self.session.execute(stmt)
        return [
            MealSchema.model_validate(instance, from_attributes=True)
            for instance in res.scalars().all()
        ]

    async def create(self, **values: Unpack[MealCreateParams]) -> MealSchema:
        try:
            stmt = insert(Meal).values(values).returning(Meal)
            res = await self.session.execute(stmt)
            return MealSchema.model_validate(res.scalar_one(), from_attributes=True)
        except IntegrityError:
            raise ObjectAlreadyExists(
                message="Meal already exists", title=values.get("title")
            )

    async def update(self, id: int, **values: Unpack[MealUpdateParams]) -> MealSchema:
        try:
            stmt = update(Meal).where(Meal.id == id).values(values).returning(Meal)
            res = await self.session.execute(stmt)
            instance = res.scalar_one_or_none()
            if instance is None:
                raise ObjectNotFound(message="Meal not found", id=id)
            return MealSchema.model_validate(instance, from_attributes=True)
        except IntegrityError:
            raise ObjectAlreadyExists(
                message="Meal already exists", title=values.get("title")
            )

    async def delete(self, id: int) -> None:
        stmt = delete(Meal).where(Meal.id == id)
        await self.session.execute(stmt)
