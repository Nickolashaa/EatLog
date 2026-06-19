from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from ..database.models.users import Gender, Goal


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: int | None
    name: str
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
    notification_time: datetime | None
    hard_mod: bool
    created_at: datetime
    updated_at: datetime


class UserInput(BaseModel):
    telegram_id: int | None = None
    name: str
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
    notification_time: datetime | None = None
    hard_mod: bool = False


class UserUpdate(BaseModel):
    name: str | None = None
    gender: Gender | None = None
    weight: float | None = None
    height: float | None = None
    age: int | None = None
    goal: Goal | None = None
    notification_time: datetime | None = None
    hard_mod: bool | None = None


class UserRegister(BaseModel):
    id: UUID
    telegram_id: int
