from typing import Literal, cast

from ..api.client import client
from ..profile.types import Profile, ProfileBase


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
            "name": str(data["name"]),
            "gender": cast(Literal["male", "female"], data["gender"]),
            "weight": float(data["weight"]),
            "height": float(data["height"]),
            "age": int(data["age"]),
            "goal": cast(Literal["maintain", "lose", "gain"], data["goal"]),
            "notification_time": data["notification_time"],
            "hard_mod": bool(data["hard_mod"]),
        }

    @staticmethod
    def get_telegram_id(uuid: str) -> int | None:
        resp = client.get(f"/users/{uuid}")
        resp.raise_for_status()
        telegram_id = resp.json()["telegram_id"]
        return int(telegram_id) if telegram_id is not None else None

    @staticmethod
    def update_profile(uuid: str, profile: ProfileBase) -> None:
        resp = client.put(f"/users/{uuid}", json=dict(profile))
        resp.raise_for_status()

    @staticmethod
    def update_notifications(
        uuid: str, notification_time: str | None, hard_mod: bool
    ) -> None:
        resp = client.put(
            f"/users/{uuid}",
            json={"notification_time": notification_time, "hard_mod": hard_mod},
        )
        resp.raise_for_status()
