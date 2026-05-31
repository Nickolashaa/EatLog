from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MealResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    calories: float
    protein: float
    fat: float
    carbohydrate: float
    created_at: datetime
    updated_at: datetime


class MealInput(BaseModel):
    title: str
    calories: float
    protein: float
    fat: float
    carbohydrate: float
