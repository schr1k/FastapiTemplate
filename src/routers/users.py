from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from pydantic import EmailStr

from src.auth.auth import get_auth_user
from src.auth.hash import hash_password
from src.schemas.users import AddUser, Token, UserId, UserInfo
from src.services.users import UsersService

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    summary='Register',
)
async def register(
    username: Annotated[str, Form(description='Username', min_length=4, max_length=30, examples=['username'])],
    email: Annotated[EmailStr, Form(description='Email', examples=['mail@mail.com'])],
    password: Annotated[str, Form(description='Password', min_length=8, examples=['₽@$$w0rD'])],
) -> UserId:
    user = AddUser(
        username=username,
        email=email,
        password=hash_password(password),
    )
    user_id = await UsersService.create_user(user)
    return user_id


@users_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    summary='Login',
)
async def login(
    email: Annotated[EmailStr, Form(description='Email', examples=['mail@mail.com'])],
    password: Annotated[str, Form(description='Password', min_length=8, examples=['₽@$$w0rD'])],
) -> Token:
    token = await UsersService.auth_user_with_jwt(email, password)
    return token


@users_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    summary='Get user info',
)
async def get_me(user_id: Annotated[int, Depends(get_auth_user)]) -> UserInfo:
    user = await UsersService.get_user(user_id)
    return user
