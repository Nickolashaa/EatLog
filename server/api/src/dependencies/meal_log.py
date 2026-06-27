from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.meal_log.service import MealLogService
from .session import get_session


async def get_meal_log_service(
    session: AsyncSession = Depends(get_session),
) -> MealLogService:
    return MealLogService(session)
