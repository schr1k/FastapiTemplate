from fastapi import APIRouter, status

checks_router = APIRouter(
    prefix='/checks',
    tags=['checks'],
)


@checks_router.get(
    '',
    status_code=status.HTTP_200_OK,
    summary='Health Check',
)
async def health_check() -> dict:
    return {'status': 'ok'}


@checks_router.head(
    '',
    status_code=status.HTTP_200_OK,
    summary='Health Check',
)
async def head_check() -> None:
    return None
