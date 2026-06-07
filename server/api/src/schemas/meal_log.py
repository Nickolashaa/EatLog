from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MealLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: UUID
    meal_id: int
    grams: float
    created_at: datetime
    updated_at: datetime


class MealLogInput(BaseModel):
    user_id: UUID
    meal_id: int
    grams: float


class MealLogTableRowResponse(BaseModel):
    log_id: int
    meal_id: int
    meal_title: str
    grams: float
    calories: float
    protein: float
    fat: float
    carbohydrate: float


class MealLogTotalsResponse(BaseModel):
    calories: float
    protein: float
    fat: float
    carbohydrate: float
