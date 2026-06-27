from dataclasses import dataclass

import strawberry
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from ..dependencies.meal_logs import get_meal_log_service
from ..dependencies.meals import get_meal_service
from ..dependencies.session import get_session
from ..dependencies.users import get_user_service
from ..services.meal_logs import MealLogService
from ..services.meals import MealService
from ..services.users import UserService


@dataclass(slots=True)
class Context(BaseContext):
    session: AsyncSession
    user_service: UserService
    meal_service: MealService
    meal_log_service: MealLogService


async def context_getter(
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    meal_service: MealService = Depends(get_meal_service),
    meal_log_service: MealLogService = Depends(get_meal_log_service),
) -> Context:
    return Context(
        session=session,
        user_service=user_service,
        meal_service=meal_service,
        meal_log_service=meal_log_service,
    )


AppInfo = strawberry.Info[Context]
