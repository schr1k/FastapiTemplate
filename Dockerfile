FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

COPY . .

EXPOSE 8000

CMD [ "uv", "run", "--no-dev", "fastapi", "run", "--host", "0.0.0.0", "--port", "8000" ]