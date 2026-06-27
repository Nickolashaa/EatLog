from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info
from strawberry.fastapi import BaseContext

from ..dependencies.meal_logs import get_meal_log_service
from ..dependencies.meals import get_meal_service
from ..dependencies.session import get_session
from ..dependencies.users import get_user_service
from ..services import Services
from ..services.meal_logs import MealLogService
from ..services.meals import MealService
from ..services.users import UserService
from .data_loaders import DataLoaders
from .data_loaders.meals import build_meal_data_loader
from .data_loaders.users import build_user_data_loader


@dataclass(slots=True)
class Context(BaseContext):
    session: AsyncSession
    services: Services
    data_loaders: DataLoaders


async def context_getter(
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    meal_service: MealService = Depends(get_meal_service),
    meal_log_service: MealLogService = Depends(get_meal_log_service),
) -> Context:
    return Context(
        session=session,
        services=Services(
            user_service=user_service,
            meal_service=meal_service,
            meal_log_service=meal_log_service,
        ),
        data_loaders=DataLoaders(
            user_data_loader=build_user_data_loader(user_service),
            meal_data_loader=build_meal_data_loader(meal_service),
        ),
    )


AppInfo = Info[Context]
