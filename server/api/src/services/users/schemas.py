from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .types import GENDER, GOAL


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: str | None
    name: str
    gender: GENDER
    weight: float
    height: float
    age: int
    goal: GOAL
    notification_time: time | None
    hard_mod: bool
    created_at: datetime
    updated_at: datetime
