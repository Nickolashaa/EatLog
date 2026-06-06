from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from ..database.models.users import Gender, Goal


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: int | None
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
    created_at: datetime
    updated_at: datetime


class UserInput(BaseModel):
    telegram_id: int | None = None
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal


class UserRegister(BaseModel):
    id: UUID
    telegram_id: int
