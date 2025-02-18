from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    imageUrl: Optional[str] = None
    username: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    imageUrl: Optional[str] = None
    username: str

    class Config:
        orm_mode = True

class LinkCreate(BaseModel):
    title: str
    url: str
    tags: str
    category: str

class LinkResponse(BaseModel):
    id: str
    title: str
    url: str
    tags: str
    category: str

    class Config:
        orm_mode = True