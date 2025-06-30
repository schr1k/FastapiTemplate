from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.database.connection import create_tables, engine
from src.routers.checks import checks_router
from src.routers.users import users_router
from src.settings import settings

swagger_ui_parameters = {
    'filter': True,
    'defaultModelsExpandDepth': 0,
    'displayRequestDuration': True,
    'tryItOutEnabled': True,
    'syntaxHighlight': {
        'activate': True,
        'theme': 'nord',
    },
}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(
    title=f'Template {"dev" if settings.DEBUG else "prod"} API',
    swagger_ui_parameters=swagger_ui_parameters,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(checks_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url='/docs')
