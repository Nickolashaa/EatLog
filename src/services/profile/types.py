from typing import Literal, TypedDict


class Profile(TypedDict):
    gender: Literal["male", "female"]
    weight: float
    height: float
    age: int
    goal: Literal["maintain", "lose", "gain"]


class Kbzhu(TypedDict):
    calories: int
    protein: int
    fat: int
    carbohydrate: int
