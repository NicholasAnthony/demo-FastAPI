from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterModel(BaseModel):
    username: str
    password: str
    email: EmailStr


class LoginModel(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
