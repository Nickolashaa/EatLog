import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .cronjobs import scheduler
from .graphql import graphql_app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.basicConfig(level=logging.INFO)
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(title="EatLog API", lifespan=lifespan)
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
