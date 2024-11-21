from pydantic import BaseModel, EmailStr, Field

from typing import List
from enum import Enum

class UserBase(BaseModel):
    name: str
    email: str
    password: str



class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):  # Exclude password from response
    id: int
    name: str
    email: EmailStr
    blogs: List["BlogResponse"] = Field(default_factory=list)  # Correctly use default_factory

    class Config:
        Form_attribute = True  # Fixed typo: form_attribute -> orm_mode


# Blog schemas
class BlogBase(BaseModel):
    title: str
    description: str


class BlogCreate(BlogBase):
    pass


class BlogResponse(BlogBase):
    id: int
    user_id: int

    class Config:
        form_attribute = True  # Fixed typo: form_attribute -> orm_mode


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    id:int
