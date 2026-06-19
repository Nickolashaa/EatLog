from datetime import datetime
from typing import NotRequired, Required, TypedDict

from ...database.models.users import Gender, Goal


class UserCreateParams(TypedDict):
    telegram_id: Required[int | None]
    name: Required[str]
    gender: Required[Gender]
    weight: Required[float]
    height: Required[float]
    age: Required[int]
    goal: Required[Goal]
    notification_time: Required[datetime | None]
    hard_mod: Required[bool]


class UserUpdateParams(TypedDict):
    telegram_id: NotRequired[int | None]
    name: NotRequired[str]
    gender: NotRequired[Gender]
    weight: NotRequired[float]
    height: NotRequired[float]
    age: NotRequired[int]
    goal: NotRequired[Goal]
    notification_time: NotRequired[datetime | None]
    hard_mod: NotRequired[bool]
