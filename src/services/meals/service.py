from sqlalchemy import delete, insert, or_, select, update
from sqlalchemy.orm import Session

from ...database.models.meals import Meal
from ..exceptions import ObjectNotFound
from .types import MealCreateParams, MealUpdateParams


class MealService:
    @staticmethod
    def get(session: Session, id: int) -> Meal:
        stmt = select(Meal).where(Meal.id == id)
        res = session.execute(stmt)
        instance = res.scalar_one_or_none()

        if instance is None:
            raise ObjectNotFound("Meal not found", id=id)

        return instance

    @staticmethod
    def get_list(
        session: Session,
        search_query: str = "",
        limit: int | None = None,
    ) -> list[Meal]:
        stmt = select(Meal).order_by(Meal.title)
        if search_query:
            stmt = stmt.where(
                or_(
                    Meal.title.icontains(search_query),
                    Meal.title.icontains(search_query.lower()),
                    Meal.title.icontains(search_query.upper()),
                    Meal.title.icontains(search_query.capitalize()),
                )
            )
        if limit is not None:
            stmt = stmt.limit(limit)
        res = session.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    def create(session: Session, values: MealCreateParams) -> Meal:
        stmt = insert(Meal).values(values).returning(Meal)
        res = session.execute(stmt)
        return res.scalar_one()

    @staticmethod
    def update(session: Session, id: int, values: MealUpdateParams) -> Meal:
        stmt = update(Meal).where(Meal.id == id).values(values).returning(Meal)
        res = session.execute(stmt)
        instance = res.scalar_one_or_none()

        if instance is None:
            raise ObjectNotFound("Meal not found", id=id)

        return instance

    @staticmethod
    def delete(session: Session, id: int) -> None:
        stmt = delete(Meal).where(Meal.id == id)
        session.execute(stmt)
