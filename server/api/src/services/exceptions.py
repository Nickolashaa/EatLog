from uuid import UUID


class BaseException(Exception):
    def __init__(self, message: str, **kwargs: int | str | UUID | None) -> None:
        super().__init__(message)
        self.error_text = f"{message}\n{
            '\n'.join([f'{key}: {value}' for key, value in kwargs.items()])
        }"


class ObjectNotFound(BaseException):
    pass


class ObjectAlreadyExists(BaseException):
    pass
