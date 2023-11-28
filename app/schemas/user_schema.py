from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

class UserRead(UserBase):
    id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None