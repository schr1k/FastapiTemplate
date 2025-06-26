from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError, decode, encode

from src.settings import settings

http_bearer = HTTPBearer()


def encode_jwt(
    payload: dict,
    expire_minutes: int = settings.EXPIRE_MINUTES,
) -> str:
    payload_to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expire_minutes)
    payload_to_encode.update(exp=expire, iat=now)
    encoded = encode(payload=payload_to_encode, key=settings.JWT_PRIVATE, algorithm=settings.ALGORITHM)
    return encoded


def decode_jwt(token: str) -> dict:
    try:
        decoded = decode(token, settings.JWT_PUBLIC, algorithms=[settings.ALGORITHM])
    except PyJWTError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid authentication credentials',
        ) from err
    else:
        return decoded


def get_auth_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]) -> int:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    auth_user_id = payload.get('sub')
    return int(auth_user_id)
