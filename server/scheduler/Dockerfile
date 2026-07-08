FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/shared/gql/
COPY ./shared/gql/ ./

WORKDIR /app/server/scheduler/
COPY ./server/scheduler/pyproject.toml ./server/scheduler/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

WORKDIR /app/server/scheduler/src/
COPY ./server/scheduler/src/ ./

WORKDIR /app/server/scheduler/
CMD ["uv", "run", "python", "-m", "src"]
