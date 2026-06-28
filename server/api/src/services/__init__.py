from dataclasses import dataclass

from .meal_logs import MealLogService
from .meals import MealService
from .users import UserService


@dataclass(frozen=True, slots=True)
class Services:
    user_service: UserService
    meal_service: MealService
    meal_log_service: MealLogService
