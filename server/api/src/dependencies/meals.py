from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.meals.service import MealService
from .session import get_session


async def get_meal_service(session: AsyncSession = Depends(get_session)) -> MealService:
    return MealService(session)
