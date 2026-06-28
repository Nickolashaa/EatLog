from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .graphql import graphql_app

app = FastAPI(title="EatLog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
