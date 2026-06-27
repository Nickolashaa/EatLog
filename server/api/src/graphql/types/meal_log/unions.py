from typing import Annotated

import strawberry

from ..errors import ObjectNotFoundError
from .types import MealLog

CreateMealLogOrError = Annotated[
    MealLog | ObjectNotFoundError, strawberry.union("CreateMealLogOrError")
]
UpdateMealLogOrError = Annotated[
    MealLog | ObjectNotFoundError, strawberry.union("UpdateMealLogOrError")
]
