from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from .types import GENDER, GOAL


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: int | None
    name: str
    gender: GENDER
    weight: float
    height: float
    age: int
    goal: GOAL
    notification_time: datetime | None
    hard_mod: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("gender", "goal", mode="before")
    @classmethod
    def _enum_to_literal(cls, value: Enum | str) -> str:
        return value.name if isinstance(value, Enum) else value
