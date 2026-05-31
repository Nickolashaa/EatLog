import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..di.meal_log import get_meal_log_service
from ..schemas.meal_log import (
    MealLogInput,
    MealLogResponse,
    MealLogTableRowResponse,
    MealLogTotalsResponse,
)
from ..services.exceptions import ObjectNotFound
from ..services.meal_log.service import MealLogService
from ..services.meal_log.types import MealLogListFilters

router = APIRouter(prefix="/meal-log", tags=["meal-log"])


@router.get("/table")
async def get_table(
    user_id: UUID,
    date: datetime.date | None = None,
    offset: int | None = None,
    service: MealLogService = Depends(get_meal_log_service),
) -> list[MealLogTableRowResponse]:
    filters: MealLogListFilters = {}
    if date is not None:
        filters["date_filter"] = date
    if offset is not None:
        filters["offset"] = offset
    return await service.get_table_list(user_id, **filters)


@router.get("/totals")
async def get_daily_totals(
    user_id: UUID,
    date: datetime.date,
    service: MealLogService = Depends(get_meal_log_service),
) -> MealLogTotalsResponse:
    return await service.get_daily_totals(user_id=user_id, target_date=date)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_meal_log(
    input: MealLogInput,
    service: MealLogService = Depends(get_meal_log_service),
) -> MealLogResponse:
    return await service.create(
        user_id=input.user_id,
        meal_id=input.meal_id,
        grams=input.grams,
    )


@router.put("/{id}")
async def update_meal_log(
    id: int,
    input: MealLogInput,
    service: MealLogService = Depends(get_meal_log_service),
) -> MealLogResponse:
    try:
        return await service.update(
            id,
            meal_id=input.meal_id,
            grams=input.grams,
        )
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal_log(
    id: int,
    service: MealLogService = Depends(get_meal_log_service),
) -> None:
    await service.delete(id)
