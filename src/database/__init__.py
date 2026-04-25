from .connection import Base, engine
from .models.meals import Meal  # noqa: F401

Base.metadata.create_all(bind=engine)
