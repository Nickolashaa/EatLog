from typing import Self

import strawberry

from ....services.exceptions import BaseException


@strawberry.interface
class BaseErrorInterface:
    message: str

    @classmethod
    def from_exception(cls, instance: BaseException) -> Self:
        return cls(
            message=instance.error_text,
        )
