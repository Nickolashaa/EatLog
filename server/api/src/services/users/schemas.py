from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .types import GENDER, GOAL


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: str | None
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
