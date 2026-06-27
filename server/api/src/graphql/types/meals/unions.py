from typing import Annotated

import strawberry

from ..errors import ObjectAlreadyExistsError
from .types import Meal

type CreateMealOrError = Annotated[
    Meal | ObjectAlreadyExistsError, strawberry.union("CreateMealOrError")
]
