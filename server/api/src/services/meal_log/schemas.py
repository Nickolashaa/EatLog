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
