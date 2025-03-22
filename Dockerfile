FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY . .

EXPOSE 8000

CMD [ "uv", "run", "fastapi", "run", "--host", "0.0.0.0", "--port", "8000" ]
