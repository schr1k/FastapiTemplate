from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr


class UserId(BaseModel):
    id: int


class UserInfo(User, UserId):
    class Config:
        from_attributes = True


class AddUser(User):
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
