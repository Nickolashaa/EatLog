import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Goal(enum.Enum):
    MAINTAIN = "maintain"
    LOSE = "lose"
    GAIN = "gain"


class UserResponse(BaseModel):
    id: UUID
    telegram_id: int | None
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
    created_at: datetime
    updated_at: datetime


class UserRegister(BaseModel):
    id: UUID
    telegram_id: int
