from typing import Annotated

import strawberry

from ..errors import ObjectNotFoundError
from .types import User

GetUserOrError = Annotated[
    User | ObjectNotFoundError, strawberry.union("GetUserOrError")
]
UpdateUserOrError = Annotated[
    User | ObjectNotFoundError, strawberry.union("UpdateUserOrError")
]
