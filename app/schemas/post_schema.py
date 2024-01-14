from pydantic import BaseModel, ConfigDict
from typing import Optional, ClassVar
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

    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class Post(PostBase):
    id: int
    owner_id: int

    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]