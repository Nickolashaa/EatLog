from datetime import date

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.orm import Session

from ...database.models.meal_log import MealLog
from ...database.models.meals import Meal
from ..exceptions import ObjectNotFound
from .types import (
    MealLogCreateParams,
    MealLogTableRow,
    MealLogTotals,
    MealLogUpdateParams,
)


class MealLogService:
    @staticmethod
    def get(session: Session, id: int) -> MealLog:
        stmt = select(MealLog).where(MealLog.id == id)
        res = session.execute(stmt)
        instance = res.scalar_one_or_none()

        if instance is None:
            raise ObjectNotFound("MealLog not found", id=id)

        return instance

    @staticmethod
    def get_list(
        session: Session,
        date_filter: date | None = None,
    ) -> list[MealLog]:
        stmt = select(MealLog).order_by(MealLog.created_at.desc())
        if date_filter is not None:
            stmt = stmt.where(func.date(MealLog.created_at) == date_filter)
        res = session.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    def create(session: Session, values: MealLogCreateParams) -> MealLog:
        stmt = insert(MealLog).values(values).returning(MealLog)
        res = session.execute(stmt)
        return res.scalar_one()

    @staticmethod
    def update(session: Session, id: int, values: MealLogUpdateParams) -> MealLog:
        stmt = update(MealLog).where(MealLog.id == id).values(values).returning(MealLog)
        res = session.execute(stmt)
        instance = res.scalar_one_or_none()

        if instance is None:
            raise ObjectNotFound("MealLog not found", id=id)

        return instance

    @staticmethod
    def delete(session: Session, id: int) -> None:
        stmt = delete(MealLog).where(MealLog.id == id)
        session.execute(stmt)

    @staticmethod
    def get_table_list(
        session: Session,
        date_filter: date | None = None,
    ) -> list[MealLogTableRow]:
        stmt = (
            select(
                MealLog.id,
                Meal.title,
                MealLog.grams,
                (Meal.calories * MealLog.grams / 100).label("calories"),
                (Meal.protein * MealLog.grams / 100).label("protein"),
                (Meal.fat * MealLog.grams / 100).label("fat"),
                (Meal.carbohydrate * MealLog.grams / 100).label("carbohydrate"),
            )
            .join(Meal, MealLog.meal_id == Meal.id)
            .order_by(MealLog.created_at.desc())
        )
        if date_filter is not None:
            stmt = stmt.where(func.date(MealLog.created_at) == date_filter)
        return [
            {
                "log_id": int(r[0]),
                "meal_title": str(r[1]),
                "grams": float(r[2]),
                "calories": round(float(r[3]), 1),
                "protein": round(float(r[4]), 1),
                "fat": round(float(r[5]), 1),
                "carbohydrate": round(float(r[6]), 1),
            }
            for r in session.execute(stmt).all()
        ]

    @staticmethod
    def get_daily_totals(session: Session, target_date: date) -> MealLogTotals:
        stmt = (
            select(
                func.coalesce(func.sum(Meal.calories * MealLog.grams / 100), 0.0),
                func.coalesce(func.sum(Meal.protein * MealLog.grams / 100), 0.0),
                func.coalesce(func.sum(Meal.fat * MealLog.grams / 100), 0.0),
                func.coalesce(func.sum(Meal.carbohydrate * MealLog.grams / 100), 0.0),
            )
            .select_from(MealLog)
            .join(Meal, MealLog.meal_id == Meal.id)
            .where(func.date(MealLog.created_at) == target_date)
        )
        row = session.execute(stmt).one()
        return {
            "calories": float(row[0]),
            "protein": float(row[1]),
            "fat": float(row[2]),
            "carbohydrate": float(row[3]),
        }
