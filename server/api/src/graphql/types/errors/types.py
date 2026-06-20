import strawberry

from .interfaces import BaseErrorInterface


@strawberry.type
class ObjectNotFoundError(BaseErrorInterface):
    pass


@strawberry.type
class ObjectAlreadyExistsError(BaseErrorInterface):
    pass
