import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ..connection import Base


class Gender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Goal(StrEnum):
    MAINTAIN = "MAINTAIN"
    LOSE = "LOSE"
    GAIN = "GAIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    telegram_id: Mapped[str | None]
    gender: Mapped[Gender]
    weight: Mapped[float]
    height: Mapped[float]
    age: Mapped[int]
    goal: Mapped[Goal]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    notification_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    hard_mod: Mapped[bool] = mapped_column(server_default=expression.false())
    name: Mapped[str]
