from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import meal_log, meals, users

app = FastAPI(title="EatLog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meals.router)
app.include_router(meal_log.router)
app.include_router(users.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
