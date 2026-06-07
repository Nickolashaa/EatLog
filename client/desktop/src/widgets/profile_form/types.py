from typing import Literal

GENDER_OPTIONS: list[tuple[str, Literal["male", "female"]]] = [
    ("Мужской", "male"),
    ("Женский", "female"),
]

GOAL_OPTIONS: list[tuple[str, Literal["maintain", "lose", "gain"]]] = [
    ("Поддержание веса", "maintain"),
    ("Похудение", "lose"),
    ("Набор мышечной массы", "gain"),
]
