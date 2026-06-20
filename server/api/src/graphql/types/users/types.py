from datetime import datetime
from typing import Self
from uuid import UUID

import strawberry

from ....services.users.schemas import UserResponse
from .enums import Gender, Goal


@strawberry.type
class User:
    id: UUID
    name: str
    telegram_id: str | None
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
    created_at: datetime
    updated_at: datetime
    notification_time: datetime | None
    hard_mod: bool

    @classmethod
    def from_schema(cls, instance: UserResponse) -> Self:
        return cls(
            id=instance.id,
            name=instance.name,
            telegram_id=str(instance.telegram_id),
            gender=Gender[instance.gender],
            weight=instance.weight,
            height=instance.height,
            age=instance.age,
            goal=Goal[instance.goal],
            created_at=instance.created_at,
            updated_at=instance.updated_at,
            notification_time=instance.notification_time,
            hard_mod=instance.hard_mod,
        )
