from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.sql import exists

from src.auth.auth import encode_jwt
from src.auth.hash import verify_password
from src.database.connection import async_session
from src.database.models import UserModel
from src.schemas.users import AddUser, Token, UserId, UserInfo
from src.settings import settings


class UsersService:
    @staticmethod
    async def check_user_exists(email: str, username: str) -> None:
        async with async_session() as session:
            query = select(exists().where(UserModel.email == email))
            result = await session.execute(query)
            email_exists = result.scalar()
            if email_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is already in use')
            query = select(exists().where(UserModel.username == username))
            result = await session.execute(query)
            username_exists = result.scalar()
            if username_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username is already in use')

    @staticmethod
    async def create_user(data: AddUser) -> UserId:
        async with async_session() as session:
            add_user = data.model_dump()
            user = UserModel(**add_user)
            await UsersService.check_user_exists(user.email, user.username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            response = UserId(
                id=user.id,
            )
            return response

    @staticmethod
    async def validate_auth_user(email: str, password: str) -> UserInfo | None:
        async with async_session() as session:
            query = select(UserModel).where(UserModel.email == email)
            result = await session.execute(query)
            user = await result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
            if not verify_password(plain_password=password, hashed_password=user.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
            return user

    @staticmethod
    async def auth_user_with_jwt(email: str, password: str) -> Token:
        user = await UsersService.validate_auth_user(email, password)
        payload = {
            'sub': str(user.id),
            'username': user.username,
            'email': user.email,
        }
        token = encode_jwt(payload=payload)
        return Token(access_token=token, token_type=settings.TOKEN_TYPE)

    @staticmethod
    async def get_user(user_id: int) -> UserInfo:
        async with async_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user_model = result.scalars().first()
            user = UserInfo.model_validate(user_model)
            return user
