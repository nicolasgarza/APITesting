from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: str

class CommentRead(CommentBase):
    id: int
    post_id: int
    owner_id: int 
    content: str
    created_at: datetime

    class Config: 
        from_attributes = True

class Comment(CommentBase):
    id: int
    post_id: int
    owner_id: int

    class Config:
        from_attributes = True

class CommentCreate(CommentBase):
    post_id: int
    owner_id: int
    content: str

class CommentUpdate(CommentBase):
    content: Optional[str]