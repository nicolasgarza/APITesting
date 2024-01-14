from typing import Optional, ClassVar
from pydantic import BaseModel, EmailStr, ConfigDict

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

    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int

    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserFullInfo(BaseModel):
    email: EmailStr
    username: str
    id: int
    hashed_password: str