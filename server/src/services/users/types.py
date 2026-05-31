from typing import NotRequired, Required, TypedDict

from ...database.models.users import Gender, Goal


class UserCreateParams(TypedDict):
    telegram_id: Required[int | None]
    gender: Required[Gender]
    weight: Required[float]
    height: Required[float]
    age: Required[int]
    goal: Required[Goal]


class UserUpdateParams(TypedDict):
    telegram_id: NotRequired[int | None]
    gender: NotRequired[Gender]
    weight: NotRequired[float]
    height: NotRequired[float]
    age: NotRequired[int]
    goal: NotRequired[Goal]
