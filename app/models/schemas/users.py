from pydantic import BaseModel, EmailStr
from typing import Optional
from app.resources.userTypes import UserTypes


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class User(BaseModel):
    username: str
    usertype: Optional[UserTypes] = UserTypes.Client
    email: EmailStr

class UserWithToken(BaseModel):
    token: str