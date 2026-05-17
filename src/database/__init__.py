from .connection import Base, engine
from .models.meal_log import MealLog  # noqa: F401
from .models.meals import Meal  # noqa: F401

Base.metadata.create_all(bind=engine)
