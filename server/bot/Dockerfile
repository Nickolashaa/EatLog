FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/shared/gql/
COPY ./shared/gql/ ./

WORKDIR /app/server/bot/
COPY ./server/bot/pyproject.toml ./server/bot/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

WORKDIR /app/server/bot/src/
COPY ./server/bot/src/ ./

WORKDIR /app/server/bot/
CMD ["uv", "run", "python", "-m", "src"]
