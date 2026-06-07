from typing import Unpack

from ..api.client import client
from ..profile.types import ProfileBase
from .types import UserUpdateParams


class UserApiService:
    @staticmethod
    def create(profile: ProfileBase) -> str:
        resp = client.post("/users", json={"telegram_id": None, **profile})
        resp.raise_for_status()
        return str(resp.json()["id"])

    @staticmethod
    def update(**params: Unpack[UserUpdateParams]) -> None:
        resp = client.put(
            f"/users/{params['uuid']}",
            json={"telegram_id": None, **params["profile"]},
        )
        resp.raise_for_status()
