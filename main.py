from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.database.connection import create_tables, engine
from src.routers.checks import checks_router
from src.routers.users import users_router
from src.settings import settings

swagger_ui_parameters = {
    'tryItOutEnabled': True,
    'syntaxHighlight': {
        'activate': True,
        'theme': 'nord',
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:  # noqa: ARG001
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(
    swagger_ui_parameters=swagger_ui_parameters,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(checks_router)
app.include_router(users_router)

origins = [
    'http://localhost',
    'https://localhost',
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://0.0.0.0',
    'https://0.0.0.0',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', include_in_schema=False)
async def redirect_to_docs() -> None:
    return RedirectResponse(url='/docs')
