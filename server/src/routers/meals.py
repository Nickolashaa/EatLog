from fastapi import APIRouter, Depends, HTTPException, status

from ..di.meals import get_meal_service
from ..schemas.meals import MealInput, MealResponse
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound
from ..services.meals.service import MealService
from ..services.meals.types import MealListFilters

router = APIRouter(prefix="/meals", tags=["meals"])


@router.get("")
async def list_meals(
    search: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    service: MealService = Depends(get_meal_service),
) -> list[MealResponse]:
    filters: MealListFilters = {}
    if search is not None:
        filters["search_query"] = search
    if limit is not None:
        filters["limit"] = limit
    if offset is not None:
        filters["offset"] = offset
    return await service.get_list(**filters)


@router.get("/{id}")
async def get_meal(
    id: int, service: MealService = Depends(get_meal_service)
) -> MealResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_meal(
    input: MealInput, service: MealService = Depends(get_meal_service)
) -> MealResponse:
    try:
        return await service.create(
            title=input.title,
            calories=input.calories,
            protein=input.protein,
            fat=input.fat,
            carbohydrate=input.carbohydrate,
        )
    except ObjectAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}")
async def update_meal(
    id: int,
    input: MealInput,
    service: MealService = Depends(get_meal_service),
) -> MealResponse:
    try:
        return await service.update(
            id,
            title=input.title,
            calories=input.calories,
            protein=input.protein,
            fat=input.fat,
            carbohydrate=input.carbohydrate,
        )
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ObjectAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(
    id: int, service: MealService = Depends(get_meal_service)
) -> None:
    await service.delete(id)
