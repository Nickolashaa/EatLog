from dataclasses import dataclass

from .meals import MEAL_DATA_LOADER
from .users import USER_DATA_LOADER


@dataclass(frozen=True, slots=True)
class DataLoaders:
    user_data_loader: USER_DATA_LOADER
    meal_data_loader: MEAL_DATA_LOADER
