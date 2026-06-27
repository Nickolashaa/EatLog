from typing import TypedDict

from ...graphql.client import Gender, Goal

GENDER_OPTIONS: list[tuple[str, Gender]] = [
    ("Мужской", Gender.MALE),
    ("Женский", Gender.FEMALE),
]

GOAL_OPTIONS: list[tuple[str, Goal]] = [
    ("Поддержание веса", Goal.MAINTAIN),
    ("Похудение", Goal.LOSE),
    ("Набор мышечной массы", Goal.GAIN),
]


class ProfileFormValues(TypedDict):
    name: str
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
