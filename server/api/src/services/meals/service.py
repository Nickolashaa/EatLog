from typing import Unpack

from sqlalchemy import insert, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.meals import Meal
from ..exceptions import ObjectAlreadyExists
from .schemas import MealSchema
from .types import MealCreateParams, MealListFilters


class MealService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters: Unpack[MealListFilters],
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
        if ids := filters.get("ids"):
            stmt = stmt.where(Meal.id.in_(ids))

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
