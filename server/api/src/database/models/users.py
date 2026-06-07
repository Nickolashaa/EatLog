import enum
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Goal(enum.Enum):
    MAINTAIN = "maintain"
    LOSE = "lose"
    GAIN = "gain"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    telegram_id: Mapped[int | None] = mapped_column(BigInteger)
    gender: Mapped[Gender]
    weight: Mapped[float]
    height: Mapped[float]
    age: Mapped[int]
    goal: Mapped[Goal]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
