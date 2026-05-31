from typing import Any


class BaseException(Exception):
    def __init__(self, message: str, **kwagrs: Any) -> None:
        super().__init__()
        self.message = message
        self.data = kwagrs

    def __str__(self) -> str:
        return f"{self.message}\n{self.data}"


class ObjectNotFound(BaseException):
    pass
