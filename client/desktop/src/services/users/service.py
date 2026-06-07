from typing import Literal, Unpack, cast

from ..api.client import client
from ..profile.types import Profile, ProfileBase
from .types import UserUpdateParams


class UserApiService:
    @staticmethod
    def create(profile: ProfileBase) -> str:
        resp = client.post("/users", json={"telegram_id": None, **profile})
        resp.raise_for_status()
        return str(resp.json()["id"])

    @staticmethod
    def get(uuid: str) -> Profile:
        resp = client.get(f"/users/{uuid}")
        resp.raise_for_status()
        data = resp.json()
        return {
            "uuid": str(data["id"]),
            "gender": cast(Literal["male", "female"], data["gender"]),
            "weight": float(data["weight"]),
            "height": float(data["height"]),
            "age": int(data["age"]),
            "goal": cast(Literal["maintain", "lose", "gain"], data["goal"]),
        }

    @staticmethod
    def get_telegram_id(uuid: str) -> int | None:
        resp = client.get(f"/users/{uuid}")
        resp.raise_for_status()
        telegram_id = resp.json()["telegram_id"]
        return int(telegram_id) if telegram_id is not None else None

    @staticmethod
    def update(**params: Unpack[UserUpdateParams]) -> None:
        resp = client.put(
            f"/users/{params['uuid']}",
            json={"telegram_id": None, **params["profile"]},
        )
        resp.raise_for_status()
