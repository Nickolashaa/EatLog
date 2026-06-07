from typing import Unpack, cast

from ..api.client import client
from .types import MealData, MealInput, MealListParams, MealUpdateParams


class MealApiService:
    @staticmethod
    def get_list(**params: Unpack[MealListParams]) -> list[MealData]:
        query: dict[str, str | int] = {}
        if "search" in params and params["search"]:
            query["search"] = params["search"]
        if "limit" in params:
            query["limit"] = params["limit"]
        resp = client.get("/meals", params=query)
        resp.raise_for_status()
        return cast(list[MealData], resp.json())

    @staticmethod
    def create(**params: Unpack[MealInput]) -> MealData:
        resp = client.post("/meals", json=dict(params))
        resp.raise_for_status()
        return cast(MealData, resp.json())

    @staticmethod
    def update(**params: Unpack[MealUpdateParams]) -> MealData:
        resp = client.put(f"/meals/{params['meal_id']}", json=dict(params["data"]))
        resp.raise_for_status()
        return cast(MealData, resp.json())

    @staticmethod
    def delete(meal_id: int) -> None:
        client.delete(f"/meals/{meal_id}").raise_for_status()
