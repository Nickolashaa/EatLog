from datetime import datetime
from typing import Literal, NotRequired, Required, TypedDict

type GENDER = Literal["MALE", "FEMALE"]
type GOAL = Literal["MAINTAIN", "LOSE", "GAIN"]


class UserCreateParams(TypedDict):
    telegram_id: Required[str | None]
    name: Required[str]
    gender: Required[GENDER]
    weight: Required[float]
    height: Required[float]
    age: Required[int]
    goal: Required[GOAL]
    notification_time: Required[datetime | None]
    hard_mod: Required[bool]


class UserUpdateParams(TypedDict):
    telegram_id: NotRequired[str | None]
    name: NotRequired[str]
    gender: NotRequired[GENDER]
    weight: NotRequired[float]
    height: NotRequired[float]
    age: NotRequired[int]
    goal: NotRequired[GOAL]
    notification_time: NotRequired[datetime | None]
    hard_mod: NotRequired[bool]
