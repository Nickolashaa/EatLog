from typing import Unpack, cast

from ..api.client import client
from .types import (
    MealLogCreateParams,
    MealLogTableParams,
    MealLogTableRow,
    MealLogTotals,
    MealLogTotalsParams,
    MealLogUpdateParams,
)


class MealLogApiService:
    @staticmethod
    def get_table_list(**params: Unpack[MealLogTableParams]) -> list[MealLogTableRow]:
        query: dict[str, str] = {"user_id": params["user_id"]}
        if "date_filter" in params:
            query["date"] = params["date_filter"].isoformat()
        resp = client.get("/meal-log/table", params=query)
        resp.raise_for_status()
        return cast(list[MealLogTableRow], resp.json())

    @staticmethod
    def get_daily_totals(**params: Unpack[MealLogTotalsParams]) -> MealLogTotals:
        resp = client.get(
            "/meal-log/totals",
            params={
                "user_id": params["user_id"],
                "date": params["target_date"].isoformat(),
            },
        )
        resp.raise_for_status()
        return cast(MealLogTotals, resp.json())

    @staticmethod
    def create(**params: Unpack[MealLogCreateParams]) -> dict[str, object]:
        resp = client.post("/meal-log", json=dict(params))
        resp.raise_for_status()
        return cast(dict[str, object], resp.json())

    @staticmethod
    def update(**params: Unpack[MealLogUpdateParams]) -> dict[str, object]:
        resp = client.put(
            f"/meal-log/{params['log_id']}",
            json={
                "user_id": params["user_id"],
                "meal_id": params["meal_id"],
                "grams": params["grams"],
            },
        )
        resp.raise_for_status()
        return cast(dict[str, object], resp.json())

    @staticmethod
    def delete(log_id: int) -> None:
        client.delete(f"/meal-log/{log_id}").raise_for_status()
