from datetime import date, time

import strawberry

from ....services.users.types import UserCreateParams, UserListFilters, UserUpdateParams
from .enums import Gender, Goal


@strawberry.input
class CreateUserInput:
    name: str
    telegram_id: str | None = None
    gender: Gender
    weight: float
    height: float
    age: int
    goal: Goal
    notification_time: time | None = None
    hard_mod: bool = False

    def to_service_params(self) -> UserCreateParams:
        return UserCreateParams(
            name=self.name,
            telegram_id=self.telegram_id,
            gender=self.gender.value,
            weight=self.weight,
            height=self.height,
            age=self.age,
            goal=self.goal.value,
            notification_time=self.notification_time,
            hard_mod=self.hard_mod,
        )


@strawberry.input
class UpdateUserInput:
    name: strawberry.Maybe[str]
    telegram_id: strawberry.Maybe[str | None]
    gender: strawberry.Maybe[Gender]
    weight: strawberry.Maybe[float]
    height: strawberry.Maybe[float]
    age: strawberry.Maybe[int]
    goal: strawberry.Maybe[Goal]
    notification_time: strawberry.Maybe[time | None]
    hard_mod: strawberry.Maybe[bool]

    def to_service_params(self) -> UserUpdateParams:
        params: UserUpdateParams = {}
        if self.name is not None:
            params["name"] = self.name.value
        if self.telegram_id is not None:
            params["telegram_id"] = self.telegram_id.value
        if self.gender is not None:
            params["gender"] = self.gender.value.value
        if self.weight is not None:
            params["weight"] = self.weight.value
        if self.height is not None:
            params["height"] = self.height.value
        if self.age is not None:
            params["age"] = self.age.value
        if self.goal is not None:
            params["goal"] = self.goal.value.value
        if self.notification_time is not None:
            params["notification_time"] = self.notification_time.value
        if self.hard_mod is not None:
            params["hard_mod"] = self.hard_mod.value
        return params


@strawberry.input
class UsersFilterInput:
    without_logs_on: strawberry.Maybe[date]

    def to_service_params(self) -> UserListFilters:
        params: UserListFilters = {}
        if self.without_logs_on is not None:
            params["without_logs_on"] = self.without_logs_on.value
        return params
