from typing import Literal, TypedDict


class ProfileBase(TypedDict):
    name: str
    gender: Literal["male", "female"]
    weight: float
    height: float
    age: int
    goal: Literal["maintain", "lose", "gain"]


class Profile(ProfileBase):
    uuid: str
    notification_time: str | None
    hard_mod: bool


class Kbzhu(TypedDict):
    calories: int
    protein: int
    fat: int
    carbohydrate: int
