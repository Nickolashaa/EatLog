from typing import Literal, TypedDict


class ProfileBase(TypedDict):
    gender: Literal["male", "female"]
    weight: float
    height: float
    age: int
    goal: Literal["maintain", "lose", "gain"]


class Profile(ProfileBase):
    uuid: str


class Kbzhu(TypedDict):
    calories: int
    protein: int
    fat: int
    carbohydrate: int
