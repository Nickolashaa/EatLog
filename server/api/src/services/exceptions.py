class BaseException(Exception):
    def __init__(self, message: str, **kwargs: object) -> None:
        super().__init__(message)
        self.details = kwargs


class ObjectNotFound(BaseException):
    pass


class ObjectAlreadyExists(BaseException):
    pass
