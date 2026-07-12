FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/server/api/

COPY ./server/api/pyproject.toml ./server/api/uv.lock ./server/api/alembic.ini ./

RUN uv sync --frozen --no-dev --no-install-project

COPY ./server/api/src/ ./src/

CMD ["uv", "run", "python", "-m", "src"]
