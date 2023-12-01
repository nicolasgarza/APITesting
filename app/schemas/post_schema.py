from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    title: str
    content: str
    owner_id: int

class PostRead(PostBase):
    id: int
    owner_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]