from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, ClassVar

class CommentBase(BaseModel):
    content: str

class CommentRead(CommentBase):
    id: int
    post_id: int
    owner_id: int 
    content: str
    created_at: datetime

    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class Comment(CommentBase):
    id: int
    post_id: int
    owner_id: int

    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class CommentCreate(CommentBase):
    post_id: int
    owner_id: int
    content: str

class CommentUpdate(CommentBase):
    content: Optional[str]